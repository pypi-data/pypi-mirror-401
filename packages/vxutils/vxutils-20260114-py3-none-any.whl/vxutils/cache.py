"""SQLite缓存管理器"""

import io
import pickle
import logging
import sqlite3
import json
import hashlib
import time
from pathlib import Path
from functools import singledispatch
from typing import Optional, Any, Tuple


@singledispatch
def _serialize_data(data: Any) -> Tuple[bytes, str]:
    """序列化数据为字节流和数据类型"""
    data_bytes = io.BytesIO()
    pickle.dump(data, data_bytes)
    return data_bytes.getvalue(), "python"


def _deserialize_data(data_bytes: bytes, data_type: str) -> Any:
    """反序列化数据为原始对象"""

    if data_type == "polars":
        import polars as pl

        return pl.DataFrame(pl.read_parquet(io.BytesIO(data_bytes)))
    elif data_type == "pandas":
        import pandas as pd

        return pd.DataFrame(pl.read_parquet(io.BytesIO(data_bytes)))
    return pickle.loads(data_bytes)


"""反序列化数据"""


try:
    import pandas as pd

    @_serialize_data.register
    def _(data: pd.DataFrame) -> Tuple[bytes, str]:
        """序列化DataFrame为字节流"""

        data_bytes = io.BytesIO()
        data.to_parquet(data_bytes)
        return data_bytes.getvalue(), "pandas"
except ImportError:
    pass

try:
    import polars as pl

    @_serialize_data.register
    def _(data: pl.DataFrame) -> Tuple[bytes, str]:
        """序列化Polars DataFrame为Parquet"""
        data_bytes = io.BytesIO()
        data.write_parquet(data_bytes)
        return data_bytes.getvalue(), "polars"
except ImportError:
    pass


class Cache:
    """TTL缓存管理器"""

    def __init__(self, db_path: Path = ":memory:"):
        """初始化缓存管理器，连接SQLite数据库"""
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        # 启用WAL模式提升并发性能
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._init_database()

    def _init_database(self):
        """创建表和索引，支持版本管理"""
        try:
            cursor = self._conn.cursor()

            # 检查表是否存在
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='cache_data'
            """)
            table_exists = cursor.fetchone() is not None

            if not table_exists:
                # 创建新表（支持版本管理）
                cursor.execute("""
                    CREATE TABLE cache_data (
                        cache_key TEXT NOT NULL,
                        data BLOB NOT NULL,
                        data_type TEXT NOT NULL DEFAULT 'python',
                        ttl REAL NOT NULL DEFAULT 0,
                        expires_at REAL NOT NULL,
                        created_at REAL NOT NULL,
                        PRIMARY KEY (cache_key)
                    )
                """)

            # 创建索引
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_cache_key ON cache_data(cache_key)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_expires_at ON cache_data(expires_at)
            """)

            self._conn.commit()
        except sqlite3.Error as e:
            logging.error(f"初始化数据库失败: {e}")
            self._conn.rollback()

    def _generate_cache_key(self, **params) -> str:
        """生成缓存键"""
        # 将参数排序后序列化，确保相同参数生成相同键
        param_str = json.dumps(params, sort_keys=True, ensure_ascii=False)
        key_str = f"CACHEKEY_{param_str}"
        # 使用 MD5 生成短键名
        return hashlib.md5(key_str.encode("utf-8")).hexdigest()

    def get(self, **params) -> Optional[pl.DataFrame]:
        """获取缓存的DataFrame,即使过期也返回（数据永久保留）"""
        cache_key = self._generate_cache_key(**params)
        current_time = time.time()

        cursor = self._conn.cursor()
        # 查询最新版本的数据（不过滤过期时间，数据永久保留）
        cursor.execute(
            """
            SELECT data,data_type,ttl,expires_at FROM cache_data 
            WHERE cache_key = ? AND expires_at > ?;
            """,
            (cache_key, current_time),
        )

        row = cursor.fetchone()
        if row is None:
            return None

        data, data_type, ttl, expires_at = row

        if ttl > 0:
            expires_at = current_time + ttl
            # 更新访问统计（更新最新版本）
            cursor.execute(
                """
                UPDATE cache_data 
                SET  expires_at = ?
                WHERE cache_key = ?
            """,
                (expires_at, cache_key),
            )
            self._conn.commit()
        return _deserialize_data(data, data_type)

    def set(
        self,
        data: Any,
        ttl: float = 0,
        expires_at: float = float("inf"),
        **params,
    ) -> str:
        """保存DataFrame到缓存,设置过期时间（秒）,默认0表示永不过期

        Args:
            data (Any): 要缓存的数据
            ttl (float, optional): 缓存过期时间（秒），默认0表示永不过期
            **params: 缓存键的参数

        Returns:
            str: 缓存键,如果过期时间无效则返回空字符串
        """
        cache_key = self._generate_cache_key(**params)
        current_time = time.time()
        if ttl > 0:
            expires_at = current_time + ttl

        if expires_at <= current_time:
            return ""

        # DataFrame转为Parquet字节流
        try:
            data_bytes, data_type = _serialize_data(data)
            # 插入或更新缓存数据（保留所有历史版本）
            cursor = self._conn.cursor()
            cursor.execute(
                """
                INSERT INTO cache_data 
                (cache_key,data,data_type,ttl,expires_at,created_at)
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
                    data_type,
                    ttl,
                    expires_at,
                    current_time,
                ),
            )
            self._conn.commit()
            return cache_key
        except (TypeError, ValueError, sqlite3.Error) as e:
            logging.error(
                f"缓存数据{params=},{ttl=},{expires_at=},{data=}设置失败: {e}"
            )
            self._conn.rollback()
            return ""

    def clear(self) -> int:
        """清理缓存"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM cache_data")
            count = cursor.rowcount
            self.conn.commit()
            return count
        except sqlite3.Error as e:
            logging.error(f"清理缓存失败: {e}")
            self._conn.rollback()
            return 0

    def cleanup_expired(self) -> int:
        """清楚过期缓存"""

        try:
            current_time = time.time()
            cursor = self._conn.cursor()
            # 只标记为过期，不删除数据
            cursor.execute(
                """
                DELETE FROM cache_data
                WHERE expires_at <= ?
            """,
                (current_time,),
            )
            count = cursor.rowcount
            self._conn.commit()
            return count
        except sqlite3.Error as e:
            logging.error(f"清理过期缓存失败: {e}")
            self._conn.rollback()
            return 0

    def close(self):
        """关闭数据库连接"""
        if self._conn:
            self._conn.close()


if __name__ == "__main__":
    cache_manager = Cache()
    data = pl.DataFrame({"a": [1, 2, 3]})
    data = 1234556
    cache_key = cache_manager.set(data, ttl=4, ods="test", table="calendar")
    print(cache_key)
    # 等待过期
    time.sleep(2)
    data = cache_manager.get(ods="test", table="calendar")
    print(data)
    time.sleep(4.5)
    data = cache_manager.get(ods="test", table="calendar")
    print(data)
