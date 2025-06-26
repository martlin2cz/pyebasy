from unittest import TestCase
import sqlite3

from cache_sqlite import SqliteCache, SqliteTableHelper
from cache_test_helpers import SomeCacheTestMixin


class TestSqliteCache(TestCase, SomeCacheTestMixin):
    def test_some_cache(self):
        cache = SqliteCache(db_path=":memory:")
        self.populate_cache(cache)
        self.check_has(cache)
        self.check_get(cache)


class TestSqliteTableHelper(TestCase):

    def test_foo(self):
        conn = sqlite3.connect(":memory:")
        with conn:
            helper = SqliteTableHelper(conn,"Foo", {
                "name": "TEXT",
                "number": "INTEGER"
            })

            helper.insert_into({"name": "lorem", "number": 421})
            helper.insert_into({"name": "ipsum", "number": 422})

            helper.update_in({"number": 420}, "name = ?", ["lorem"])
            helper.update_in({"name": "IPSUM"}, "name = ?", ["ipsum"])

            self.assertEqual(
                [
                    {"name": "lorem", "number": 420},
                    {"name": "IPSUM", "number": 422}
                ],
                helper.select_from())

            self.assertEqual(
                [],
                helper.select_from("name = ?", ["ipsum"]))

            self.assertEqual({"name": "lorem", "number": 420}, helper.select_one("name = ?", ["lorem"]))

            self.assertIsNone(helper.select_one("name = ?", ["DOLOR"]))

        conn.close()

