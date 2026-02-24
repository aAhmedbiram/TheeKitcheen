-- Migration script to add delivery-related columns to orders table
-- Run this script on your Neon PostgreSQL database

-- Check if columns exist before adding them
DO $$
BEGIN
    -- Add customer_lat column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'orders' AND column_name = 'customer_lat'
    ) THEN
        ALTER TABLE orders ADD COLUMN customer_lat FLOAT NOT NULL DEFAULT 0.0;
        RAISE NOTICE 'Added customer_lat column';
    END IF;

    -- Add customer_lng column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'orders' AND column_name = 'customer_lng'
    ) THEN
        ALTER TABLE orders ADD COLUMN customer_lng FLOAT NOT NULL DEFAULT 0.0;
        RAISE NOTICE 'Added customer_lng column';
    END IF;

    -- Add address_text column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'orders' AND column_name = 'address_text'
    ) THEN
        ALTER TABLE orders ADD COLUMN address_text TEXT NOT NULL DEFAULT '';
        RAISE NOTICE 'Added address_text column';
    END IF;

    -- Add distance_km column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'orders' AND column_name = 'distance_km'
    ) THEN
        ALTER TABLE orders ADD COLUMN distance_km NUMERIC(10,2) NOT NULL DEFAULT 0.0;
        RAISE NOTICE 'Added distance_km column';
    END IF;

    -- Add delivery_fee column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'orders' AND column_name = 'delivery_fee'
    ) THEN
        ALTER TABLE orders ADD COLUMN delivery_fee NUMERIC(10,2) NOT NULL DEFAULT 0.0;
        RAISE NOTICE 'Added delivery_fee column';
    END IF;

    -- Add customer_name column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'orders' AND column_name = 'customer_name'
    ) THEN
        ALTER TABLE orders ADD COLUMN customer_name VARCHAR(80) NOT NULL DEFAULT '';
        RAISE NOTICE 'Added customer_name column';
    END IF;

    -- Add customer_phone column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'orders' AND column_name = 'customer_phone'
    ) THEN
        ALTER TABLE orders ADD COLUMN customer_phone VARCHAR(20) NOT NULL DEFAULT '';
        RAISE NOTICE 'Added customer_phone column';
    END IF;

    -- Add created_at column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'orders' AND column_name = 'created_at'
    ) THEN
        ALTER TABLE orders ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
        RAISE NOTICE 'Added created_at column';
    END IF;

END $$;

-- Create indexes for performance if they don't exist
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);

-- Grant permissions (adjust user/role as needed)
-- GRANT ALL PRIVILEGES ON TABLE orders TO your_user;

COMMIT;

-- Verify the columns were added
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'orders' 
ORDER BY ordinal_position;
