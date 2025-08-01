
WITH sku_stats AS (
    SELECT
        sku,
        COUNT(*)               AS total_orders,
        SUM(is_return)         AS total_returns,
        ROUND(
            100.0 * SUM(is_return) / NULLIF(COUNT(*), 0),
            2
        )                      AS return_rate_pct
    FROM {{ returns_table }}
    GROUP BY sku
)

SELECT *
FROM sku_stats
ORDER BY return_rate_pct DESC
LIMIT 10;

