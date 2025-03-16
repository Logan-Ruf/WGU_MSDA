-- User Schemas
CREATE TABLE user_account (
    id SERIAL PRIMARY KEY,
    name VARCHAR(500),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    last_login TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE
);

-- SELECT * from user_account;

CREATE TABLE user_session (
    token VARCHAR(255) PRIMARY KEY UNIQUE,
    user_id INTEGER REFERENCES user_account(id),
    created_at TIMESTAMP NOT NULL,
    last_login TIMESTAMP
);

CREATE TABLE user_log (
    log_id SERIAL PRIMARY KEY UNIQUE,
    user_id INTEGER REFERENCES user_account(id),
    timestamp TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    action JSONB
);

-- Region Schemas
CREATE TABLE region (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    region_id INTEGER REFERENCES region(id)
);

-- Product Schemas
CREATE TABLE brand (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    logo VARCHAR(255),
    description TEXT
);

CREATE TABLE product_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type INTEGER REFERENCES product_type(id),
    brand INTEGER REFERENCES brand(id),
    price DECIMAL(10, 2),
    cost DECIMAL(10, 2),
    description TEXT,
    stock INTEGER
);
CREATE INDEX idx_type_search ON product (type, brand, stock);
CREATE INDEX idx_search ON product (name, stock);

-- Order Schemas
CREATE TABLE sales_channel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    ship_date TIMESTAMP,
    user_id INTEGER REFERENCES user_account(id),
    country_id INTEGER REFERENCES country(id),
    channel_id INTEGER REFERENCES sales_channel(id),
    priority SMALLINT,
    price DECIMAL(10, 2),
    cost DECIMAL(10, 2),
    profit DECIMAL(10, 2)
);
CREATE INDEX idx_revenue_reporting ON orders(date, country_id, channel_id) INCLUDE (price, profit);

CREATE TABLE order_item (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES product(id),
    amount INTEGER,
    unit_price DECIMAL(10, 2)
);
CREATE INDEX idx_product_reporting ON order_item (product_id);

CREATE TABLE product_review (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES product(id),
    user_id INTEGER REFERENCES user_account(id),
    rating INTEGER,
    review TEXT,
    -- Ensure that a user can only review a product once
    UNIQUE (product_id, user_id)
);

CREATE INDEX idx_product_review_product ON product_review (product_id, rating);
CREATE INDEX idx_product_review_user ON product_review (user_id);

-- Certification Schema
CREATE TABLE certification (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    organization VARCHAR(255),
    description TEXT
);

CREATE TABLE product_certification (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES product(id),
    cert_id INTEGER REFERENCES certification(id),
    issued DATE,
    expiration DATE,
    -- Ensure that a product can only have a certification once
    UNIQUE (product_id, cert_id)
);

CREATE INDEX idx_product_certification_product ON product_certification (product_id);
CREATE INDEX idx_product_certification_cert ON product_certification (cert_id);

CREATE TABLE brand_certification (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brand(id),
    cert_id INTEGER REFERENCES certification(id),
    issued DATE,
    expiration DATE,
    -- Ensure that a brand can only have a certification once
    UNIQUE (brand_id, cert_id)
);

CREATE INDEX idx_brand_certification_brand ON brand_certification (brand_id);
CREATE INDEX idx_brand_certification_cert ON brand_certification (cert_id);