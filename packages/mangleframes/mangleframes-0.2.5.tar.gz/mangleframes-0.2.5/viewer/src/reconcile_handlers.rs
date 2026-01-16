//! HTTP handlers for CSV reconciliation endpoints.

use std::io::Cursor;
use std::sync::Arc;
use std::time::Instant;

use arrow::record_batch::RecordBatch;
use arrow_csv::ReaderBuilder;
use axum::body::Body;
use axum::extract::{Multipart, State};
use axum::http::{header, Response, StatusCode};
use axum::response::IntoResponse;
use axum::Json;
use base64::{Engine as _, engine::general_purpose::STANDARD as BASE64};
use serde::{Deserialize, Serialize};
use serde_json::json;

use crate::dashboard::{self, DashboardMetadata};
use crate::web_server::{AppState, CachedFrame};

const CSV_FRAME_PREFIX: &str = "__csv__";

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum JoinType {
    Inner,
    Left,
    Right,
    Full,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum AggregationType {
    Sum,
    Count,
    Min,
    Max,
    Avg,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AggregationConfig {
    pub column: String,
    pub aggregations: Vec<AggregationType>,
}

#[derive(Deserialize)]
pub struct UploadCsvJsonRequest {
    pub csv_data: String,
    pub frame_name: String,
}

#[derive(Serialize)]
pub struct UploadCsvResponse {
    pub frame_name: String,
    pub columns: Vec<ColumnInfo>,
    pub row_count: usize,
}

#[derive(Serialize)]
pub struct ColumnInfo {
    pub name: String,
    pub data_type: String,
    pub nullable: bool,
}

#[derive(Deserialize)]
pub struct ReconcileRequest {
    pub source_frame: String,
    pub target_frame: String,
    #[serde(default = "default_source_type")]
    pub source_type: String,
    pub source_group_by: Vec<String>,
    pub target_group_by: Vec<String>,
    pub source_join_keys: Vec<String>,
    pub target_join_keys: Vec<String>,
    pub join_type: JoinType,
    #[serde(default)]
    pub aggregations: Vec<AggregationConfig>,
    pub sample_limit: Option<usize>,
}

fn default_source_type() -> String {
    "csv".to_string()
}

#[derive(Deserialize)]
pub struct ExportReconcileRequest {
    pub source_frame: String,
    pub target_frame: String,
    #[serde(default = "default_source_type")]
    pub source_type: String,
    pub source_group_by: Vec<String>,
    pub target_group_by: Vec<String>,
    pub source_join_keys: Vec<String>,
    pub target_join_keys: Vec<String>,
    pub join_type: JoinType,
    #[serde(default)]
    pub aggregations: Vec<AggregationConfig>,
}

fn parse_csv(data: &[u8]) -> Result<Vec<RecordBatch>, String> {
    let cursor = Cursor::new(data);
    let format = arrow_csv::reader::Format::default().with_header(true);
    let (schema, _) = format
        .infer_schema(cursor, Some(100))
        .map_err(|e| e.to_string())?;

    let cursor = Cursor::new(data);
    let reader = ReaderBuilder::new(Arc::new(schema))
        .with_header(true)
        .build(cursor)
        .map_err(|e| e.to_string())?;

    reader.collect::<Result<Vec<_>, _>>().map_err(|e| e.to_string())
}

pub async fn upload_csv_multipart(
    State(state): State<Arc<AppState>>,
    mut multipart: Multipart,
) -> impl IntoResponse {
    let mut csv_data: Option<Vec<u8>> = None;
    let mut frame_name: Option<String> = None;

    while let Ok(Some(field)) = multipart.next_field().await {
        let name = field.name().unwrap_or("").to_string();
        match name.as_str() {
            "file" => {
                csv_data = match field.bytes().await {
                    Ok(b) => Some(b.to_vec()),
                    Err(e) => return error_response(StatusCode::BAD_REQUEST, &e.to_string()),
                };
            }
            "frame_name" => {
                frame_name = match field.text().await {
                    Ok(t) => Some(t),
                    Err(e) => return error_response(StatusCode::BAD_REQUEST, &e.to_string()),
                };
            }
            _ => {}
        }
    }

    let csv_data = match csv_data {
        Some(d) => d,
        None => return error_response(StatusCode::BAD_REQUEST, "No CSV file provided"),
    };

    let frame_name = frame_name.unwrap_or_else(|| {
        format!("csv_upload_{}", chrono::Utc::now().timestamp_millis())
    });

    process_csv_upload(&state, &csv_data, &frame_name).await
}

pub async fn upload_csv_json(
    State(state): State<Arc<AppState>>,
    Json(req): Json<UploadCsvJsonRequest>,
) -> impl IntoResponse {
    let csv_data = match BASE64.decode(&req.csv_data) {
        Ok(d) => d,
        Err(e) => return error_response(StatusCode::BAD_REQUEST, &format!("Invalid base64: {}", e)),
    };

    process_csv_upload(&state, &csv_data, &req.frame_name).await
}

async fn process_csv_upload(
    state: &AppState,
    csv_data: &[u8],
    frame_name: &str,
) -> axum::response::Response {
    let batches = match parse_csv(csv_data) {
        Ok(b) => b,
        Err(e) => return error_response(StatusCode::BAD_REQUEST, &e),
    };

    if batches.is_empty() {
        return error_response(StatusCode::BAD_REQUEST, "CSV has no data");
    }

    let schema = batches[0].schema();
    let columns: Vec<ColumnInfo> = schema.fields().iter().map(|f| ColumnInfo {
        name: f.name().clone(),
        data_type: format!("{:?}", f.data_type()),
        nullable: f.is_nullable(),
    }).collect();

    let row_count: usize = batches.iter().map(|b| b.num_rows()).sum();

    state.evict_frame_if_needed().await;
    let mut cache = state.cache.write().await;
    cache.insert(
        format!("{}{}", CSV_FRAME_PREFIX, frame_name),
        CachedFrame { batches, stats: None, last_access: Instant::now() },
    );

    Json(UploadCsvResponse { frame_name: frame_name.to_string(), columns, row_count }).into_response()
}

pub async fn list_csv_frames(State(state): State<Arc<AppState>>) -> impl IntoResponse {
    let cache = state.cache.read().await;
    let frames: Vec<String> = cache.keys()
        .filter(|k| k.starts_with(CSV_FRAME_PREFIX))
        .map(|k| k.strip_prefix(CSV_FRAME_PREFIX).unwrap_or(k).to_string())
        .collect();
    Json(json!({ "frames": frames }))
}

pub async fn reconcile(
    State(state): State<Arc<AppState>>,
    Json(req): Json<ReconcileRequest>,
) -> impl IntoResponse {
    if req.source_join_keys.len() != req.target_join_keys.len() {
        return error_response(StatusCode::BAD_REQUEST, "Join key count mismatch");
    }
    if req.source_join_keys.is_empty() {
        return error_response(StatusCode::BAD_REQUEST, "At least one join key required");
    }
    if req.source_group_by.is_empty() {
        return error_response(StatusCode::BAD_REQUEST, "At least one source group-by column required");
    }
    if req.target_group_by.is_empty() {
        return error_response(StatusCode::BAD_REQUEST, "At least one target group-by column required");
    }
    if !req.source_join_keys.iter().all(|k| req.source_group_by.contains(k)) {
        return error_response(StatusCode::BAD_REQUEST, "Source join keys must be subset of group-by");
    }
    if !req.target_join_keys.iter().all(|k| req.target_group_by.contains(k)) {
        return error_response(StatusCode::BAD_REQUEST, "Target join keys must be subset of group-by");
    }
    if req.aggregations.is_empty() {
        return error_response(StatusCode::BAD_REQUEST, "At least one aggregation required");
    }

    // Build config for Python reconciliation handler
    let config = json!({
        "source_type": req.source_type,
        "source_group_by": req.source_group_by,
        "target_group_by": req.target_group_by,
        "source_join_keys": req.source_join_keys,
        "target_join_keys": req.target_join_keys,
        "join_type": format!("{:?}", req.join_type).to_lowercase(),
        "aggregations": req.aggregations,
        "sample_limit": req.sample_limit.unwrap_or(100)
    });

    // Execute reconciliation via Python/Spark through socket client
    match state.client.reconcile_aggregated(&req.source_frame, &req.target_frame, &config) {
        Ok(result) => Json(result).into_response(),
        Err(e) => error_response(StatusCode::INTERNAL_SERVER_ERROR, &e.to_string()),
    }
}

pub async fn export_reconciliation(
    State(state): State<Arc<AppState>>,
    Json(req): Json<ExportReconcileRequest>,
) -> impl IntoResponse {
    // Build config for Python reconciliation handler (with no sample limit for full export)
    let config = json!({
        "source_type": req.source_type,
        "source_group_by": req.source_group_by,
        "target_group_by": req.target_group_by,
        "source_join_keys": req.source_join_keys,
        "target_join_keys": req.target_join_keys,
        "join_type": format!("{:?}", req.join_type).to_lowercase(),
        "aggregations": req.aggregations,
        "sample_limit": 0
    });

    // Execute reconciliation via Python/Spark
    let result = match state.client.reconcile_aggregated(&req.source_frame, &req.target_frame, &config) {
        Ok(r) => r,
        Err(e) => return error_response(StatusCode::INTERNAL_SERVER_ERROR, &e.to_string()),
    };

    let metadata = DashboardMetadata {
        source_frame: req.source_frame.clone(),
        target_frame: req.target_frame.clone(),
        source_type: req.source_type.clone(),
        group_by_source: req.source_group_by.clone(),
        group_by_target: req.target_group_by.clone(),
        join_keys_source: req.source_join_keys.clone(),
        join_keys_target: req.target_join_keys.clone(),
    };

    let html = dashboard::generate_reconcile_dashboard(&result, &metadata);
    let filename = format!("reconciliation_{}_{}.html", req.source_frame, req.target_frame);

    Response::builder()
        .header(header::CONTENT_TYPE, "text/html; charset=utf-8")
        .header(header::CONTENT_DISPOSITION, format!("attachment; filename=\"{}\"", filename))
        .body(Body::from(html))
        .unwrap()
        .into_response()
}

fn error_response(status: StatusCode, msg: &str) -> axum::response::Response {
    (status, Json(json!({"error": msg}))).into_response()
}
