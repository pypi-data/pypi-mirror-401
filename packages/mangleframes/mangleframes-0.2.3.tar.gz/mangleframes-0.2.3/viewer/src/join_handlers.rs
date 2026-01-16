//! HTTP handlers for join analysis endpoints.

use std::sync::Arc;

use axum::body::Body;
use axum::extract::{Path, Query, State};
use axum::http::{header, Response, StatusCode};
use axum::response::IntoResponse;
use axum::Json;
use serde::Deserialize;
use serde_json::json;

use crate::export;
use crate::web_server::AppState;

#[derive(Deserialize)]
pub struct JoinRequest {
    left_frame: String,
    right_frame: String,
    left_keys: Vec<String>,
    right_keys: Vec<String>,
}

pub async fn analyze_join(
    State(state): State<Arc<AppState>>,
    Json(req): Json<JoinRequest>,
) -> impl IntoResponse {
    if req.left_keys.len() != req.right_keys.len() {
        return error_response(StatusCode::BAD_REQUEST, "Key count mismatch");
    }
    if req.left_keys.is_empty() {
        return error_response(StatusCode::BAD_REQUEST, "At least one join key required");
    }

    // Build config for Python join analysis handler
    let config = json!({
        "left_keys": req.left_keys,
        "right_keys": req.right_keys,
        "sample_limit": 100
    });

    // Execute join analysis via Python/Spark through socket client
    match state.client.analyze_join(&req.left_frame, &req.right_frame, &config) {
        Ok(result) => Json(result).into_response(),
        Err(e) => error_response(StatusCode::INTERNAL_SERVER_ERROR, &e.to_string()),
    }
}

#[derive(Deserialize)]
pub struct UnmatchedQuery {
    left_frame: String,
    right_frame: String,
    left_keys: String,
    right_keys: String,
    offset: Option<usize>,
    limit: Option<usize>,
}

pub async fn get_unmatched(
    State(state): State<Arc<AppState>>,
    Path(side): Path<String>,
    Query(query): Query<UnmatchedQuery>,
) -> impl IntoResponse {
    if side != "left" && side != "right" {
        return error_response(StatusCode::BAD_REQUEST, "Side must be 'left' or 'right'");
    }

    let left_keys: Vec<String> = query.left_keys.split(',').map(|s| s.trim().to_string()).collect();
    let right_keys: Vec<String> = query.right_keys.split(',').map(|s| s.trim().to_string()).collect();

    if left_keys.len() != right_keys.len() {
        return error_response(StatusCode::BAD_REQUEST, "Key count mismatch");
    }

    let offset = query.offset.unwrap_or(0);
    let limit = query.limit.unwrap_or(100).min(1000);

    // Build config for Python unmatched page handler
    let config = json!({
        "left_keys": left_keys,
        "right_keys": right_keys,
        "side": side,
        "offset": offset,
        "limit": limit
    });

    // Execute via Python/Spark through socket client
    match state.client.get_join_unmatched(&query.left_frame, &query.right_frame, &config) {
        Ok(result) => Json(result).into_response(),
        Err(e) => error_response(StatusCode::INTERNAL_SERVER_ERROR, &e.to_string()),
    }
}

#[derive(Deserialize)]
pub struct ExportRequest {
    left_frame: String,
    right_frame: String,
    left_keys: Vec<String>,
    right_keys: Vec<String>,
    side: String,
    format: String,
}

pub async fn export_unmatched(
    State(state): State<Arc<AppState>>,
    Json(req): Json<ExportRequest>,
) -> impl IntoResponse {
    if req.side != "left" && req.side != "right" {
        return error_response(StatusCode::BAD_REQUEST, "Side must be 'left' or 'right'");
    }

    // Build config to get all unmatched rows (large limit)
    let config = json!({
        "left_keys": req.left_keys,
        "right_keys": req.right_keys,
        "side": req.side,
        "offset": 0,
        "limit": 100000
    });

    let result = match state.client.get_join_unmatched(&req.left_frame, &req.right_frame, &config) {
        Ok(r) => r,
        Err(e) => return error_response(StatusCode::INTERNAL_SERVER_ERROR, &e.to_string()),
    };

    // Extract rows from result and convert to RecordBatch for export
    let rows = match result.get("rows") {
        Some(r) => r.as_array().cloned().unwrap_or_default(),
        None => vec![],
    };

    let batches = match json_to_batches(&rows) {
        Ok(b) => b,
        Err(e) => return error_response(StatusCode::INTERNAL_SERVER_ERROR, &e),
    };

    let (content_type, data, ext) = match req.format.as_str() {
        "csv" => match export::to_csv(&batches) {
            Ok(d) => ("text/csv", d, "csv"),
            Err(e) => return error_response(StatusCode::INTERNAL_SERVER_ERROR, &e.to_string()),
        },
        "json" => match export::to_json(&batches) {
            Ok(d) => ("application/json", d, "json"),
            Err(e) => return error_response(StatusCode::INTERNAL_SERVER_ERROR, &e.to_string()),
        },
        "parquet" => match export::to_parquet(&batches) {
            Ok(d) => ("application/octet-stream", d, "parquet"),
            Err(e) => return error_response(StatusCode::INTERNAL_SERVER_ERROR, &e.to_string()),
        },
        _ => return error_response(StatusCode::BAD_REQUEST, "Invalid format"),
    };

    let filename = format!("{}_unmatched.{}", req.side, ext);
    Response::builder()
        .header(header::CONTENT_TYPE, content_type)
        .header(header::CONTENT_DISPOSITION, format!("attachment; filename=\"{}\"", filename))
        .body(Body::from(data))
        .unwrap()
        .into_response()
}

fn error_response(status: StatusCode, msg: &str) -> axum::response::Response {
    (status, Json(json!({"error": msg}))).into_response()
}

fn json_to_batches(rows: &[serde_json::Value]) -> Result<Vec<arrow::record_batch::RecordBatch>, String> {
    if rows.is_empty() {
        return Ok(vec![]);
    }

    let json_bytes = serde_json::to_vec(rows).map_err(|e| e.to_string())?;
    let cursor = std::io::Cursor::new(json_bytes);
    let reader = arrow::json::ReaderBuilder::new(arrow::datatypes::SchemaRef::new(
        infer_schema_from_json(rows)?
    )).build(cursor).map_err(|e| e.to_string())?;

    reader.into_iter().collect::<Result<Vec<_>, _>>().map_err(|e| e.to_string())
}

fn infer_schema_from_json(rows: &[serde_json::Value]) -> Result<arrow::datatypes::Schema, String> {
    use arrow::datatypes::{DataType, Field};

    let first = rows.first().ok_or("No rows")?;
    let obj = first.as_object().ok_or("Row is not an object")?;

    let fields: Vec<Field> = obj.iter().map(|(k, v)| {
        let dtype = match v {
            serde_json::Value::Bool(_) => DataType::Boolean,
            serde_json::Value::Number(n) if n.is_i64() => DataType::Int64,
            serde_json::Value::Number(_) => DataType::Float64,
            _ => DataType::Utf8,
        };
        Field::new(k, dtype, true)
    }).collect();

    Ok(arrow::datatypes::Schema::new(fields))
}
