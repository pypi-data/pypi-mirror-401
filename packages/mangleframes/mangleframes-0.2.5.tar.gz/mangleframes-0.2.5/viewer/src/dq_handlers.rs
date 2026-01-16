//! HTTP handlers for DQX data quality operations.

use std::sync::Arc;

use axum::extract::{Path, State};
use axum::http::StatusCode;
use axum::response::IntoResponse;
use axum::Json;
use serde::Deserialize;
use serde_json::json;

use crate::web_server::AppState;

/// Check if DQX is available in the Python environment.
pub async fn dqx_available(State(state): State<Arc<AppState>>) -> impl IntoResponse {
    match state.client.dqx_available_async().await {
        Ok(result) => Json(result).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(json!({"error": e.to_string()})),
        )
            .into_response(),
    }
}

/// Profile a DataFrame to get suggested quality rules.
pub async fn profile_frame(
    State(state): State<Arc<AppState>>,
    Path(name): Path<String>,
) -> impl IntoResponse {
    match state.client.dq_profile(&name) {
        Ok(result) => Json(result).into_response(),
        Err(e) => {
            let status = if e.to_string().contains("not found") {
                StatusCode::NOT_FOUND
            } else {
                StatusCode::INTERNAL_SERVER_ERROR
            };
            (status, Json(json!({"error": e.to_string()}))).into_response()
        }
    }
}

#[derive(Deserialize)]
pub struct CheckRequest {
    rules: Vec<DQRuleInput>,
}

#[derive(Deserialize, serde::Serialize)]
pub struct DQRuleInput {
    name: Option<String>,
    check_func: String,
    column: Option<String>,
    criticality: Option<String>,
    #[serde(default)]
    check_func_kwargs: serde_json::Value,
}

/// Apply quality checks to a DataFrame.
pub async fn run_quality_checks(
    State(state): State<Arc<AppState>>,
    Path(name): Path<String>,
    Json(req): Json<CheckRequest>,
) -> impl IntoResponse {
    // Convert rules to JSON string for protocol
    let rules_json = match serde_json::to_string(&req.rules) {
        Ok(json) => json,
        Err(e) => {
            return (
                StatusCode::BAD_REQUEST,
                Json(json!({"error": format!("Invalid rules: {}", e)})),
            )
                .into_response()
        }
    };

    match state.client.dq_check(&name, &rules_json) {
        Ok(result) => Json(result).into_response(),
        Err(e) => {
            let status = if e.to_string().contains("not found") {
                StatusCode::NOT_FOUND
            } else {
                StatusCode::INTERNAL_SERVER_ERROR
            };
            (status, Json(json!({"error": e.to_string()}))).into_response()
        }
    }
}
