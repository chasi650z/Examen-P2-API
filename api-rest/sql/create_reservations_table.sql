CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    room_number INT NOT NULL,
    customer_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20)
);