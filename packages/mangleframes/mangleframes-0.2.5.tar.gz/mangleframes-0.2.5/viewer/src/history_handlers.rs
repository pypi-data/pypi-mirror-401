//! HTTP handlers for history coverage analysis endpoints.

use std::sync::Arc;

use axum::extract::State;
use axum::http::StatusCode;
use axum::response::IntoResponse;
use axum::Json;
use serde::Deserialize;
use serde_json::json;

use crate::history_analysis::{
    DateGap, FrameDataLoss, FrameKeyStats, FrameTemporalStats, HistoryAnalyzer,
    PairwiseOverlap, TemporalRangeStats,
};
use crate::web_server::AppState;

#[derive(Deserialize)]
pub struct FrameConfig {
    pub frame: String,
    pub columns: Vec<String>,
}

#[derive(Deserialize)]
pub struct JoinPair {
    pub source_frame: String,
    pub target_frame: String,
    pub source_keys: Vec<String>,
    pub target_keys: Vec<String>,
}

#[derive(Deserialize)]
pub struct HistoryRequest {
    pub frames: Vec<FrameConfig>,
    pub join_pairs: Vec<JoinPair>,
    pub bucket_size: Option<String>,
}

pub async fn analyze_history(
    State(state): State<Arc<AppState>>,
    Json(req): Json<HistoryRequest>,
) -> impl IntoResponse {
    if req.frames.is_empty() {
        return error_response(StatusCode::BAD_REQUEST, "At least one frame required");
    }

    if req.frames.len() > 5 {
        return error_response(StatusCode::BAD_REQUEST, "Maximum 5 frames supported");
    }

    for jp in &req.join_pairs {
        if jp.source_keys.len() != jp.target_keys.len() {
            return error_response(
                StatusCode::BAD_REQUEST,
                "Source and target keys must have same length",
            );
        }
        if jp.source_frame == jp.target_frame {
            return error_response(StatusCode::BAD_REQUEST, "Cannot join frame to itself");
        }
    }

    let mut analyzer = HistoryAnalyzer::new();
    let bucket = req.bucket_size.as_deref().unwrap_or("month");

    // Collect key stats for each frame
    for fc in &req.frames {
        match state.client.get_join_keys(&fc.frame, &fc.columns) {
            Ok(result) => {
                let stats = FrameKeyStats {
                    frame: result["frame"].as_str().unwrap_or("").to_string(),
                    columns: fc.columns.clone(),
                    cardinality: result["cardinality"].as_u64().unwrap_or(0) as usize,
                    null_count: result["null_count"].as_u64().unwrap_or(0) as usize,
                    total_rows: result["total_rows"].as_u64().unwrap_or(0) as usize,
                };
                analyzer.add_key_stats(stats);
            }
            Err(e) => {
                return error_response(
                    StatusCode::INTERNAL_SERVER_ERROR,
                    &format!("Failed to get key stats for {}: {}", fc.frame, e),
                );
            }
        }
    }

    // Auto-detect date columns from join keys and run temporal analysis
    for fc in &req.frames {
        // Get schema to check column types
        let date_column = match state.client.get_schema(&fc.frame) {
            Ok(schema) => {
                let columns = schema["columns"].as_array();
                fc.columns.iter().find(|col_name| {
                    columns.map_or(false, |cols| {
                        cols.iter().any(|c| {
                            let name = c["name"].as_str().unwrap_or("");
                            let dtype = c["type"].as_str().unwrap_or("").to_lowercase();
                            name == *col_name && (dtype.contains("date") || dtype.contains("timestamp"))
                        })
                    })
                }).cloned()
            }
            Err(_) => None,
        };

        // If join key is a date column, run temporal analysis
        if let Some(ref date_col) = date_column {
            // Collect temporal bucket stats
            if let Ok(result) = state.client.get_join_temporal(&fc.frame, date_col, bucket) {
                let buckets: std::collections::HashMap<String, usize> = result["buckets"]
                    .as_object()
                    .map(|obj| {
                        obj.iter()
                            .map(|(k, v)| (k.clone(), v.as_u64().unwrap_or(0) as usize))
                            .collect()
                    })
                    .unwrap_or_default();

                let stats = FrameTemporalStats {
                    frame: fc.frame.clone(),
                    column: date_col.clone(),
                    bucket_size: bucket.to_string(),
                    min: result["min"].as_str().map(String::from),
                    max: result["max"].as_str().map(String::from),
                    buckets,
                };
                analyzer.add_temporal_stats(stats);
            }

            // Collect detailed temporal range stats
            if let Ok(result) = state.client.get_temporal_range(&fc.frame, date_col, bucket) {
                let internal_gaps: Vec<DateGap> = result["internal_gaps"]
                    .as_array()
                    .map(|arr| {
                        arr.iter()
                            .filter_map(|g| {
                                Some(DateGap {
                                    start: g["start"].as_str()?.to_string(),
                                    end: g["end"].as_str()?.to_string(),
                                    periods: g["periods"].as_u64()? as usize,
                                })
                            })
                            .collect()
                    })
                    .unwrap_or_default();

                let range_stats = TemporalRangeStats {
                    frame: fc.frame.clone(),
                    column: date_col.clone(),
                    granularity: bucket.to_string(),
                    min_date: result["min_date"].as_str().map(String::from),
                    max_date: result["max_date"].as_str().map(String::from),
                    total_rows: result["total_rows"].as_u64().unwrap_or(0) as usize,
                    null_dates: result["null_dates"].as_u64().unwrap_or(0) as usize,
                    distinct_dates: result["distinct_dates"].as_u64().unwrap_or(0) as usize,
                    internal_gaps,
                };
                analyzer.add_temporal_range(range_stats);
            }
        }
    }

    // Compute overlaps for explicit join pairs
    for jp in &req.join_pairs {
        match state.client.get_join_overlap(
            &jp.source_frame,
            &jp.target_frame,
            &jp.source_keys,
            &jp.target_keys,
        ) {
            Ok(result) => {
                let overlap = PairwiseOverlap {
                    frame1: jp.source_frame.clone(),
                    frame2: jp.target_frame.clone(),
                    left_total: result["left_total"].as_u64().unwrap_or(0) as usize,
                    right_total: result["right_total"].as_u64().unwrap_or(0) as usize,
                    left_only: result["left_only"].as_u64().unwrap_or(0) as usize,
                    right_only: result["right_only"].as_u64().unwrap_or(0) as usize,
                    both: result["both"].as_u64().unwrap_or(0) as usize,
                    overlap_pct: result["overlap_pct"].as_f64().unwrap_or(0.0),
                };
                analyzer.add_overlap(overlap);
            }
            Err(e) => {
                return error_response(
                    StatusCode::INTERNAL_SERVER_ERROR,
                    &format!(
                        "Failed to compute overlap between {} and {}: {}",
                        jp.source_frame, jp.target_frame, e
                    ),
                );
            }
        }
    }

    // Compute data loss for each frame based on overlap zone
    // First, build a map of frame -> date column from the temporal ranges we collected
    let frame_date_columns: std::collections::HashMap<String, String> = req.frames.iter()
        .filter_map(|fc| {
            let date_col = match state.client.get_schema(&fc.frame) {
                Ok(schema) => {
                    let columns = schema["columns"].as_array();
                    fc.columns.iter().find(|col_name| {
                        columns.map_or(false, |cols| {
                            cols.iter().any(|c| {
                                let name = c["name"].as_str().unwrap_or("");
                                let dtype = c["type"].as_str().unwrap_or("").to_lowercase();
                                name == *col_name && (dtype.contains("date") || dtype.contains("timestamp"))
                            })
                        })
                    }).cloned()
                }
                Err(_) => None,
            };
            date_col.map(|col| (fc.frame.clone(), col))
        })
        .collect();

    if !frame_date_columns.is_empty() {
        // Compute overlap zone from all frames' date ranges
        let (overlap_start, overlap_end) = compute_overlap_bounds_auto(&req.frames, &state, &frame_date_columns);

        if let (Some(start), Some(end)) = (overlap_start, overlap_end) {
            if start <= end {
                for fc in &req.frames {
                    if let Some(date_col) = frame_date_columns.get(&fc.frame) {
                        match state.client.get_temporal_loss(&fc.frame, date_col, &start, &end) {
                            Ok(result) => {
                                let loss = FrameDataLoss {
                                    frame: fc.frame.clone(),
                                    rows_before_overlap: result["rows_before"].as_u64().unwrap_or(0) as usize,
                                    rows_after_overlap: result["rows_after"].as_u64().unwrap_or(0) as usize,
                                    total_lost: result["total_lost"].as_u64().unwrap_or(0) as usize,
                                    pct_lost: result["pct_lost"].as_f64().unwrap_or(0.0),
                                    range_lost_before: None,
                                    range_lost_after: None,
                                };
                                analyzer.add_data_loss(loss);
                            }
                            Err(e) => {
                                eprintln!("Warning: data loss calc failed for {}: {}", fc.frame, e);
                            }
                        }
                    }
                }
            }
        }
    }

    // Compute final coverage result
    let frame_names: Vec<String> = req.frames.iter().map(|f| f.frame.clone()).collect();
    match analyzer.compute_coverage(&frame_names) {
        Ok(result) => Json(result).into_response(),
        Err(e) => error_response(StatusCode::INTERNAL_SERVER_ERROR, &e.to_string()),
    }
}

fn compute_overlap_bounds_auto(
    frames: &[FrameConfig],
    state: &Arc<AppState>,
    frame_date_columns: &std::collections::HashMap<String, String>,
) -> (Option<String>, Option<String>) {
    let mut min_dates: Vec<String> = Vec::new();
    let mut max_dates: Vec<String> = Vec::new();

    for fc in frames {
        if let Some(date_col) = frame_date_columns.get(&fc.frame) {
            if let Ok(result) = state.client.get_temporal_range(&fc.frame, date_col, "day") {
                if let Some(min) = result["min_date"].as_str() {
                    min_dates.push(min.to_string());
                }
                if let Some(max) = result["max_date"].as_str() {
                    max_dates.push(max.to_string());
                }
            }
        }
    }

    let overlap_start = min_dates.iter().max().cloned();
    let overlap_end = max_dates.iter().min().cloned();

    (overlap_start, overlap_end)
}

fn error_response(status: StatusCode, msg: &str) -> axum::response::Response {
    (status, Json(json!({"error": msg}))).into_response()
}
