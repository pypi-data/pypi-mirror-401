"""Protocol handlers for DataFrame server commands."""
from __future__ import annotations

import json
import struct
import threading
import time
from decimal import Decimal
from typing import TYPE_CHECKING, Any

import pyarrow as pa
from pyspark.sql import functions as F

if TYPE_CHECKING:
    from pyspark.sql import DataFrame

# DQX availability detection
try:
    from databricks.sdk import WorkspaceClient
    from databricks.labs.dqx.engine import DQEngine
    from databricks.labs.dqx.profiler.profiler import DQProfiler
    from databricks.labs.dqx.profiler.generator import DQGenerator
    from databricks.labs.dqx.checks_serializer import deserialize_checks
    HAS_DQX = True
except ImportError:
    HAS_DQX = False

STATUS_OK = 0
STATUS_ERROR = 1

# Cache for computed stats (cleared when DataFrame is re-registered)
_stats_cache: dict[str, dict] = {}

# Cache for prefetched Arrow data: name -> (limit, payload_bytes)
_arrow_cache: dict[str, tuple[int, bytes]] = {}
_arrow_cache_lock = threading.Lock()


def clear_stats_cache(name: str | None = None) -> None:
    """Clear cached stats for a DataFrame or all DataFrames."""
    if name is None:
        _stats_cache.clear()
    elif name in _stats_cache:
        del _stats_cache[name]


def clear_arrow_cache(name: str | None = None) -> None:
    """Clear cached Arrow data for a DataFrame or all DataFrames."""
    with _arrow_cache_lock:
        if name is None:
            _arrow_cache.clear()
        elif name in _arrow_cache:
            del _arrow_cache[name]


def _serialize_arrow_ipc(table: pa.Table) -> tuple[bytes, int]:
    """Serialize Arrow table to IPC format, returning bytes and timing in ms."""
    start = time.perf_counter()
    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchStreamWriter(sink, table.schema) as writer:
        for batch in table.to_batches():
            writer.write_batch(batch)
    ipc_ms = int((time.perf_counter() - start) * 1000)
    return sink.getvalue().to_pybytes(), ipc_ms


def encode_response(status: int, payload: bytes) -> bytes:
    """Encode response with status and length prefix."""
    return struct.pack(">II", status, len(payload)) + payload


def encode_json_response(data: Any) -> bytes:
    """Encode JSON data as successful response."""
    return encode_response(STATUS_OK, json.dumps(data).encode("utf-8"))


def encode_error(message: str) -> bytes:
    """Encode error message response."""
    return encode_response(STATUS_ERROR, message.encode("utf-8"))


def handle_list(registry: dict[str, DataFrame]) -> bytes:
    """Return list of registered DataFrame names."""
    return encode_json_response(list(registry.keys()))


def handle_schema(registry: dict[str, DataFrame], name: str) -> bytes:
    """Return schema of a DataFrame as JSON."""
    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    df = registry[name]
    columns = [
        {"name": field.name, "type": str(field.dataType), "nullable": field.nullable}
        for field in df.schema.fields
    ]
    return encode_json_response({"name": name, "columns": columns})


def handle_get(registry: dict[str, DataFrame], name: str, limit: int) -> bytes:
    """Return DataFrame data as Arrow IPC stream with timing info."""
    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    # Check cache first - return cached data if limit is sufficient
    # limit=0 means "fetch all rows", so bypass cache in that case
    with _arrow_cache_lock:
        if name in _arrow_cache and limit > 0:
            cached_limit, cached_payload = _arrow_cache[name]
            if cached_limit >= limit:
                return encode_response(STATUS_OK, cached_payload)

    # Cache miss or insufficient limit - materialize from Spark
    df = registry[name]

    start = time.perf_counter()
    limited_df = df.limit(limit) if limit > 0 else df
    table = limited_df.toArrow()
    spark_ms = int((time.perf_counter() - start) * 1000)
    total_rows = table.num_rows

    arrow_bytes, ipc_ms = _serialize_arrow_ipc(table)
    # 24-byte header: spark_ms, ipc_ms, total_rows (all little-endian u64)
    payload = struct.pack("<QQQ", spark_ms, ipc_ms, total_rows) + arrow_bytes

    # Cache result for future requests
    with _arrow_cache_lock:
        _arrow_cache[name] = (limit, payload)

    return encode_response(STATUS_OK, payload)


def _is_numeric_type(dtype_str: str) -> bool:
    """Check if a Spark type string represents a numeric type."""
    dtype_lower = dtype_str.lower()
    return any(t in dtype_lower for t in ["int", "long", "double", "float", "decimal"])


def _is_temporal_type(dtype_str: str) -> bool:
    """Check if a Spark type string represents a temporal type."""
    dtype_lower = dtype_str.lower()
    return any(t in dtype_lower for t in ["date", "timestamp"])


def handle_stats(registry: dict[str, DataFrame], name: str) -> bytes:
    """Return basic statistics for a DataFrame using single aggregation."""
    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    # Return cached stats if available
    if name in _stats_cache:
        return encode_json_response(_stats_cache[name])

    df = registry[name]
    fields = df.schema.fields

    # Build all aggregation expressions in one pass
    agg_exprs = [F.count(F.lit(1)).alias("__total")]
    for field in fields:
        col_name = field.name
        agg_exprs.append(
            F.sum(F.when(F.col(col_name).isNull(), 1).otherwise(0)).alias(f"{col_name}__nulls")
        )
        if _is_numeric_type(str(field.dataType)):
            agg_exprs.append(F.min(col_name).alias(f"{col_name}__min"))
            agg_exprs.append(F.max(col_name).alias(f"{col_name}__max"))

    # Single Spark action
    result = df.agg(*agg_exprs).collect()[0]
    row_count = result["__total"]

    # Extract stats from result
    column_stats = []
    for field in fields:
        col_name = field.name
        dtype_str = str(field.dataType)
        stats = {"name": col_name, "type": dtype_str, "nullable": field.nullable}
        stats["null_count"] = result[f"{col_name}__nulls"] or 0

        if _is_numeric_type(dtype_str):
            min_val = result[f"{col_name}__min"]
            max_val = result[f"{col_name}__max"]
            stats["min"] = str(min_val) if min_val is not None else None
            stats["max"] = str(max_val) if max_val is not None else None

        column_stats.append(stats)

    stats_data = {"name": name, "row_count": row_count, "columns": column_stats}
    _stats_cache[name] = stats_data  # Cache for future requests

    return encode_json_response(stats_data)


def handle_count(registry: dict[str, DataFrame], name: str) -> bytes:
    """Return total row count without transferring data."""
    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    df = registry[name]
    start = time.perf_counter()
    count = df.count()
    count_ms = int((time.perf_counter() - start) * 1000)

    return encode_json_response({"name": name, "count": count, "count_ms": count_ms})


def handle_join_keys(registry: dict[str, DataFrame], name: str, columns: list[str]) -> bytes:
    """Return key statistics for join analysis."""
    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    df = registry[name]
    for col in columns:
        if col not in [f.name for f in df.schema.fields]:
            return encode_error(f"Column '{col}' not found in '{name}'")

    if len(columns) == 1:
        key_expr = F.col(columns[0])
    else:
        key_expr = F.struct(*[F.col(c) for c in columns])

    start = time.perf_counter()
    result = df.agg(
        F.countDistinct(key_expr).alias("cardinality"),
        F.sum(F.when(key_expr.isNull(), 1).otherwise(0)).alias("null_count"),
        F.count(F.lit(1)).alias("total_rows")
    ).collect()[0]
    compute_ms = int((time.perf_counter() - start) * 1000)

    return encode_json_response({
        "frame": name,
        "columns": columns,
        "cardinality": result["cardinality"],
        "null_count": result["null_count"] or 0,
        "total_rows": result["total_rows"],
        "compute_ms": compute_ms
    })


def handle_join_temporal(
    registry: dict[str, DataFrame], name: str, column: str, bucket: str
) -> bytes:
    """Return temporal distribution for join coverage analysis."""
    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    df = registry[name]
    if column not in [f.name for f in df.schema.fields]:
        return encode_error(f"Column '{column}' not found in '{name}'")

    field = next(f for f in df.schema.fields if f.name == column)
    if not _is_temporal_type(str(field.dataType)):
        return encode_error(f"Column '{column}' is not a temporal type")

    if bucket not in ("day", "week", "month"):
        return encode_error(f"Invalid bucket: {bucket}. Use day, week, or month")

    start = time.perf_counter()
    truncated = df.withColumn("__bucket", F.date_trunc(bucket, F.col(column)))
    buckets_df = truncated.groupBy("__bucket").agg(F.count(F.lit(1)).alias("count"))
    bucket_rows = buckets_df.orderBy("__bucket").collect()
    compute_ms = int((time.perf_counter() - start) * 1000)

    min_max = df.agg(
        F.min(column).alias("min_val"),
        F.max(column).alias("max_val")
    ).collect()[0]

    buckets = {}
    for row in bucket_rows:
        if row["__bucket"] is not None:
            bucket_key = str(row["__bucket"])[:10]
            buckets[bucket_key] = row["count"]

    return encode_json_response({
        "frame": name,
        "column": column,
        "bucket_size": bucket,
        "min": str(min_max["min_val"]) if min_max["min_val"] else None,
        "max": str(min_max["max_val"]) if min_max["max_val"] else None,
        "buckets": buckets,
        "compute_ms": compute_ms
    })


def _generate_expected_buckets(min_date: str, max_date: str, granularity: str) -> list[str]:
    """Generate all expected bucket keys between min and max dates."""
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta

    start = datetime.strptime(min_date[:10], "%Y-%m-%d")
    end = datetime.strptime(max_date[:10], "%Y-%m-%d")
    buckets = []

    if granularity == "day":
        current = start
        while current <= end:
            buckets.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
    elif granularity == "week":
        current = start - timedelta(days=start.weekday())
        end_aligned = end - timedelta(days=end.weekday())
        while current <= end_aligned:
            buckets.append(current.strftime("%Y-%m-%d"))
            current += timedelta(weeks=1)
    elif granularity == "month":
        current = start.replace(day=1)
        end_aligned = end.replace(day=1)
        while current <= end_aligned:
            buckets.append(current.strftime("%Y-%m-%d"))
            current += relativedelta(months=1)

    return buckets


def _find_gaps(expected: list[str], actual: set[str]) -> list[dict]:
    """Find contiguous ranges of missing buckets."""
    gaps = []
    gap_start = None
    gap_count = 0

    for bucket in expected:
        if bucket not in actual:
            if gap_start is None:
                gap_start = bucket
                gap_count = 1
            else:
                gap_count += 1
        else:
            if gap_start is not None:
                gaps.append({
                    "start": gap_start,
                    "end": expected[expected.index(gap_start) + gap_count - 1],
                    "periods": gap_count
                })
                gap_start = None
                gap_count = 0

    if gap_start is not None:
        gaps.append({
            "start": gap_start,
            "end": expected[expected.index(gap_start) + gap_count - 1],
            "periods": gap_count
        })

    return gaps


def handle_temporal_range(
    registry: dict[str, DataFrame], name: str, column: str, granularity: str
) -> bytes:
    """Return detailed temporal range statistics for a frame."""
    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    df = registry[name]
    if column not in [f.name for f in df.schema.fields]:
        return encode_error(f"Column '{column}' not found in '{name}'")

    field = next(f for f in df.schema.fields if f.name == column)
    if not _is_temporal_type(str(field.dataType)):
        return encode_error(f"Column '{column}' is not a temporal type")

    if granularity not in ("day", "week", "month"):
        return encode_error(f"Invalid granularity: {granularity}")

    start_time = time.perf_counter()

    agg_result = df.agg(
        F.min(column).alias("min_date"),
        F.max(column).alias("max_date"),
        F.count(F.lit(1)).alias("total_rows"),
        F.sum(F.when(F.col(column).isNull(), 1).otherwise(0)).alias("null_dates"),
        F.countDistinct(column).alias("distinct_dates")
    ).collect()[0]

    min_date = agg_result["min_date"]
    max_date = agg_result["max_date"]
    total_rows = agg_result["total_rows"]
    null_dates = agg_result["null_dates"] or 0
    distinct_dates = agg_result["distinct_dates"]

    internal_gaps = []
    if min_date and max_date:
        truncated = df.withColumn("__bucket", F.date_trunc(granularity, F.col(column)))
        bucket_rows = truncated.select("__bucket").distinct().collect()
        actual_buckets = {
            str(row["__bucket"])[:10] for row in bucket_rows if row["__bucket"]
        }
        expected = _generate_expected_buckets(str(min_date), str(max_date), granularity)
        internal_gaps = _find_gaps(expected, actual_buckets)

    compute_ms = int((time.perf_counter() - start_time) * 1000)

    return encode_json_response({
        "frame": name,
        "column": column,
        "granularity": granularity,
        "min_date": str(min_date)[:10] if min_date else None,
        "max_date": str(max_date)[:10] if max_date else None,
        "total_rows": total_rows,
        "null_dates": null_dates,
        "distinct_dates": distinct_dates,
        "internal_gaps": internal_gaps,
        "compute_ms": compute_ms
    })


def handle_temporal_loss(
    registry: dict[str, DataFrame],
    name: str, column: str,
    overlap_start: str, overlap_end: str
) -> bytes:
    """Return row counts outside the overlap zone."""
    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    df = registry[name]
    if column not in [f.name for f in df.schema.fields]:
        return encode_error(f"Column '{column}' not found in '{name}'")

    field = next(f for f in df.schema.fields if f.name == column)
    if not _is_temporal_type(str(field.dataType)):
        return encode_error(f"Column '{column}' is not a temporal type")

    start_time = time.perf_counter()

    result = df.agg(
        F.count(F.lit(1)).alias("total"),
        F.sum(F.when(F.col(column) < overlap_start, 1).otherwise(0)).alias("before"),
        F.sum(F.when(F.col(column) > overlap_end, 1).otherwise(0)).alias("after")
    ).collect()[0]

    total = result["total"]
    rows_before = result["before"] or 0
    rows_after = result["after"] or 0
    total_lost = rows_before + rows_after
    pct_lost = (total_lost / total * 100) if total > 0 else 0.0

    compute_ms = int((time.perf_counter() - start_time) * 1000)

    return encode_json_response({
        "frame": name,
        "rows_before": rows_before,
        "rows_after": rows_after,
        "total_lost": total_lost,
        "pct_lost": round(pct_lost, 2),
        "compute_ms": compute_ms
    })


def handle_dqx_available() -> bytes:
    """Return whether DQX is available."""
    return encode_json_response({"available": HAS_DQX})


def handle_dq_profile(registry: dict[str, DataFrame], name: str) -> bytes:
    """Profile a DataFrame and return suggested quality rules."""
    if not HAS_DQX:
        return encode_error("DQX not installed. Install with: pip install databricks-labs-dqx")

    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    df = registry[name]
    start = time.perf_counter()

    try:
        ws = WorkspaceClient()
        profiler = DQProfiler(ws)
        summary_stats, profiles = profiler.profile(df)
        generator = DQGenerator(ws)
        suggested_rules = generator.generate_dq_rules(profiles)
        compute_ms = int((time.perf_counter() - start) * 1000)

        # summary_stats is already a dict from DQProfiler.profile()
        stats_list = summary_stats if summary_stats is not None else {}

        # Convert DQX rule dicts to frontend-expected flat structure
        rules_list = []
        for rule in suggested_rules:
            check = rule.get("check", {})
            args = check.get("arguments", {})
            col = args.get("column") or args.get("col_name") or (args.get("col_names", [None])[0])
            kwargs = {k: v for k, v in args.items() if k not in ("column", "col_name", "col_names")}
            rules_list.append({
                "name": rule.get("name", f"{check.get('function', 'check')}_{col or 'all'}"),
                "check_func": check.get("function"),
                "column": col,
                "criticality": rule.get("criticality", "error"),
                "check_func_kwargs": kwargs
            })

        return encode_json_response({
            "frame": name,
            "summary_stats": _serialize_for_json(stats_list),
            "suggested_rules": _serialize_for_json(rules_list),
            "compute_ms": compute_ms
        })
    except Exception as e:
        return encode_error(f"Profiling failed: {str(e)}")


def handle_dq_check(registry: dict[str, DataFrame], name: str, rules_json: str) -> bytes:
    """Apply DQX quality checks to a DataFrame."""
    if not HAS_DQX:
        return encode_error("DQX not installed. Install with: pip install databricks-labs-dqx")

    if name not in registry:
        return encode_error(f"DataFrame '{name}' not found")

    df = registry[name]
    start = time.perf_counter()

    try:
        rules_data = json.loads(rules_json)
        if not isinstance(rules_data, list):
            return encode_error("Rules must be a JSON array")

        # Convert frontend format to DQX dictionary format
        dqx_rules_data = []
        for r in rules_data:
            args = r.get("check_func_kwargs", {}).copy()
            if r.get("column"):
                args["column"] = r["column"]
            dqx_rule = {
                "name": r.get("name", f"check_{len(dqx_rules_data)}"),
                "criticality": r.get("criticality", "error"),
                "check": {
                    "function": r["check_func"],
                    "arguments": args
                }
            }
            dqx_rules_data.append(dqx_rule)

        dq_rules = deserialize_checks(dqx_rules_data)

        ws = WorkspaceClient()
        engine = DQEngine(ws)
        result_df = engine.apply_checks(df, dq_rules)

        # Get error/warning columns
        error_col = "_error"
        warning_col = "_warning"

        # Collect results with error/warning info
        result_rows = result_df.limit(1000).collect()
        compute_ms = int((time.perf_counter() - start) * 1000)

        # Build response with row-level errors/warnings
        rows_data = []
        error_summary = {}
        warning_summary = {}

        for idx, row in enumerate(result_rows):
            row_dict = row.asDict()
            errors = row_dict.pop(error_col, None) or []
            warnings = row_dict.pop(warning_col, None) or []

            # Convert to serializable format
            row_errors = []
            for err in errors:
                err_dict = err.asDict() if hasattr(err, "asDict") else dict(err)
                row_errors.append(err_dict)
                col = err_dict.get("columns", ["unknown"])[0] if err_dict.get("columns") else "unknown"
                error_summary[col] = error_summary.get(col, 0) + 1

            row_warnings = []
            for warn in warnings:
                warn_dict = warn.asDict() if hasattr(warn, "asDict") else dict(warn)
                row_warnings.append(warn_dict)
                col = warn_dict.get("columns", ["unknown"])[0] if warn_dict.get("columns") else "unknown"
                warning_summary[col] = warning_summary.get(col, 0) + 1

            rows_data.append({
                "row_index": idx,
                "data": {k: _serialize_value(v) for k, v in row_dict.items()},
                "errors": row_errors,
                "warnings": row_warnings
            })

        return encode_json_response({
            "frame": name,
            "rows": rows_data,
            "total_rows": len(rows_data),
            "error_summary": error_summary,
            "warning_summary": warning_summary,
            "compute_ms": compute_ms
        })
    except json.JSONDecodeError as e:
        return encode_error(f"Invalid JSON: {str(e)}")
    except Exception as e:
        return encode_error(f"Quality check failed: {str(e)}")


def _serialize_value(val: Any) -> Any:
    """Convert Spark/Python values to JSON-serializable format."""
    if val is None:
        return None
    if isinstance(val, (str, int, float, bool)):
        return val
    if isinstance(val, Decimal):
        return float(val)
    if hasattr(val, "isoformat"):
        return val.isoformat()
    return str(val)


def _serialize_for_json(obj: Any) -> Any:
    """Recursively convert nested structures to JSON-serializable format."""
    if isinstance(obj, dict):
        return {k: _serialize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize_for_json(item) for item in obj]
    return _serialize_value(obj)


def handle_sql(registry: dict[str, DataFrame], sql: str, limit: int) -> bytes:
    """Execute SQL query via Spark SQL and return results as Arrow IPC."""
    import logging
    logging.info(f"Executing SQL query (limit={limit}): {sql[:100]}...")

    if not registry:
        return encode_error("No DataFrames registered")

    try:
        # Get SparkSession from any registered DataFrame
        spark = next(iter(registry.values())).sparkSession

        # Register all DataFrames as temp views
        for name, df in registry.items():
            df.createOrReplaceTempView(name)

        start = time.perf_counter()
        result_df = spark.sql(sql)
        if limit > 0:
            result_df = result_df.limit(limit)
        table = result_df.toArrow()
        spark_ms = int((time.perf_counter() - start) * 1000)
        total_rows = table.num_rows

        arrow_bytes, ipc_ms = _serialize_arrow_ipc(table)
        payload = struct.pack("<QQQ", spark_ms, ipc_ms, total_rows) + arrow_bytes

        logging.info(f"SQL query complete: {total_rows} rows in {spark_ms}ms")
        return encode_response(STATUS_OK, payload)
    except Exception as e:
        logging.error(f"SQL query failed: {e}")
        return encode_error(f"SQL execution failed: {str(e)}")


def _df_to_json_rows(df: "DataFrame", limit: int) -> list[dict]:
    """Convert DataFrame to list of JSON-serializable dicts."""
    rows = df.limit(limit).collect() if limit > 0 else df.collect()
    return [_serialize_for_json(row.asDict()) for row in rows]


def _build_agg_exprs(aggregations: list[dict]) -> list:
    """Build PySpark aggregation expressions from config."""
    agg_exprs = []
    for config in aggregations:
        col = config["column"]
        for agg_type in config["aggregations"]:
            alias = f"{col}_{agg_type.lower()}"
            if agg_type == "sum":
                agg_exprs.append(F.sum(col).alias(alias))
            elif agg_type == "count":
                agg_exprs.append(F.count(col).alias(alias))
            elif agg_type == "min":
                agg_exprs.append(F.min(col).alias(alias))
            elif agg_type == "max":
                agg_exprs.append(F.max(col).alias(alias))
            elif agg_type == "avg":
                agg_exprs.append(F.avg(col).alias(alias))
    return agg_exprs


def _compute_column_totals(
    source_agg: "DataFrame", target_agg: "DataFrame", aggregations: list[dict]
) -> list[dict]:
    """Compute column-level total comparisons."""
    results = []
    for config in aggregations:
        col = config["column"]
        for agg_type in config["aggregations"]:
            alias = f"{col}_{agg_type.lower()}"
            source_val = source_agg.agg(F.sum(alias)).collect()[0][0]
            target_val = target_agg.agg(F.sum(alias)).collect()[0][0]

            source_f = float(source_val) if source_val is not None else None
            target_f = float(target_val) if target_val is not None else None

            diff = None
            pct_diff = None
            if source_f is not None and target_f is not None:
                diff = source_f - target_f
                if abs(source_f) > 1e-9:
                    pct_diff = (diff / source_f) * 100

            results.append({
                "column": col,
                "aggregation": agg_type.upper(),
                "source_total": source_f,
                "target_total": target_f,
                "difference": diff,
                "percent_diff": pct_diff
            })
    return results


def handle_reconcile_aggregated(
    registry: dict[str, DataFrame],
    source_name: str,
    target_name: str,
    config_json: str
) -> bytes:
    """Perform aggregated reconciliation via PySpark."""
    import logging
    logging.info(f"Starting reconciliation: {source_name} vs {target_name}")

    if source_name not in registry:
        return encode_error(f"Source frame '{source_name}' not found")
    if target_name not in registry:
        return encode_error(f"Target frame '{target_name}' not found")

    try:
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        return encode_error(f"Invalid config JSON: {e}")

    source_df = registry[source_name]
    target_df = registry[target_name]
    start = time.perf_counter()

    try:
        # Build aggregation expressions
        agg_exprs = _build_agg_exprs(config["aggregations"])

        # Aggregate source and target
        source_agg = source_df.groupBy(config["source_group_by"]).agg(*agg_exprs)
        target_agg = target_df.groupBy(config["target_group_by"]).agg(*agg_exprs)

        # Compute statistics
        source_groups = source_agg.count()
        target_groups = target_agg.count()

        # Build join condition
        src_keys = config["source_join_keys"]
        tgt_keys = config["target_join_keys"]
        join_cond = [source_agg[sk] == target_agg[tk] for sk, tk in zip(src_keys, tgt_keys)]

        # Matched groups
        matched = source_agg.join(target_agg, join_cond, "inner")
        matched_groups = matched.count()

        # Unmatched source (left anti join)
        source_only = source_agg.join(target_agg, join_cond, "left_anti")
        source_only_groups = source_only.count()

        # Unmatched target (right anti join)
        target_only = target_agg.join(source_agg, join_cond, "left_anti")
        target_only_groups = target_only.count()

        # Sample rows
        sample_limit = config.get("sample_limit", 100)
        matched_sample = _df_to_json_rows(matched, sample_limit)
        source_only_sample = _df_to_json_rows(source_only, sample_limit)
        target_only_sample = _df_to_json_rows(target_only, sample_limit)

        # Column totals comparison
        column_totals = _compute_column_totals(source_agg, target_agg, config["aggregations"])

        compute_ms = int((time.perf_counter() - start) * 1000)
        logging.info(f"Reconciliation complete in {compute_ms}ms")

        match_rate = matched_groups / source_groups if source_groups > 0 else 0.0
        result = {
            "statistics": {
                "source_groups": source_groups,
                "target_groups": target_groups,
                "matched_groups": matched_groups,
                "source_only_groups": source_only_groups,
                "target_only_groups": target_only_groups,
                "match_rate": match_rate
            },
            "matched_rows": {"total": matched_groups, "rows": matched_sample},
            "source_only": {"total": source_only_groups, "rows": source_only_sample},
            "target_only": {"total": target_only_groups, "rows": target_only_sample},
            "column_totals": column_totals
        }
        return encode_json_response(result)
    except Exception as e:
        logging.error(f"Reconciliation failed: {e}")
        return encode_error(f"Reconciliation failed: {str(e)}")


def _determine_cardinality(left_distinct: int, right_distinct: int, total_pairs: int) -> str:
    """Determine join cardinality type."""
    if total_pairs == 0:
        return "N/A"
    left_ratio = total_pairs / max(left_distinct, 1)
    right_ratio = total_pairs / max(right_distinct, 1)
    if left_ratio <= 1.05 and right_ratio <= 1.05:
        return "1:1"
    elif left_ratio <= 1.05:
        return "1:N"
    elif right_ratio <= 1.05:
        return "N:1"
    return "N:M"


def handle_join_analyze(
    registry: dict[str, DataFrame],
    left_name: str,
    right_name: str,
    config_json: str
) -> bytes:
    """Analyze join characteristics via PySpark."""
    import logging
    from functools import reduce
    logging.info(f"Analyzing join: {left_name} <-> {right_name}")

    if left_name not in registry:
        return encode_error(f"Left frame '{left_name}' not found")
    if right_name not in registry:
        return encode_error(f"Right frame '{right_name}' not found")

    try:
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        return encode_error(f"Invalid config JSON: {e}")

    left_df = registry[left_name]
    right_df = registry[right_name]
    left_keys = config["left_keys"]
    right_keys = config["right_keys"]

    if len(left_keys) != len(right_keys):
        return encode_error("Key count mismatch")

    start = time.perf_counter()

    try:
        # Total counts
        left_total = left_df.count()
        right_total = right_df.count()

        # Null key counts
        left_null_cond = reduce(lambda a, b: a | b, [F.col(k).isNull() for k in left_keys])
        right_null_cond = reduce(lambda a, b: a | b, [F.col(k).isNull() for k in right_keys])
        left_null_keys = left_df.filter(left_null_cond).count()
        right_null_keys = right_df.filter(right_null_cond).count()

        # Duplicate key counts
        left_dup = left_df.groupBy(left_keys).count().filter(F.col("count") > 1).count()
        right_dup = right_df.groupBy(right_keys).count().filter(F.col("count") > 1).count()

        # Build join condition
        join_cond = [left_df[lk] == right_df[rk] for lk, rk in zip(left_keys, right_keys)]

        # Matched counts via inner join
        joined = left_df.join(right_df, join_cond, "inner")
        left_matched = joined.select([left_df[k] for k in left_keys]).distinct().count()
        right_matched = joined.select([right_df[k] for k in right_keys]).distinct().count()
        total_pairs = joined.count()

        # Cardinality detection
        cardinality = _determine_cardinality(left_matched, right_matched, total_pairs)

        # Unmatched rows
        sample_limit = config.get("sample_limit", 100)
        left_unmatched = left_df.join(right_df, join_cond, "left_anti")
        right_unmatched = right_df.join(left_df, join_cond, "left_anti")
        left_unmatched_count = left_unmatched.count()
        right_unmatched_count = right_unmatched.count()

        compute_ms = int((time.perf_counter() - start) * 1000)
        logging.info(f"Join analysis complete in {compute_ms}ms")

        match_rate_left = left_matched / left_total if left_total > 0 else 0.0
        match_rate_right = right_matched / right_total if right_total > 0 else 0.0

        result = {
            "statistics": {
                "left_total": left_total,
                "right_total": right_total,
                "matched_left": left_matched,
                "matched_right": right_matched,
                "match_rate_left": match_rate_left,
                "match_rate_right": match_rate_right,
                "cardinality": cardinality,
                "left_null_keys": left_null_keys,
                "right_null_keys": right_null_keys,
                "left_duplicate_keys": left_dup,
                "right_duplicate_keys": right_dup
            },
            "left_unmatched": {
                "total": left_unmatched_count,
                "rows": _df_to_json_rows(left_unmatched, sample_limit)
            },
            "right_unmatched": {
                "total": right_unmatched_count,
                "rows": _df_to_json_rows(right_unmatched, sample_limit)
            }
        }
        return encode_json_response(result)
    except Exception as e:
        logging.error(f"Join analysis failed: {e}")
        return encode_error(f"Join analysis failed: {str(e)}")


def handle_join_unmatched_page(
    registry: dict[str, DataFrame],
    left_name: str,
    right_name: str,
    config_json: str
) -> bytes:
    """Get paginated unmatched rows for join analysis."""
    import logging
    logging.info(f"Fetching unmatched rows: {left_name} <-> {right_name}")

    if left_name not in registry:
        return encode_error(f"Left frame '{left_name}' not found")
    if right_name not in registry:
        return encode_error(f"Right frame '{right_name}' not found")

    try:
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        return encode_error(f"Invalid config JSON: {e}")

    left_df = registry[left_name]
    right_df = registry[right_name]
    left_keys = config["left_keys"]
    right_keys = config["right_keys"]
    side = config.get("side", "left")
    offset = config.get("offset", 0)
    limit = config.get("limit", 100)

    start = time.perf_counter()

    try:
        # Build join condition
        join_cond = [left_df[lk] == right_df[rk] for lk, rk in zip(left_keys, right_keys)]

        if side == "left":
            unmatched = left_df.join(right_df, join_cond, "left_anti")
        else:
            unmatched = right_df.join(left_df, join_cond, "left_anti")

        total = unmatched.count()

        # Apply pagination (offset via row_number window function would be expensive)
        # For simplicity, collect with limit offset+limit and slice
        rows = unmatched.limit(offset + limit).collect()
        page_rows = rows[offset:] if offset < len(rows) else []
        json_rows = [_serialize_for_json(r.asDict()) for r in page_rows]

        compute_ms = int((time.perf_counter() - start) * 1000)
        logging.info(f"Unmatched page complete in {compute_ms}ms")

        return encode_json_response({
            "rows": json_rows,
            "total": total,
            "offset": offset
        })
    except Exception as e:
        logging.error(f"Unmatched page failed: {e}")
        return encode_error(f"Unmatched page failed: {str(e)}")


def handle_join_overlap(
    registry: dict[str, DataFrame],
    frame1: str, frame2: str,
    cols1: list[str], cols2: list[str]
) -> bytes:
    """Return key overlap statistics between two frames."""
    if frame1 not in registry:
        return encode_error(f"DataFrame '{frame1}' not found")
    if frame2 not in registry:
        return encode_error(f"DataFrame '{frame2}' not found")
    if len(cols1) != len(cols2):
        return encode_error("Column count mismatch")

    df1 = registry[frame1]
    df2 = registry[frame2]

    for col in cols1:
        if col not in [f.name for f in df1.schema.fields]:
            return encode_error(f"Column '{col}' not found in '{frame1}'")
    for col in cols2:
        if col not in [f.name for f in df2.schema.fields]:
            return encode_error(f"Column '{col}' not found in '{frame2}'")

    start = time.perf_counter()

    if len(cols1) == 1:
        key1 = F.col(cols1[0])
        key2 = F.col(cols2[0])
    else:
        key1 = F.struct(*[F.col(c) for c in cols1])
        key2 = F.struct(*[F.col(c) for c in cols2])

    keys1 = df1.select(key1.alias("key")).distinct()
    keys2 = df2.select(key2.alias("key")).distinct()

    count1 = keys1.count()
    count2 = keys2.count()
    both = keys1.join(keys2, "key", "inner").count()
    left_only = count1 - both
    right_only = count2 - both

    compute_ms = int((time.perf_counter() - start) * 1000)

    overlap_pct = (both / max(count1, count2) * 100) if max(count1, count2) > 0 else 0.0

    return encode_json_response({
        "frame1": frame1,
        "frame2": frame2,
        "cols1": cols1,
        "cols2": cols2,
        "left_total": count1,
        "right_total": count2,
        "left_only": left_only,
        "right_only": right_only,
        "both": both,
        "overlap_pct": round(overlap_pct, 2),
        "compute_ms": compute_ms
    })


def dispatch_command(
    registry: dict[str, DataFrame], command: str
) -> bytes:
    """Parse and dispatch a command to the appropriate handler."""
    command = command.strip()

    if command == "LIST":
        return handle_list(registry)

    if command.startswith("SCHEMA:"):
        name = command[7:]
        return handle_schema(registry, name)

    if command.startswith("GET:"):
        parts = command[4:].split(":")
        if len(parts) != 2:
            return encode_error("Invalid GET format. Use GET:name:limit")
        name, limit_str = parts
        try:
            limit = int(limit_str)
        except ValueError:
            return encode_error(f"Invalid limit: {limit_str}")
        return handle_get(registry, name, limit)

    if command.startswith("STATS:"):
        name = command[6:]
        return handle_stats(registry, name)

    if command.startswith("COUNT:"):
        name = command[6:]
        return handle_count(registry, name)

    if command.startswith("JOIN_KEYS:"):
        parts = command[10:].split(":")
        if len(parts) != 2:
            return encode_error("Invalid JOIN_KEYS format. Use JOIN_KEYS:name:col1,col2,...")
        name, cols_str = parts
        columns = [c.strip() for c in cols_str.split(",") if c.strip()]
        if not columns:
            return encode_error("At least one column required")
        return handle_join_keys(registry, name, columns)

    if command.startswith("JOIN_TEMPORAL:"):
        parts = command[14:].split(":")
        if len(parts) != 3:
            return encode_error("Invalid JOIN_TEMPORAL format. Use JOIN_TEMPORAL:name:column:bucket")
        name, column, bucket = parts
        return handle_join_temporal(registry, name, column, bucket)

    if command.startswith("JOIN_OVERLAP:"):
        parts = command[13:].split(":")
        if len(parts) != 4:
            return encode_error("Invalid JOIN_OVERLAP format. Use JOIN_OVERLAP:f1:f2:cols1:cols2")
        frame1, frame2, cols1_str, cols2_str = parts
        cols1 = [c.strip() for c in cols1_str.split(",") if c.strip()]
        cols2 = [c.strip() for c in cols2_str.split(",") if c.strip()]
        if not cols1 or not cols2:
            return encode_error("At least one column required per frame")
        return handle_join_overlap(registry, frame1, frame2, cols1, cols2)

    if command.startswith("TEMPORAL_RANGE:"):
        parts = command[15:].split(":")
        if len(parts) != 3:
            return encode_error("Invalid TEMPORAL_RANGE format. Use TEMPORAL_RANGE:name:column:granularity")
        name, column, granularity = parts
        return handle_temporal_range(registry, name, column, granularity)

    if command.startswith("TEMPORAL_LOSS:"):
        parts = command[14:].split(":")
        if len(parts) != 4:
            return encode_error("Invalid TEMPORAL_LOSS format. Use TEMPORAL_LOSS:name:column:start:end")
        name, column, overlap_start, overlap_end = parts
        return handle_temporal_loss(registry, name, column, overlap_start, overlap_end)

    if command == "DQX_AVAILABLE":
        return handle_dqx_available()

    if command.startswith("DQ_PROFILE:"):
        name = command[11:]
        return handle_dq_profile(registry, name)

    if command.startswith("DQ_CHECK:"):
        # Format: DQ_CHECK:name:base64_rules_json
        parts = command[9:].split(":", 1)
        if len(parts) != 2:
            return encode_error("Invalid DQ_CHECK format. Use DQ_CHECK:name:rules_json")
        name, rules_json = parts
        return handle_dq_check(registry, name, rules_json)

    # SQL execution via Spark SQL
    if command.startswith("SQL:"):
        # Format: SQL:limit:query
        parts = command[4:].split(":", 1)
        if len(parts) != 2:
            return encode_error("Invalid SQL format. Use SQL:limit:query")
        limit_str, sql = parts
        try:
            limit = int(limit_str)
        except ValueError:
            return encode_error(f"Invalid limit: {limit_str}")
        return handle_sql(registry, sql, limit)

    # Aggregated reconciliation via PySpark
    if command.startswith("RECONCILE_AGG:"):
        # Format: RECONCILE_AGG:source:target:config_json
        parts = command[14:].split(":", 2)
        if len(parts) != 3:
            return encode_error("Invalid RECONCILE_AGG format. Use RECONCILE_AGG:source:target:config_json")
        source, target, config_json = parts
        return handle_reconcile_aggregated(registry, source, target, config_json)

    # Join analysis via PySpark
    if command.startswith("JOIN_ANALYZE:"):
        # Format: JOIN_ANALYZE:left:right:config_json
        parts = command[13:].split(":", 2)
        if len(parts) != 3:
            return encode_error("Invalid JOIN_ANALYZE format. Use JOIN_ANALYZE:left:right:config_json")
        left, right, config_json = parts
        return handle_join_analyze(registry, left, right, config_json)

    # Paginated unmatched rows for join analysis
    if command.startswith("JOIN_UNMATCHED:"):
        # Format: JOIN_UNMATCHED:left:right:config_json
        parts = command[15:].split(":", 2)
        if len(parts) != 3:
            return encode_error("Invalid JOIN_UNMATCHED format. Use JOIN_UNMATCHED:left:right:config_json")
        left, right, config_json = parts
        return handle_join_unmatched_page(registry, left, right, config_json)

    return encode_error(f"Unknown command: {command}")
