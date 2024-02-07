CREATE TABLE IF NOT EXISTS "refresh_token" (
    id UUID PRIMARY KEY,
    user_id UUID,
    refresh_token VARCHAR(255),
    created_at timestamp
);


