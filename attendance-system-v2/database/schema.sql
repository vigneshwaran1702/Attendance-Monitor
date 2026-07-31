-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE
);

-- Attendances Table
CREATE TABLE attendances (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    check_in TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    check_out TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'present'
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_attendances_user_id ON attendances(user_id);
