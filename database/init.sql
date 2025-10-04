CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS nomenclature (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL CHECK(quantity >= 0),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    category_id INT NOT NULL,
    top_level_category_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (top_level_category_id) REFERENCES categories(id)
);

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    nomenclature_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (nomenclature_id) REFERENCES nomenclature(id),
    UNIQUE(order_id, nomenclature_id)
)


INSERT INTO categories (name, parent_id) VALUES
('Компьютеры', 2)
('Ноутбуки', 2)
('Смартфоны', 3)
('Телевизоры', 1)
('Клавиатуры', NULL)


INSERT INTO clients (name, address) VALUES
('Михаил Шифутинский', 'Москва, ул. Пушкина, 123'),
('Анатолий Васерман', 'Калининград, ул. Ленина, 456'),
('Виктория Морозова', 'Москва, ул. Губкина 333');


INSERT INTO nomenclature (name, quantity, price, category_id) VALUES
('Iphone 15 Pro Max', 2, 130000.00, 3),
('MacBook Pro', 1, 120000.00, 2),
('LG Smart TV', 1, 10000.00, 4);

