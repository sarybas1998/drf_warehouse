CREATE USER warehouse_read_only WITH PASSWORD 'BBt?xMGiP0JVNqD2mJb3C@';

-- Grant connect to your database
GRANT CONNECT ON DATABASE warehouse TO warehouse_read_only;

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO warehouse_read_only;

-- Grant select on all tables in the public schema
GRANT SELECT ON ALL TABLES IN SCHEMA public TO warehouse_read_only;

-- Optional: Automatically grant select on future tables in the public schema
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO warehouse_read_only;
