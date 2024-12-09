-- 
-- depends: 

CREATE TABLE otps (
    id SERIAL PRIMARY KEY,
    code VARCHAR(6) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    session_code VARCHAR(20) NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS idx_otps_code ON otps(code);
CREATE INDEX IF NOT EXISTS idx_otps_session_code ON otps(session_code);
