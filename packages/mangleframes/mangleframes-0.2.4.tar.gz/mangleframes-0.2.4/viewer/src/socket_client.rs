//! Unix socket client for communicating with Python DataFrame server.

use std::io::{Read, Write};
use std::os::unix::net::UnixStream;
use std::path::Path;

use thiserror::Error;

const STATUS_OK: u32 = 0;

#[derive(Error, Debug)]
pub enum ClientError {
    #[error("Connection failed: {0}")]
    Connection(#[from] std::io::Error),
    #[error("Server error: {0}")]
    ServerError(String),
    #[error("Invalid response format")]
    InvalidResponse,
    #[error("JSON parse error: {0}")]
    JsonParse(#[from] serde_json::Error),
}

pub struct FrameResponse {
    pub data: Vec<u8>,
    pub spark_ms: u64,
    pub ipc_ms: u64,
    pub total_rows: u64,
}

pub struct SocketClient {
    socket_path: std::path::PathBuf,
}

impl SocketClient {
    pub fn new(socket_path: &Path) -> Self {
        Self {
            socket_path: socket_path.to_path_buf(),
        }
    }

    fn send_command(&self, command: &str) -> Result<Vec<u8>, ClientError> {
        let mut stream = UnixStream::connect(&self.socket_path)?;

        // Avoid format! allocation - write command and newline directly
        stream.write_all(command.as_bytes())?;
        stream.write_all(b"\n")?;

        let mut header = [0u8; 8];
        stream.read_exact(&mut header)?;

        let status = u32::from_be_bytes([header[0], header[1], header[2], header[3]]);
        let length = u32::from_be_bytes([header[4], header[5], header[6], header[7]]) as usize;

        let mut payload = vec![0u8; length];
        stream.read_exact(&mut payload)?;

        if status != STATUS_OK {
            let msg = String::from_utf8_lossy(&payload).to_string();
            return Err(ClientError::ServerError(msg));
        }

        Ok(payload)
    }

    pub fn list_frames(&self) -> Result<Vec<String>, ClientError> {
        let payload = self.send_command("LIST")?;
        let names: Vec<String> = serde_json::from_slice(&payload)?;
        Ok(names)
    }

    pub fn get_schema(&self, name: &str) -> Result<serde_json::Value, ClientError> {
        let payload = self.send_command(&format!("SCHEMA:{}", name))?;
        let schema: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(schema)
    }

    pub fn get_frame(&self, name: &str, limit: usize) -> Result<FrameResponse, ClientError> {
        let payload = self.send_command(&format!("GET:{}:{}", name, limit))?;

        // 24-byte header: spark_ms, ipc_ms, total_rows (all little-endian u64)
        if payload.len() < 24 {
            return Err(ClientError::InvalidResponse);
        }

        let spark_ms = u64::from_le_bytes(payload[0..8].try_into().unwrap());
        let ipc_ms = u64::from_le_bytes(payload[8..16].try_into().unwrap());
        let total_rows = u64::from_le_bytes(payload[16..24].try_into().unwrap());
        let data = payload[24..].to_vec();

        Ok(FrameResponse { data, spark_ms, ipc_ms, total_rows })
    }

    pub fn get_stats(&self, name: &str) -> Result<serde_json::Value, ClientError> {
        let payload = self.send_command(&format!("STATS:{}", name))?;
        let stats: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(stats)
    }

    pub fn get_join_keys(&self, name: &str, columns: &[String]) -> Result<serde_json::Value, ClientError> {
        let cols = columns.join(",");
        let payload = self.send_command(&format!("JOIN_KEYS:{}:{}", name, cols))?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn get_join_temporal(
        &self,
        name: &str,
        column: &str,
        bucket: &str,
    ) -> Result<serde_json::Value, ClientError> {
        let payload = self.send_command(&format!("JOIN_TEMPORAL:{}:{}:{}", name, column, bucket))?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn get_join_overlap(
        &self,
        frame1: &str,
        frame2: &str,
        cols1: &[String],
        cols2: &[String],
    ) -> Result<serde_json::Value, ClientError> {
        let c1 = cols1.join(",");
        let c2 = cols2.join(",");
        let payload = self.send_command(&format!("JOIN_OVERLAP:{}:{}:{}:{}", frame1, frame2, c1, c2))?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn get_temporal_range(
        &self,
        name: &str,
        column: &str,
        granularity: &str,
    ) -> Result<serde_json::Value, ClientError> {
        let cmd = format!("TEMPORAL_RANGE:{}:{}:{}", name, column, granularity);
        let payload = self.send_command(&cmd)?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn get_temporal_loss(
        &self,
        name: &str,
        column: &str,
        overlap_start: &str,
        overlap_end: &str,
    ) -> Result<serde_json::Value, ClientError> {
        let cmd = format!("TEMPORAL_LOSS:{}:{}:{}:{}", name, column, overlap_start, overlap_end);
        let payload = self.send_command(&cmd)?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn dqx_available(&self) -> Result<serde_json::Value, ClientError> {
        let payload = self.send_command("DQX_AVAILABLE")?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn dq_profile(&self, name: &str) -> Result<serde_json::Value, ClientError> {
        let payload = self.send_command(&format!("DQ_PROFILE:{}", name))?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn dq_check(&self, name: &str, rules_json: &str) -> Result<serde_json::Value, ClientError> {
        let payload = self.send_command(&format!("DQ_CHECK:{}:{}", name, rules_json))?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn execute_sql(&self, sql: &str, limit: usize) -> Result<FrameResponse, ClientError> {
        let payload = self.send_command(&format!("SQL:{}:{}", limit, sql))?;

        if payload.len() < 24 {
            return Err(ClientError::InvalidResponse);
        }

        let spark_ms = u64::from_le_bytes(payload[0..8].try_into().unwrap());
        let ipc_ms = u64::from_le_bytes(payload[8..16].try_into().unwrap());
        let total_rows = u64::from_le_bytes(payload[16..24].try_into().unwrap());
        let data = payload[24..].to_vec();

        Ok(FrameResponse { data, spark_ms, ipc_ms, total_rows })
    }

    pub fn reconcile_aggregated(
        &self,
        source: &str,
        target: &str,
        config: &serde_json::Value,
    ) -> Result<serde_json::Value, ClientError> {
        let config_str = serde_json::to_string(config)?;
        let cmd = format!("RECONCILE_AGG:{}:{}:{}", source, target, config_str);
        let payload = self.send_command(&cmd)?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn analyze_join(
        &self,
        left: &str,
        right: &str,
        config: &serde_json::Value,
    ) -> Result<serde_json::Value, ClientError> {
        let config_str = serde_json::to_string(config)?;
        let cmd = format!("JOIN_ANALYZE:{}:{}:{}", left, right, config_str);
        let payload = self.send_command(&cmd)?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }

    pub fn get_join_unmatched(
        &self,
        left: &str,
        right: &str,
        config: &serde_json::Value,
    ) -> Result<serde_json::Value, ClientError> {
        let config_str = serde_json::to_string(config)?;
        let cmd = format!("JOIN_UNMATCHED:{}:{}:{}", left, right, config_str);
        let payload = self.send_command(&cmd)?;
        let result: serde_json::Value = serde_json::from_slice(&payload)?;
        Ok(result)
    }
}

// Async wrappers using spawn_blocking to avoid blocking the Tokio runtime.
// These should be used from async handlers instead of the sync methods above.
impl SocketClient {
    pub async fn list_frames_async(
        self: &std::sync::Arc<Self>,
    ) -> Result<Vec<String>, ClientError> {
        let client = self.clone();
        tokio::task::spawn_blocking(move || client.list_frames())
            .await
            .map_err(|e| ClientError::ServerError(e.to_string()))?
    }

    pub async fn get_schema_async(
        self: &std::sync::Arc<Self>,
        name: String,
    ) -> Result<serde_json::Value, ClientError> {
        let client = self.clone();
        tokio::task::spawn_blocking(move || client.get_schema(&name))
            .await
            .map_err(|e| ClientError::ServerError(e.to_string()))?
    }

    pub async fn get_frame_async(
        self: &std::sync::Arc<Self>,
        name: String,
        limit: usize,
    ) -> Result<FrameResponse, ClientError> {
        let client = self.clone();
        tokio::task::spawn_blocking(move || client.get_frame(&name, limit))
            .await
            .map_err(|e| ClientError::ServerError(e.to_string()))?
    }

    pub async fn get_stats_async(
        self: &std::sync::Arc<Self>,
        name: String,
    ) -> Result<serde_json::Value, ClientError> {
        let client = self.clone();
        tokio::task::spawn_blocking(move || client.get_stats(&name))
            .await
            .map_err(|e| ClientError::ServerError(e.to_string()))?
    }

    pub async fn execute_sql_async(
        self: &std::sync::Arc<Self>,
        sql: String,
        limit: usize,
    ) -> Result<FrameResponse, ClientError> {
        let client = self.clone();
        tokio::task::spawn_blocking(move || client.execute_sql(&sql, limit))
            .await
            .map_err(|e| ClientError::ServerError(e.to_string()))?
    }

    pub async fn dqx_available_async(
        self: &std::sync::Arc<Self>,
    ) -> Result<serde_json::Value, ClientError> {
        let client = self.clone();
        tokio::task::spawn_blocking(move || client.dqx_available())
            .await
            .map_err(|e| ClientError::ServerError(e.to_string()))?
    }
}
