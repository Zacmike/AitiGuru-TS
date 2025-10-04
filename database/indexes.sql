CREATE INDEX IF NOT EXISTS idx_orders_date_status ON orders(order_date, status);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_nomenclature ON order_items(nomenclature_id);
CREATE INDEX IF NOT EXISTS idx_nomenclature_category_id ON nomenclature(category_id);
CREATE INDEX IF NOT EXISTS idx_nomenclature_top_category ON nomenclature(top_level_category_id);
CREATE INDEX IF NOT EXISTS idx_categories_parent_id ON categories(parent_id);


CREATE UNIQUE INDEX IF NOT EXISTS idx_daily_sales_unique ON daily_salse_aggregation(sale_date, nomenclature_id);


