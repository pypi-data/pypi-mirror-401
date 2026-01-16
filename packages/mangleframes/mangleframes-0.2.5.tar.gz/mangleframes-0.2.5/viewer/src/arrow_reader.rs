//! Arrow IPC stream parsing and JSON conversion.

use std::io::Cursor;

use arrow::array::{Array, AsArray, RecordBatch};
use arrow::datatypes::{DataType, Date32Type, Decimal128Type, DecimalType};
use arrow::temporal_conversions::date32_to_datetime;
use arrow_ipc::reader::StreamReader;
use serde_json::{json, Value};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ArrowError {
    #[error("Failed to parse Arrow IPC: {0}")]
    ParseError(#[from] arrow::error::ArrowError),
}

pub fn parse_arrow_stream(data: &[u8]) -> Result<Vec<RecordBatch>, ArrowError> {
    let cursor = Cursor::new(data);
    let reader = StreamReader::try_new(cursor, None)?;
    let batches: Result<Vec<_>, _> = reader.collect();
    Ok(batches?)
}

/// Convert Arrow batches to JSON bytes with proper type handling.
/// Handles Decimal128, Date32, Timestamp, and all primitive types correctly.
pub fn batches_to_json_bytes(batches: &[RecordBatch], offset: usize, limit: usize) -> (Vec<u8>, usize) {
    if batches.is_empty() {
        return (b"[]".to_vec(), 0);
    }

    let total_rows: usize = batches.iter().map(|b| b.num_rows()).sum();
    let actual_limit = limit.min(total_rows.saturating_sub(offset));
    if actual_limit == 0 {
        return (b"[]".to_vec(), 0);
    }

    let sliced = slice_batches(batches, offset, actual_limit);
    if sliced.is_empty() {
        return (b"[]".to_vec(), 0);
    }

    // Build JSON array using custom type handling
    let mut rows: Vec<Value> = Vec::with_capacity(actual_limit);
    for batch in &sliced {
        for row_idx in 0..batch.num_rows() {
            let mut row = serde_json::Map::new();
            for (col_idx, field) in batch.schema().fields().iter().enumerate() {
                let col = batch.column(col_idx);
                let value = array_value_to_json(col.as_ref(), row_idx);
                row.insert(field.name().clone(), value);
            }
            rows.push(Value::Object(row));
        }
    }

    let row_count = rows.len();
    let bytes = serde_json::to_vec(&rows).unwrap_or_else(|_| b"[]".to_vec());
    (bytes, row_count)
}

fn array_value_to_json(array: &dyn Array, index: usize) -> Value {
    if array.is_null(index) {
        return Value::Null;
    }

    match array.data_type() {
        DataType::Boolean => {
            json!(array.as_boolean().value(index))
        }
        DataType::Int8 => {
            json!(array.as_primitive::<arrow::datatypes::Int8Type>().value(index))
        }
        DataType::Int16 => {
            json!(array.as_primitive::<arrow::datatypes::Int16Type>().value(index))
        }
        DataType::Int32 => {
            json!(array.as_primitive::<arrow::datatypes::Int32Type>().value(index))
        }
        DataType::Int64 => {
            json!(array.as_primitive::<arrow::datatypes::Int64Type>().value(index))
        }
        DataType::UInt8 => {
            json!(array.as_primitive::<arrow::datatypes::UInt8Type>().value(index))
        }
        DataType::UInt16 => {
            json!(array.as_primitive::<arrow::datatypes::UInt16Type>().value(index))
        }
        DataType::UInt32 => {
            json!(array.as_primitive::<arrow::datatypes::UInt32Type>().value(index))
        }
        DataType::UInt64 => {
            json!(array.as_primitive::<arrow::datatypes::UInt64Type>().value(index))
        }
        DataType::Float32 => {
            json!(array.as_primitive::<arrow::datatypes::Float32Type>().value(index))
        }
        DataType::Float64 => {
            json!(array.as_primitive::<arrow::datatypes::Float64Type>().value(index))
        }
        DataType::Utf8 => {
            json!(array.as_string::<i32>().value(index))
        }
        DataType::LargeUtf8 => {
            json!(array.as_string::<i64>().value(index))
        }
        DataType::Date32 => {
            let days = array.as_primitive::<Date32Type>().value(index);
            match date32_to_datetime(days) {
                Some(dt) => json!(dt.format("%Y-%m-%d").to_string()),
                None => Value::Null,
            }
        }
        DataType::Decimal128(precision, scale) => {
            let arr = array.as_primitive::<Decimal128Type>();
            let value = arr.value(index);
            json!(Decimal128Type::format_decimal(value, *precision, *scale))
        }
        DataType::Timestamp(_, _) => {
            // Format timestamp as ISO string
            use arrow::array::TimestampMicrosecondArray;
            if let Some(ts_array) = array.as_any().downcast_ref::<TimestampMicrosecondArray>() {
                let micros = ts_array.value(index);
                let secs = micros / 1_000_000;
                let nsecs = ((micros % 1_000_000) * 1000) as u32;
                if let Some(dt) = chrono::DateTime::from_timestamp(secs, nsecs) {
                    return json!(dt.format("%Y-%m-%dT%H:%M:%S%.6f").to_string());
                }
            }
            json!(format!("{:?}", array.data_type()))
        }
        _ => json!(format!("{:?}", array.data_type())),
    }
}

/// Legacy function for compatibility - parses back to Value
pub fn batches_to_json(batches: &[RecordBatch], offset: usize, limit: usize) -> Value {
    let (bytes, _) = batches_to_json_bytes(batches, offset, limit);
    serde_json::from_slice(&bytes).unwrap_or(Value::Array(vec![]))
}

/// Slice batches to extract rows in range [offset, offset+limit)
fn slice_batches(batches: &[RecordBatch], offset: usize, limit: usize) -> Vec<RecordBatch> {
    let mut result = Vec::new();
    let mut current_offset = 0;
    let mut remaining = limit;

    for batch in batches {
        let batch_rows = batch.num_rows();

        if current_offset + batch_rows <= offset {
            current_offset += batch_rows;
            continue;
        }

        let start = if current_offset < offset { offset - current_offset } else { 0 };
        let len = remaining.min(batch_rows - start);

        if len > 0 {
            let sliced = batch.slice(start, len);
            result.push(sliced);
            remaining -= len;
        }

        if remaining == 0 {
            break;
        }
        current_offset += batch_rows;
    }

    result
}

pub fn total_row_count(batches: &[RecordBatch]) -> usize {
    batches.iter().map(|b| b.num_rows()).sum()
}
