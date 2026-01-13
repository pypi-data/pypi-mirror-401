"""
AIVibe PostgreSQL Knowledge Module

Complete PostgreSQL 16+ patterns, performance optimization,
multi-tenant design, and best practices.
"""


class PostgreSQLKnowledge:
    """Comprehensive PostgreSQL development knowledge."""

    VERSION = "16"

    SCHEMA_DESIGN = {
        "multi_tenant": {
            "row_level": """
-- Row-Level Security for multi-tenant isolation
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create RLS policy
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON projects
    USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Set tenant context in application
SET app.current_tenant = 'tenant-uuid-here';""",
            "schema_per_tenant": """
-- Schema-per-tenant for complete isolation
CREATE SCHEMA tenant_abc123;

CREATE TABLE tenant_abc123.projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL
);

-- Set search path for tenant
SET search_path TO tenant_abc123, public;""",
        },
        "common_patterns": {
            "soft_delete": """
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    deleted_at TIMESTAMPTZ,
    CONSTRAINT not_deleted EXCLUDE (email WITH =) WHERE (deleted_at IS NULL)
);

-- View for active records
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;""",
            "audit_trail": """
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by UUID,
    changed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by)
    VALUES (
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        TG_OP,
        CASE WHEN TG_OP = 'DELETE' THEN to_jsonb(OLD) ELSE NULL END,
        CASE WHEN TG_OP != 'DELETE' THEN to_jsonb(NEW) ELSE NULL END,
        current_setting('app.current_user', true)::uuid
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_audit
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger();""",
            "updated_at": """
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON projects
FOR EACH ROW EXECUTE FUNCTION update_updated_at();""",
        },
        "jsonb_patterns": {
            "storage": """
CREATE TABLE settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    preferences JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}'
);

-- GIN index for JSONB queries
CREATE INDEX idx_settings_preferences ON settings USING GIN (preferences);""",
            "queries": """
-- Access nested value
SELECT preferences->>'theme' FROM settings;
SELECT preferences->'notifications'->>'email' FROM settings;

-- Filter by JSONB value
SELECT * FROM settings WHERE preferences @> '{"theme": "dark"}';

-- Check key exists
SELECT * FROM settings WHERE preferences ? 'notifications';

-- Update nested value
UPDATE settings SET preferences = jsonb_set(preferences, '{theme}', '"light"');

-- Merge objects
UPDATE settings SET preferences = preferences || '{"newKey": "value"}';""",
        },
    }

    QUERIES = {
        "common_patterns": {
            "pagination": """
-- Keyset pagination (efficient for large datasets)
SELECT * FROM posts
WHERE created_at < $1
ORDER BY created_at DESC
LIMIT 20;

-- Offset pagination (for smaller datasets)
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 40;

-- Count with pagination
SELECT
    (SELECT COUNT(*) FROM posts WHERE tenant_id = $1) as total,
    posts.*
FROM posts
WHERE tenant_id = $1
ORDER BY created_at DESC
LIMIT 20 OFFSET $2;""",
            "upsert": """
-- Insert or update on conflict
INSERT INTO users (id, email, name)
VALUES ($1, $2, $3)
ON CONFLICT (email)
DO UPDATE SET name = EXCLUDED.name, updated_at = NOW()
RETURNING *;

-- Insert if not exists
INSERT INTO users (email, name)
VALUES ($1, $2)
ON CONFLICT (email) DO NOTHING
RETURNING *;""",
            "cte": """
-- Common Table Expression for complex queries
WITH active_projects AS (
    SELECT * FROM projects
    WHERE status = 'active' AND tenant_id = $1
),
project_stats AS (
    SELECT
        project_id,
        COUNT(*) as task_count,
        SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) as completed
    FROM tasks
    WHERE project_id IN (SELECT id FROM active_projects)
    GROUP BY project_id
)
SELECT
    p.*,
    COALESCE(s.task_count, 0) as task_count,
    COALESCE(s.completed, 0) as completed_count
FROM active_projects p
LEFT JOIN project_stats s ON p.id = s.project_id;""",
            "window_functions": """
-- Ranking
SELECT
    name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num
FROM players;

-- Running totals
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- Moving average
SELECT
    date,
    value,
    AVG(value) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as seven_day_avg
FROM metrics;""",
        },
        "full_text_search": """
-- Add search vector column
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Create trigger to update vector
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.body, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_search_update
BEFORE INSERT OR UPDATE ON articles
FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- Create GIN index
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Search query
SELECT *,
    ts_rank(search_vector, query) as rank
FROM articles,
    plainto_tsquery('english', $1) query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;""",
    }

    PERFORMANCE = {
        "indexes": {
            "btree": "CREATE INDEX idx_users_email ON users(email);",
            "partial": "CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;",
            "composite": "CREATE INDEX idx_tenant_created ON posts(tenant_id, created_at DESC);",
            "covering": "CREATE INDEX idx_users_lookup ON users(id) INCLUDE (name, email);",
            "expression": "CREATE INDEX idx_lower_email ON users(LOWER(email));",
            "concurrent": "CREATE INDEX CONCURRENTLY idx_name ON table(column);",
        },
        "explain": """
-- Analyze query plan
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';

-- With more details
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'test@example.com';

-- Key metrics to watch:
-- - Seq Scan vs Index Scan (prefer index)
-- - Actual rows vs estimated (if off, analyze table)
-- - Buffers hit vs read (higher hit ratio = better cache)""",
        "vacuum": """
-- Regular maintenance
VACUUM ANALYZE users;

-- Full vacuum (reclaims space, locks table)
VACUUM FULL users;

-- Configure autovacuum
ALTER TABLE high_churn_table SET (
    autovacuum_vacuum_scale_factor = 0.05,
    autovacuum_analyze_scale_factor = 0.02
);""",
        "partitioning": """
-- Range partitioning by date
CREATE TABLE events (
    id UUID DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_01 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE events_2024_02 PARTITION OF events
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Automatic partition creation (use pg_partman extension)""",
        "connection_pooling": """
-- PgBouncer configuration (pgbouncer.ini)
[databases]
mydb = host=localhost dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5""",
    }

    SECURITY = {
        "roles": """
-- Create application role
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure_password';

-- Grant minimum required permissions
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- Read-only role
CREATE ROLE readonly_user WITH LOGIN PASSWORD 'readonly_pass';
GRANT CONNECT ON DATABASE mydb TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;""",
        "rls": """
-- Row Level Security
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Policy for tenant isolation
CREATE POLICY tenant_policy ON projects
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Admin bypass policy
CREATE POLICY admin_policy ON projects
    FOR ALL
    TO admin_role
    USING (true);

-- Force RLS for table owner too
ALTER TABLE projects FORCE ROW LEVEL SECURITY;""",
        "encryption": """
-- Enable pgcrypto
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt sensitive data
INSERT INTO users (email, ssn_encrypted)
VALUES (
    'user@example.com',
    pgp_sym_encrypt('123-45-6789', 'encryption_key')
);

-- Decrypt
SELECT pgp_sym_decrypt(ssn_encrypted::bytea, 'encryption_key')
FROM users WHERE id = $1;""",
    }

    MIGRATIONS = {
        "safe_patterns": {
            "add_column": """
-- Safe: Add nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Unsafe: Add NOT NULL without default (locks table)
-- ALTER TABLE users ADD COLUMN phone VARCHAR(20) NOT NULL;

-- Safe: Add NOT NULL with default
ALTER TABLE users ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'active';

-- Remove default after backfill if needed
ALTER TABLE users ALTER COLUMN status DROP DEFAULT;""",
            "add_index": """
-- Safe: Create index concurrently (no lock)
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);

-- Unsafe: Regular create index (locks table)
-- CREATE INDEX idx_users_phone ON users(phone);""",
            "rename_column": """
-- Safe approach: Add new, migrate, remove old
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
UPDATE users SET full_name = name;
ALTER TABLE users DROP COLUMN name;

-- Or use view for backward compatibility
CREATE VIEW users_v2 AS
SELECT id, name AS full_name, email FROM users;""",
            "change_type": """
-- Safe: Create new column, migrate, swap
ALTER TABLE products ADD COLUMN price_new NUMERIC(10,2);
UPDATE products SET price_new = price::numeric(10,2);
ALTER TABLE products DROP COLUMN price;
ALTER TABLE products RENAME COLUMN price_new TO price;""",
        },
        "tools": {
            "flyway": "Java-based, version-controlled migrations",
            "golang-migrate": "Go-based, supports many databases",
            "prisma": "TypeScript ORM with migrations",
            "drizzle": "TypeScript ORM with push/pull migrations",
            "alembic": "Python SQLAlchemy migrations",
        },
    }

    CODING_STANDARDS = {
        "naming": {
            "tables": "snake_case plural - users, project_tasks",
            "columns": "snake_case - user_id, created_at",
            "indexes": "idx_{table}_{columns} - idx_users_email",
            "constraints": "type_{table}_{columns} - pk_users_id, fk_posts_user_id",
            "functions": "verb_noun - get_user, update_status",
        },
        "conventions": {
            "primary_key": "UUID with gen_random_uuid() or BIGSERIAL",
            "timestamps": "Use TIMESTAMPTZ, name as created_at/updated_at",
            "soft_delete": "deleted_at TIMESTAMPTZ column",
            "foreign_keys": "Always name and index foreign keys",
            "not_null": "Default to NOT NULL unless truly optional",
        },
        "avoid": [
            "SELECT * in production code",
            "Unbounded queries without LIMIT",
            "N+1 queries (use JOINs or batch)",
            "Storing sensitive data unencrypted",
            "Using SERIAL (prefer BIGSERIAL or UUID)",
            "Implicit type conversions",
        ],
    }

    AWS_RDS = {
        "aurora_postgresql": {
            "connection": """
-- Connection string format
postgresql://user:password@cluster.cluster-xxxxx.region.rds.amazonaws.com:5432/dbname?sslmode=require

-- With IAM authentication
import boto3

def get_iam_token():
    client = boto3.client('rds')
    return client.generate_db_auth_token(
        DBHostname='cluster.xxxxx.region.rds.amazonaws.com',
        Port=5432,
        DBUsername='iam_user',
        Region='us-east-1'
    )""",
            "performance_insights": """
-- Enable in RDS console or via CLI
aws rds modify-db-instance \\
    --db-instance-identifier myinstance \\
    --enable-performance-insights \\
    --performance-insights-retention-period 7""",
            "read_replicas": """
-- Route read queries to reader endpoint
reader_host = 'cluster-ro.cluster-xxxxx.region.rds.amazonaws.com'

-- Application-level read/write splitting
async def get_connection(readonly: bool = False):
    host = READER_HOST if readonly else WRITER_HOST
    return await asyncpg.connect(host=host, ...)""",
        },
    }

    def get_all(self) -> dict:
        """Get complete PostgreSQL knowledge."""
        return {
            "version": self.VERSION,
            "schema_design": self.SCHEMA_DESIGN,
            "queries": self.QUERIES,
            "performance": self.PERFORMANCE,
            "security": self.SECURITY,
            "migrations": self.MIGRATIONS,
            "coding_standards": self.CODING_STANDARDS,
            "aws_rds": self.AWS_RDS,
        }

    def get_coding_standards(self) -> dict:
        """Get PostgreSQL coding standards."""
        return self.CODING_STANDARDS

    def get_performance_guide(self) -> dict:
        """Get performance optimization guide."""
        return self.PERFORMANCE

    def get_security_patterns(self) -> dict:
        """Get security patterns."""
        return self.SECURITY
