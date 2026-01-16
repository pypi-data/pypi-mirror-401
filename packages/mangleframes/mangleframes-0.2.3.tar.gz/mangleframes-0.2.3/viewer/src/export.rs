//! Export DataFrame to various formats.

use arrow::record_batch::RecordBatch;
use arrow_csv::WriterBuilder as CsvWriterBuilder;
use arrow_json::LineDelimitedWriter;
use parquet::arrow::ArrowWriter;
use parquet::basic::Compression;
use parquet::file::properties::WriterProperties;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ExportError {
    #[error("Arrow error: {0}")]
    Arrow(#[from] arrow::error::ArrowError),
    #[error("Parquet error: {0}")]
    Parquet(#[from] parquet::errors::ParquetError),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("No data to export")]
    NoData,
}

pub fn to_csv(batches: &[RecordBatch]) -> Result<Vec<u8>, ExportError> {
    if batches.is_empty() {
        return Err(ExportError::NoData);
    }

    let mut buffer = Vec::new();
    let mut writer = CsvWriterBuilder::new()
        .with_header(true)
        .build(&mut buffer);

    for batch in batches {
        writer.write(batch)?;
    }

    drop(writer);
    Ok(buffer)
}

pub fn to_json(batches: &[RecordBatch]) -> Result<Vec<u8>, ExportError> {
    if batches.is_empty() {
        return Err(ExportError::NoData);
    }

    let mut buffer = Vec::new();
    let mut writer = LineDelimitedWriter::new(&mut buffer);

    for batch in batches {
        writer.write(batch)?;
    }

    writer.finish()?;
    Ok(buffer)
}

pub fn to_parquet(batches: &[RecordBatch]) -> Result<Vec<u8>, ExportError> {
    if batches.is_empty() {
        return Err(ExportError::NoData);
    }

    let schema = batches[0].schema();
    let mut buffer = Vec::new();

    let props = WriterProperties::builder()
        .set_compression(Compression::SNAPPY)
        .build();

    let mut writer = ArrowWriter::try_new(&mut buffer, schema, Some(props))?;

    for batch in batches {
        writer.write(batch)?;
    }

    writer.close()?;
    Ok(buffer)
}
