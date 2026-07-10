# 🏛️ ADR-0001: Introduce Indexed `created_at` Timestamp for Database Cleanup Optimization

* **Date**: 2026-07-03
* **Author**: @Eugene
* **Status**: Accepted

## 1. Context (The Problem)

The system ingests high-volume sensor data into SQLite before streaming it to broker in batches of 50,000+ records. The post-delivery deletion strategy using `WHERE id IN (...)` fails due to SQLite's host parameter limits (`OperationalError: too many SQL variables`). Relying solely on `id` comparison introduces risks of data loss or incorrect deletions if auto-increment counters reset, misalign, or clear during maintenance.

## 2. Decision (The Solution)

Add a `created_at` column (`DateTime`) to the `SensorData` model with a database-level default value (`server_default=func.now()`) and an explicit index (`index=True`). Deletion after broker delivery will use a compound condition combining the batch's maximum values: `WHERE created_at <= :max_created_at AND id <= :max_id`.

## 3. Consequences & Trade-offs

* **Pros (+)**:
  * **Performance**: Replaces 50,000 discrete deletion parameters with a single indexed range scan, executing in milliseconds.
  * **Safety**: The dual-constraint (`id` + `created_at`) guarantees new records arriving mid-flight are never deleted, even if they share the exact same timestamp millisecond.
  * **Resilience**: Immune to auto-increment counter resets or ID overflow edge cases.
* **Cons (-)**:
  * **Storage Overhead**: Minor increase in SQLite file size due to storing the timestamp and maintaining its B-tree index.
  * **Migration Cost**: Requires schema update and index creation on existing production tables via Alembic.
