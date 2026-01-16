//! MangleFrames Viewer - Web-based PySpark DataFrame viewer.

mod arrow_reader;
mod dashboard;
mod dq_handlers;
mod export;
mod handlers;
mod history_analysis;
mod history_handlers;
mod join_handlers;
mod perf;
mod reconcile_handlers;
mod socket_client;
mod stats;
mod web_server;
mod websocket;

use std::path::PathBuf;
use std::sync::Arc;

use clap::Parser;
use tracing::info;
use tracing_subscriber::EnvFilter;

use std::time::Instant;

use crate::arrow_reader::batches_to_json_bytes;
use crate::socket_client::SocketClient;
use crate::web_server::{AppState, CachedFrame, JsonCacheEntry, JsonCacheKey};

#[derive(Parser)]
#[command(name = "mangleframes-viewer")]
#[command(about = "Web-based PySpark DataFrame viewer")]
struct Args {
    #[arg(short, long)]
    socket: PathBuf,

    #[arg(short, long, default_value = "8765")]
    port: u16,

    #[arg(long)]
    no_browser: bool,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::from_default_env())
        .init();

    let args = Args::parse();

    info!("Connecting to Python server at {:?}", args.socket);
    let client = Arc::new(SocketClient::new(&args.socket));
    let state = AppState::new(client.clone());

    // Spawn background preload task (non-blocking)
    let preload_state = state.clone();
    tokio::spawn(async move {
        preload_first_frame(preload_state).await;
    });

    if !args.no_browser {
        let url = format!("http://localhost:{}", args.port);
        info!("Opening browser at {}", url);
        let _ = webbrowser::open(&url);
    }

    info!("Starting web server on port {}", args.port);
    web_server::run(state, args.port).await
}

/// Preload first frame into cache in background for faster initial display.
async fn preload_first_frame(state: Arc<AppState>) {
    let frames = match state.client.list_frames_async().await {
        Ok(f) => f,
        Err(e) => {
            info!("Failed to list frames during preload: {}", e);
            mark_preload_complete(&state, None).await;
            return;
        }
    };

    let first = match frames.first() {
        Some(f) => f.clone(),
        None => {
            info!("No frames to preload");
            mark_preload_complete(&state, None).await;
            return;
        }
    };

    info!("Preloading frame: {}", first);
    if let Ok(response) = state.client.get_frame_async(first.clone(), 10000).await {
        if let Ok(batches) = arrow_reader::parse_arrow_stream(&response.data) {
            let common_limits = [100, 500, 1000, 5000, 10000];
            {
                let mut json_cache = state.json_cache.write().await;
                for &limit in &common_limits {
                    let (rows_bytes, _) = batches_to_json_bytes(&batches, 0, limit);
                    let total = batches.iter().map(|b| b.num_rows()).sum::<usize>();
                    let body = build_prewarm_response(&rows_bytes, total, 0, limit);
                    let key = JsonCacheKey { frame: first.clone(), offset: 0, limit };
                    json_cache.insert(key, JsonCacheEntry { data: body, created: Instant::now() });
                }
                info!("Pre-warmed JSON cache for {} limits", common_limits.len());
            }

            let mut cache = state.cache.write().await;
            cache.insert(first.clone(), CachedFrame { batches, stats: None, last_access: Instant::now() });
        }
    }

    mark_preload_complete(&state, Some(&first)).await;
}

/// Mark preload as complete and notify frontend via WebSocket.
async fn mark_preload_complete(state: &Arc<AppState>, frame: Option<&str>) {
    *state.preload_complete.write().await = true;

    let msg = match frame {
        Some(f) => format!(r#"{{"type":"preload_complete","frame":"{}"}}"#, f),
        None => r#"{"type":"preload_complete","frame":null}"#.to_string(),
    };
    let _ = state.broadcast_tx.send(msg);
    info!("Preload complete");
}

/// Build pre-warm response JSON (cached timing values are zeros)
fn build_prewarm_response(rows_bytes: &[u8], total: usize, offset: usize, limit: usize) -> Vec<u8> {
    let timing = r#"{"spark_ms":0,"ipc_ms":0,"socket_ms":0,"parse_ms":0,"json_ms":0,"total_ms":0,"rows_fetched":0,"bytes_transferred":0,"cached":true}"#;
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
