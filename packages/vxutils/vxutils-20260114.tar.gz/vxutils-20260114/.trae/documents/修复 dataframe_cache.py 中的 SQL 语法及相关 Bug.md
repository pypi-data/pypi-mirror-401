# 修复 dataframe_cache.py 中的 SQL 语法和属性错误

## 1. 修正 SQL 语句 (src/vxutils/dataframe_cache.py)
将 `set` 方法中的 `INSERT` 语句修正为包含 `VALUES` 子句，并使用正确的列名 `data`。

```python
cursor.execute(
    """
    INSERT INTO cache_data 
    (cache_key, data, data_type, ttl, expires_at, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(cache_key) DO UPDATE SET
    data = excluded.data,
    data_type = excluded.data_type,
    ttl = excluded.ttl,
    expires_at = excluded.expires_at,
    created_at = excluded.created_at;
""",
    (
        cache_key,
        data_bytes,
        # ...
    ),
)
```

## 2. 修复属性访问错误
将 `clear`, `cleanup_expired`, `close` 方法中错误的 `self.conn` 修正为 `self._conn`，与 `__init__` 中保持一致。

## 3. 验证修复
创建一个简单的测试脚本，调用 `DataCache.set` 和 `DataCache.get` 以及 `DataCache.clear`，确保修复后功能正常且无报错。