# Week 5: Data Metrics and Model Evaluation

---

## Day 1: pandas groupby + SQL aggregation

### Goal

- Practice pandas `groupby`, `agg`, `reset_index`, `sort_values`.
- Practice SQL `GROUP BY`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
- Compute user-level, city-level, and channel-level metrics.

```
df.groupby("key").agg(
    metric_name=("column", "function")
).reset_index()
```
```
SELECT group_col, COUNT(*) AS n, AVG(metric) AS avg_metric
FROM table
GROUP BY group_col;
```