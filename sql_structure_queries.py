SELECT_TABLE_PREFIX = """
SELECT SUBSTRING_INDEX(table_name, '_', 1) as prefix 
FROM information_schema.TABLES WHERE TABLE_TYPE = 'BASE TABLE' LIMIT 1;
"""