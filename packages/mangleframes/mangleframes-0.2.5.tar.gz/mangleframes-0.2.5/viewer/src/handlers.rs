//! HTTP route handlers for the web API.

use std::sync::Arc;
use std::time::Instant;

use axum::body::Body;
use axum::extract::{Path, Query, State};
use axum::http::{header, Response, StatusCode};
use axum::response::IntoResponse;
use axum::Json;
use serde::Deserialize;
use serde_json::json;

use crate::arrow_reader::{batches_to_json, batches_to_json_bytes, parse_arrow_stream, total_row_count};
use crate::export;
use crate::perf::TimingSample;
use crate::web_server::{AppState, CachedFrame, JsonCacheEntry, JsonCacheKey};

const INDEX_HTML: &str = include_str!("../static/index.html");
const APP_JS: &str = include_str!("../static/app.js");
const STYLE_CSS: &str = include_str!("../static/style.css");

pub async fn serve_index() -> impl IntoResponse {
    Response::builder()
        .header(header::CONTENT_TYPE, "text/html")
        .body(Body::from(INDEX_HTML))
        .unwrap()
}

pub async fn serve_js() -> impl IntoResponse {
    Response::builder()
        .header(header::CONTENT_TYPE, "application/javascript")
        .body(Body::from(APP_JS))
        .unwrap()
}

pub async fn serve_css() -> impl IntoResponse {
    Response::builder()
        .header(header::CONTENT_TYPE, "text/css")
        .body(Body::from(STYLE_CSS))
        .unwrap()
}

pub async fn list_frames(State(state): State<Arc<AppState>>) -> impl IntoResponse {
    match state.client.list_frames_async().await {
        Ok(names) => Json(json!({"frames": names})).into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, Json(json!({"error": e.to_string()}))).into_response(),
    }
}

pub async fn get_schema(
    State(state): State<Arc<AppState>>,
    Path(name): Path<String>,
) -> impl IntoResponse {
    match state.client.get_schema_async(name).await {
        Ok(schema) => Json(schema).into_response(),
        Err(e) => (StatusCode::NOT_FOUND, Json(json!({"error": e.to_string()}))).into_response(),
    }
}

#[derive(Deserialize)]
pub struct DataQuery {
    offset: Option<usize>,
    limit: Option<usize>,
}


pub async fn get_data(
    State(state): State<Arc<AppState>>,
    Path(name): Path<String>,
    Query(query): Query<DataQuery>,
) -> impl IntoResponse {
    let offset = query.offset.unwrap_or(0);
    let limit = query.limit.unwrap_or(100).min(10000);
    let total_start = Instant::now();

    // Check JSON cache first for instant response
    let cache_key = JsonCacheKey { frame: name.clone(), offset, limit };
    {
        let json_cache = state.json_cache.read().await;
        if let Some(entry) = json_cache.get(&cache_key) {
            let total_ms = total_start.elapsed().as_millis() as u64;
            record_sample(&state, &name, limit, 0, 0, 0, 0, 0, 0, total_ms, true).await;
            return Response::builder()
                .header(header::CONTENT_TYPE, "application/json")
                .body(Body::from(entry.data.clone()))
                .unwrap()
                .into_response();
        }
    }

    let cache = state.cache.read().await;
    if let Some(cached) = cache.get(&name) {
        let json_start = Instant::now();
        let (rows_bytes, rows_len) = batches_to_json_bytes(&cached.batches, offset, limit);
        let json_ms = json_start.elapsed().as_millis() as u64;
        let total = total_row_count(&cached.batches);
        let total_ms = total_start.elapsed().as_millis() as u64;

        record_sample(&state, &name, rows_len, 0, 0, 0, 0, 0, json_ms, total_ms, true).await;

        let body = build_response_json(&rows_bytes, total, offset, 0, 0, 0, 0, json_ms, total_ms, rows_len, 0, true);

        // Cache JSON response for future requests
        drop(cache);
        state.evict_json_if_needed().await;
        let mut json_cache = state.json_cache.write().await;
        json_cache.insert(cache_key, JsonCacheEntry { data: body.clone(), created: Instant::now() });

        return Response::builder()
            .header(header::CONTENT_TYPE, "application/json")
            .body(Body::from(body))
            .unwrap()
            .into_response();
    }
    drop(cache);

    let fetch_limit = (offset + limit).max(10000);

    let socket_start = Instant::now();
    match state.client.get_frame_async(name.clone(), fetch_limit).await {
        Ok(response) => {
            let socket_ms = socket_start.elapsed().as_millis() as u64;
            let bytes = response.data.len();

            let parse_start = Instant::now();
            match parse_arrow_stream(&response.data) {
                Ok(batches) => {
                    let parse_ms = parse_start.elapsed().as_millis() as u64;

                    let json_start = Instant::now();
                    let (rows_bytes, rows_len) = batches_to_json_bytes(&batches, offset, limit);
                    let json_ms = json_start.elapsed().as_millis() as u64;

                    let total = response.total_rows as usize;
                    let total_ms = total_start.elapsed().as_millis() as u64;

                    state.evict_frame_if_needed().await;
                    let mut cache = state.cache.write().await;
                    cache.insert(name.clone(), CachedFrame { batches, stats: None, last_access: Instant::now() });

                    let rows_fetched = response.total_rows as usize;
                    record_sample(
                        &state, &name, rows_fetched, bytes,
                        response.spark_ms, response.ipc_ms, socket_ms, parse_ms, json_ms,
                        total_ms, false
                    ).await;

                    let body = build_response_json(
                        &rows_bytes, total, offset,
                        response.spark_ms, response.ipc_ms, socket_ms, parse_ms, json_ms, total_ms,
                        rows_fetched, bytes, false
                    );

                    // Cache JSON response for future requests
                    state.evict_json_if_needed().await;
                    let mut json_cache = state.json_cache.write().await;
                    json_cache.insert(cache_key, JsonCacheEntry { data: body.clone(), created: Instant::now() });
                    drop(json_cache);

                    Response::builder()
                        .header(header::CONTENT_TYPE, "application/json")
                        .body(Body::from(body))
                        .unwrap()
                        .into_response()
                }
                Err(e) => {
                    (StatusCode::INTERNAL_SERVER_ERROR, Json(json!({"error": e.to_string()})))
                        .into_response()
                }
            }
        }
        Err(e) => (StatusCode::NOT_FOUND, Json(json!({"error": e.to_string()}))).into_response(),
    }
}

/// Build response JSON directly as bytes, embedding rows without re-parsing
#[allow(clippy::too_many_arguments)]
fn build_response_json(
    rows_bytes: &[u8], total: usize, offset: usize,
    spark_ms: u64, ipc_ms: u64, socket_ms: u64, parse_ms: u64, json_ms: u64, total_ms: u64,
    rows_fetched: usize, bytes_transferred: usize, cached: bool,
) -> Vec<u8> {
    let timing = format!(
        r#"{{"spark_ms":{},"ipc_ms":{},"socket_ms":{},"parse_ms":{},"json_ms":{},"total_ms":{},"rows_fetched":{},"bytes_transferred":{},"cached":{}}}"#,
        spark_ms, ipc_ms, socket_ms, parse_ms, json_ms, total_ms, rows_fetched, bytes_transferred, cached
    );

    let mut result = Vec::with_capacity(rows_bytes.len() + 200);
    result.extend_from_slice(b"{\"rows\":");
    result.extend_from_slice(rows_bytes);
    result.extend_from_slice(b",\"total\":");
    result.extend_from_slice(total.to_string().as_bytes());
    result.extend_from_slice(b",\"offset\":");
    result.extend_from_slice(offset.to_string().as_bytes());
    result.extend_from_slice(b",\"timing\":");
    result.extend_from_slice(timing.as_bytes());
    result.extend_from_slice(b"}");
    result
}

#[allow(clippy::too_many_arguments)]
async fn record_sample(
    state: &AppState, name: &str, rows: usize, bytes: usize,
    spark_ms: u64, ipc_ms: u64, socket_ms: u64, parse_ms: u64, json_ms: u64,
    total_ms: u64, cached: bool,
) {
    state.perf.record(name, TimingSample {
        timestamp: Instant::now(),
        rows, bytes, spark_ms, ipc_ms, socket_ms, parse_ms, json_ms, total_ms, cached,
    }).await;
}

pub async fn get_stats(
    State(state): State<Arc<AppState>>,
    Path(name): Path<String>,
) -> impl IntoResponse {
    match state.client.get_stats_async(name).await {
        Ok(stats) => Json(stats).into_response(),
        Err(e) => (StatusCode::NOT_FOUND, Json(json!({"error": e.to_string()}))).into_response(),
    }
}

#[derive(Deserialize)]
pub struct ExportRequest {
    format: String,
}

pub async fn export_frame(
    State(state): State<Arc<AppState>>,
    Path(name): Path<String>,
    Json(req): Json<ExportRequest>,
) -> impl IntoResponse {
    let cache = state.cache.read().await;
    let batches = match cache.get(&name) {
        Some(cached) => cached.batches.clone(),
        None => {
            drop(cache);
            match state.client.get_frame(&name, 100000) {
                Ok(response) => match parse_arrow_stream(&response.data) {
                    Ok(b) => b,
                    Err(e) => {
                        return (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response()
                    }
                },
                Err(e) => return (StatusCode::NOT_FOUND, e.to_string()).into_response(),
            }
        }
    };

    let (content_type, data) = match req.format.as_str() {
        "csv" => match export::to_csv(&batches) {
            Ok(d) => ("text/csv", d),
            Err(e) => return (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
        },
        "json" => match export::to_json(&batches) {
            Ok(d) => ("application/json", d),
            Err(e) => return (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
        },
        "parquet" => match export::to_parquet(&batches) {
            Ok(d) => ("application/octet-stream", d),
            Err(e) => return (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
        },
        _ => return (StatusCode::BAD_REQUEST, "Invalid format").into_response(),
    };

    let filename = format!("{}.{}", name, req.format);
    Response::builder()
        .header(header::CONTENT_TYPE, content_type)
        .header(header::CONTENT_DISPOSITION, format!("attachment; filename=\"{}\"", filename))
        .body(Body::from(data))
        .unwrap()
        .into_response()
}

#[derive(Deserialize)]
pub struct QueryRequest {
    sql: String,
}

pub async fn execute_query(
    State(state): State<Arc<AppState>>,
    Json(req): Json<QueryRequest>,
) -> impl IntoResponse {
    // Execute SQL via Python/Spark through socket client
    match state.client.execute_sql_async(req.sql, 1000).await {
        Ok(response) => {
            match parse_arrow_stream(&response.data) {
                Ok(batches) => {
                    let rows = batches_to_json(&batches, 0, 1000);
                    let total = total_row_count(&batches);
                    Json(json!({"rows": rows, "total": total})).into_response()
                }
                Err(e) => (StatusCode::INTERNAL_SERVER_ERROR,
                    Json(json!({"error": e.to_string()}))).into_response(),
            }
        }
        Err(e) => (StatusCode::BAD_REQUEST, Json(json!({"error": e.to_string()}))).into_response(),
    }
}

pub async fn get_perf_stats(State(state): State<Arc<AppState>>) -> impl IntoResponse {
    let frames = state.perf.get_all_metrics().await;
    let global = state.perf.get_global_metrics().await;
    Json(json!({ "frames": frames, "global": global }))
}

#[derive(Deserialize)]
pub struct BenchmarkRequest {
    frame: String,
    sample_sizes: Vec<usize>,
    iterations: Option<usize>,
}

pub async fn run_benchmark(
    State(state): State<Arc<AppState>>,
    Json(req): Json<BenchmarkRequest>,
) -> impl IntoResponse {
    let iterations = req.iterations.unwrap_or(3);
    let mut results = Vec::with_capacity(req.sample_sizes.len());

    for sample_size in &req.sample_sizes {
        let mut timings = Vec::with_capacity(iterations);

        for _ in 0..iterations {
            // Clear cache to force fresh fetch
            state.cache.write().await.remove(&req.frame);

            let start = Instant::now();
            match state.client.get_frame(&req.frame, *sample_size) {
                Ok(response) => {
                    let _ = parse_arrow_stream(&response.data);
                    let elapsed_ms = start.elapsed().as_millis() as u64;
                    timings.push(elapsed_ms);
                }
                Err(e) => {
                    return (StatusCode::NOT_FOUND, Json(json!({"error": e.to_string()})))
                        .into_response();
                }
            }
        }

        let avg_ms = timings.iter().sum::<u64>() as f64 / timings.len() as f64;
        let rows_per_sec = *sample_size as f64 / (avg_ms / 1000.0);

        results.push(json!({
            "sample_size": sample_size,
            "iterations": iterations,
            "avg_total_ms": avg_ms,
            "avg_rows_per_sec": rows_per_sec,
            "min_ms": timings.iter().min().unwrap_or(&0),
            "max_ms": timings.iter().max().unwrap_or(&0)
        }));
    }

    Json(json!({ "results": results })).into_response()
}

#[derive(Deserialize)]
pub struct StreamRequest {
    frame: String,
    chunk_size: usize,
    max_chunks: usize,
}

pub async fn stream_benchmark(
    State(state): State<Arc<AppState>>,
    Json(req): Json<StreamRequest>,
) -> impl IntoResponse {
    let start = Instant::now();
    let mut chunks_processed = 0;
    let mut total_rows = 0;
    let mut total_bytes = 0;
    let mut chunk_timings = Vec::with_capacity(req.max_chunks);

    for chunk_idx in 0..req.max_chunks {
        let chunk_start = Instant::now();
        match state.client.get_frame(&req.frame, req.chunk_size) {
            Ok(response) => {
                let rows = response.total_rows as usize;
                let bytes = response.data.len();
                let chunk_ms = chunk_start.elapsed().as_millis() as u64;

                // Parse but don't store - just measure
                let _ = parse_arrow_stream(&response.data);

                chunks_processed += 1;
                total_rows += rows;
                total_bytes += bytes;
                chunk_timings.push(json!({
                    "chunk": chunk_idx,
                    "rows": rows,
                    "ms": chunk_ms
                }));

                // Stop if we got fewer rows than requested (end of data)
                if rows < req.chunk_size {
                    break;
                }
            }
            Err(e) => {
                return (StatusCode::NOT_FOUND, Json(json!({"error": e.to_string()})))
                    .into_response();
            }
        }
    }

    let elapsed_secs = start.elapsed().as_secs_f64();
    Json(json!({
        "chunks_processed": chunks_processed,
        "total_rows": total_rows,
        "total_bytes": total_bytes,
        "elapsed_seconds": elapsed_secs,
        "rows_per_sec": total_rows as f64 / elapsed_secs,
        "bytes_per_sec": total_bytes as f64 / elapsed_secs,
        "chunk_timings": chunk_timings
    }))
    .into_response()
}
