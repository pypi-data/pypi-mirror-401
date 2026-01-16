//! Performance metrics collection and aggregation.

use std::collections::{HashMap, VecDeque};
use std::time::Instant;

use serde::Serialize;
use tokio::sync::RwLock;

const MAX_SAMPLES_PER_FRAME: usize = 1000;

#[derive(Clone)]
pub struct TimingSample {
    pub timestamp: Instant,
    pub rows: usize,
    pub bytes: usize,
    pub spark_ms: u64,
    pub ipc_ms: u64,
    pub socket_ms: u64,
    pub parse_ms: u64,
    pub json_ms: u64,
    pub total_ms: u64,
    pub cached: bool,
}

#[derive(Serialize)]
pub struct FrameMetrics {
    pub sample_count: usize,
    pub rows_per_sec: f64,
    pub bytes_per_sec: f64,
    pub latency_p50_ms: u64,
    pub latency_p95_ms: u64,
    pub latency_p99_ms: u64,
    pub avg_spark_ms: f64,
    pub avg_ipc_ms: f64,
    pub avg_socket_ms: f64,
    pub avg_parse_ms: f64,
    pub avg_json_ms: f64,
    pub cache_hit_rate: f64,
}

#[derive(Serialize)]
pub struct GlobalMetrics {
    pub total_requests: usize,
    pub uptime_seconds: u64,
}

pub struct PerfCollector {
    samples: RwLock<HashMap<String, VecDeque<TimingSample>>>,
    start_time: Instant,
    total_requests: RwLock<usize>,
}

impl PerfCollector {
    pub fn new() -> Self {
        Self {
            samples: RwLock::new(HashMap::new()),
            start_time: Instant::now(),
            total_requests: RwLock::new(0),
        }
    }

    pub async fn record(&self, frame_name: &str, sample: TimingSample) {
        let mut samples = self.samples.write().await;
        let frame_samples = samples.entry(frame_name.to_string()).or_default();

        if frame_samples.len() >= MAX_SAMPLES_PER_FRAME {
            frame_samples.pop_front();
        }
        frame_samples.push_back(sample);

        let mut total = self.total_requests.write().await;
        *total += 1;
    }

    pub async fn get_frame_metrics(&self, frame_name: &str) -> Option<FrameMetrics> {
        let samples = self.samples.read().await;
        let frame_samples = samples.get(frame_name)?;

        if frame_samples.is_empty() {
            return None;
        }

        Some(compute_metrics(frame_samples))
    }

    pub async fn get_all_metrics(&self) -> HashMap<String, FrameMetrics> {
        let samples = self.samples.read().await;
        samples
            .iter()
            .filter_map(|(name, s)| {
                if s.is_empty() {
                    None
                } else {
                    Some((name.clone(), compute_metrics(s)))
                }
            })
            .collect()
    }

    pub async fn get_global_metrics(&self) -> GlobalMetrics {
        let total = *self.total_requests.read().await;
        GlobalMetrics {
            total_requests: total,
            uptime_seconds: self.start_time.elapsed().as_secs(),
        }
    }

    pub async fn clear(&self) {
        self.samples.write().await.clear();
        *self.total_requests.write().await = 0;
    }
}

fn compute_metrics(samples: &VecDeque<TimingSample>) -> FrameMetrics {
    let count = samples.len();
    let non_cached: Vec<_> = samples.iter().filter(|s| !s.cached).collect();
    let cached_count = count - non_cached.len();

    // Compute averages from non-cached samples
    let (avg_spark, avg_ipc, avg_socket, avg_parse, avg_json) = if non_cached.is_empty() {
        (0.0, 0.0, 0.0, 0.0, 0.0)
    } else {
        let n = non_cached.len() as f64;
        (
            non_cached.iter().map(|s| s.spark_ms as f64).sum::<f64>() / n,
            non_cached.iter().map(|s| s.ipc_ms as f64).sum::<f64>() / n,
            non_cached.iter().map(|s| s.socket_ms as f64).sum::<f64>() / n,
            non_cached.iter().map(|s| s.parse_ms as f64).sum::<f64>() / n,
            non_cached.iter().map(|s| s.json_ms as f64).sum::<f64>() / n,
        )
    };

    // Compute latency percentiles from all samples
    let mut latencies: Vec<u64> = samples.iter().map(|s| s.total_ms).collect();
    latencies.sort_unstable();

    let p50 = percentile(&latencies, 50);
    let p95 = percentile(&latencies, 95);
    let p99 = percentile(&latencies, 99);

    // Compute throughput from non-cached samples
    let (rows_per_sec, bytes_per_sec) = if non_cached.is_empty() {
        (0.0, 0.0)
    } else {
        let total_rows: usize = non_cached.iter().map(|s| s.rows).sum();
        let total_bytes: usize = non_cached.iter().map(|s| s.bytes).sum();
        let total_ms: u64 = non_cached.iter().map(|s| s.total_ms).sum();
        let total_secs = total_ms as f64 / 1000.0;
        if total_secs > 0.0 {
            (total_rows as f64 / total_secs, total_bytes as f64 / total_secs)
        } else {
            (0.0, 0.0)
        }
    };

    FrameMetrics {
        sample_count: count,
        rows_per_sec,
        bytes_per_sec,
        latency_p50_ms: p50,
        latency_p95_ms: p95,
        latency_p99_ms: p99,
        avg_spark_ms: avg_spark,
        avg_ipc_ms: avg_ipc,
        avg_socket_ms: avg_socket,
        avg_parse_ms: avg_parse,
        avg_json_ms: avg_json,
        cache_hit_rate: cached_count as f64 / count as f64,
    }
}

fn percentile(sorted: &[u64], p: usize) -> u64 {
    if sorted.is_empty() {
        return 0;
    }
    let idx = (p * sorted.len() / 100).min(sorted.len() - 1);
    sorted[idx]
}
