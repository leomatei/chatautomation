CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  full_name TEXT,
  email TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status TEXT
);

INSERT INTO users (full_name, email, status)
VALUES
('Alice Smith', 'alice@example.com', 'active'),
('Bob Jones', 'bob@example.com', 'inactive');
