CREATE TABLE availability (
    room_id SERIAL PRIMARY KEY,
    room_type VARCHAR(50),
    available_date DATE,
    status VARCHAR(20)
);
