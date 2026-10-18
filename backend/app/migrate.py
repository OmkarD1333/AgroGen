from sqlalchemy import text
from app.database.database import engine

def migrate():
    statements = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'farmer';",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR(255) UNIQUE;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500);",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_provider VARCHAR(50) DEFAULT 'local';",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();",
        "ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL;",
    ]
    with engine.begin() as conn:
        for stmt in statements:
            print(f"Executing: {stmt}")
            conn.execute(text(stmt))
    print("Migration finished successfully!")

if __name__ == "__main__":
    migrate()
