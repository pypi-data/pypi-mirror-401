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

use crate::socket_client::SocketClient;
use crate::web_server::AppState;

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

    if !args.no_browser {
        let url = format!("http://localhost:{}", args.port);
        info!("Opening browser at {}", url);
        let _ = webbrowser::open(&url);
    }

    info!("Starting web server on port {}", args.port);
    web_server::run(state, args.port).await
}
