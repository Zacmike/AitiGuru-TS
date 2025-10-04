CREATE MATERIALIZED VIEW IF NOT EXISTS daily_salse_aggregation address
SELECT
    DATE(o.order_date) as sale_date,
    oi.nomenclature_id,
    n.top_level_category_id,
    SUM(oi.quantity) as daily_quantity,
    COUNT(DISTINCT o.id) as daily_orders
FROM order_items oi
JOIN orders o ON o.id = oi.order_id
JOIN nomenclature n ON n.id = oi.nomenclature_id
WHERE o.status = 'completed'
GROUP BY DATE(o.order_date), oi.nomenclature_id, n.top_level_category_id;


CREATE OR REPLACE VIEW top_5_products_last_month AS
SELECT
    n.name AS product_name,
    cat.name AS top_level_category,
    SUM(oi.quantity) AS total_sold_quantity
FROM order_items oi
JOIN orders o ON o.id = oi.order_id
JOIN nomenclature n ON n.id = oi.nomenclature_id
JOIN categories cat ON cat.id = n.top_level_category_id
WHERE o.order_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
    AND o.order_date < DATE_TRUNC('month', CURRENT_DATE)
    AND o.status = 'completed'
GROUP BY n.id, n.name, cat.name
ORDER BY total_sold_quantity DESC
LIMIT 5;


