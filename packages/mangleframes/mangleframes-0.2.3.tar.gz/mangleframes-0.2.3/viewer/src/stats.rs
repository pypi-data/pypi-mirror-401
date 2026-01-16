//! Statistics computation for DataFrame columns.

use arrow::array::Array;
use arrow::datatypes::DataType;
use arrow::record_batch::RecordBatch;
use serde_json::{json, Value};

pub fn compute_stats(batches: &[RecordBatch]) -> Value {
    if batches.is_empty() {
        return json!({"columns": []});
    }

    let schema = batches[0].schema();
    let total_rows: usize = batches.iter().map(|b| b.num_rows()).sum();

    let columns: Vec<Value> = schema
        .fields()
        .iter()
        .enumerate()
        .map(|(col_idx, field)| {
            let mut null_count = 0usize;
            for batch in batches {
                null_count += batch.column(col_idx).null_count();
            }

            let mut stats = json!({
                "name": field.name(),
                "type": format!("{:?}", field.data_type()),
                "null_count": null_count,
                "non_null_count": total_rows - null_count,
            });

            if is_numeric(field.data_type()) {
                if let Some((min, max)) = compute_min_max(batches, col_idx) {
                    stats["min"] = json!(min);
                    stats["max"] = json!(max);
                }
            }

            stats
        })
        .collect();

    json!({
        "row_count": total_rows,
        "columns": columns
    })
}

fn is_numeric(dtype: &DataType) -> bool {
    matches!(
        dtype,
        DataType::Int8 | DataType::Int16 | DataType::Int32 | DataType::Int64
        | DataType::UInt8 | DataType::UInt16 | DataType::UInt32 | DataType::UInt64
        | DataType::Float32 | DataType::Float64
    )
}

fn compute_min_max(batches: &[RecordBatch], col_idx: usize) -> Option<(f64, f64)> {
    let mut min: Option<f64> = None;
    let mut max: Option<f64> = None;

    for batch in batches {
        let col = batch.column(col_idx);
        for i in 0..col.len() {
            if col.is_null(i) {
                continue;
            }
            if let Some(val) = extract_numeric(col.as_ref(), i) {
                min = Some(min.map_or(val, |m| m.min(val)));
                max = Some(max.map_or(val, |m| m.max(val)));
            }
        }
    }

    min.zip(max)
}

fn extract_numeric(array: &dyn Array, index: usize) -> Option<f64> {
    match array.data_type() {
        DataType::Int8 => {
            let arr = array.as_any().downcast_ref::<arrow::array::Int8Array>()?;
            Some(arr.value(index) as f64)
        }
        DataType::Int16 => {
            let arr = array.as_any().downcast_ref::<arrow::array::Int16Array>()?;
            Some(arr.value(index) as f64)
        }
        DataType::Int32 => {
            let arr = array.as_any().downcast_ref::<arrow::array::Int32Array>()?;
            Some(arr.value(index) as f64)
        }
        DataType::Int64 => {
            let arr = array.as_any().downcast_ref::<arrow::array::Int64Array>()?;
            Some(arr.value(index) as f64)
        }
        DataType::Float32 => {
            let arr = array.as_any().downcast_ref::<arrow::array::Float32Array>()?;
            Some(arr.value(index) as f64)
        }
        DataType::Float64 => {
            let arr = array.as_any().downcast_ref::<arrow::array::Float64Array>()?;
            Some(arr.value(index))
        }
        _ => None,
    }
}
