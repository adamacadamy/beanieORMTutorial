 ## Question 1How would you rename an existing column in a PostgreSQL database table in production, assuming the table is large(e.g. 1 billion records) and expecting zero downtime?

### Step 1: Create a View with Renamed Column
```sql
-- Create view that presents the column with new name
CREATE VIEW your_table_renamed AS 
SELECT 
    id,
    old_column_name AS new_column_name,  -- Alias the column
    other_column1,
    other_column2
    -- ... all other columns
FROM your_table;

-- Grant same permissions as original table
GRANT SELECT, INSERT, UPDATE, DELETE ON your_table_renamed TO your_app_user;
```

### Step 2: Make View Updatable (for writes)
```sql
-- Create INSTEAD OF triggers to handle DML operations
CREATE OR REPLACE FUNCTION handle_view_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO your_table (old_column_name, other_column1, other_column2)
    VALUES (NEW.new_column_name, NEW.other_column1, NEW.other_column2);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION handle_view_update()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE your_table 
    SET old_column_name = NEW.new_column_name,
        other_column1 = NEW.other_column1,
        other_column2 = NEW.other_column2
    WHERE id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION handle_view_delete()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM your_table WHERE id = OLD.id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Create the triggers
CREATE TRIGGER your_table_renamed_insert
    INSTEAD OF INSERT ON your_table_renamed
    FOR EACH ROW EXECUTE FUNCTION handle_view_insert();

CREATE TRIGGER your_table_renamed_update
    INSTEAD OF UPDATE ON your_table_renamed
    FOR EACH ROW EXECUTE FUNCTION handle_view_update();

CREATE TRIGGER your_table_renamed_delete
    INSTEAD OF DELETE ON your_table_renamed
    FOR EACH ROW EXECUTE FUNCTION handle_view_delete();
```

### Step 3: Update Application Configuration
- Update your application's database configuration to point to the view `your_table_renamed` instead of the original table
- No code changes needed - the view presents the same interface with the renamed column
- Deploy this configuration change

### Step 4: Verify Everything Works
- **Zero downtime**: Application now uses the view
- All CRUD operations work normally
- Column appears with new name to application
- Database operations continue uninterrupted

### Step 5: Optional - Physical Rename (During Maintenance)
```sql
-- If you want to eventually rename the physical column
-- Do this during a planned maintenance window (optional)

-- 1. Drop the view and triggers
DROP VIEW your_table_renamed CASCADE;

-- 2. Rename the actual column (requires brief lock)
ALTER TABLE your_table RENAME COLUMN old_column_name TO new_column_name;

-- 3. Update application to use table directly again
```

## Alternative: Application-Layer Solution

If you prefer to avoid database views entirely:

```python
# Use field aliases in your ORM
from beanie import Document
from pydantic import Field

class YourModel(Document):
    class Settings:
        name = "your_table"
    
    # Map new name to old database column
    new_column_name: str = Field(alias="old_column_name")
    other_columns: str
```

## Benefits of This Approach

✅ **True zero downtime** - no locks on the table  
✅ **Immediate effect** - rename is available instantly  
✅ **Fully functional** - all CRUD operations work  
✅ **Reversible** - can easily rollback  
✅ **No data migration** - works with existing data  
✅ **Production safe** - no risk to large tables  

## Performance Notes
- Views have minimal overhead for simple column aliasing
- Triggers add small overhead for writes (usually negligible)
- Indexes on the underlying table work normally
- Query performance is essentially identical

## Why This is True Zero Downtime

Unlike other approaches that involve:
- `ALTER TABLE` operations (require ACCESS EXCLUSIVE locks)
- Data migration (can take hours on large tables)
- Complex replication setups

This solution:
- Creates views instantly (no table locks)
- Works with existing data immediately
- Provides immediate column rename functionality
- Maintains full CRUD capabilities