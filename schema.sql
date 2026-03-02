CREATE TABLE IF NOT EXISTS users (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  phone TEXT NOT NULL UNIQUE,
  city TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_users_name_lower  ON users (lower(name));
CREATE INDEX IF NOT EXISTS idx_users_phone_lower ON users (lower(phone));
CREATE INDEX IF NOT EXISTS idx_users_city_lower  ON users (lower(city));
