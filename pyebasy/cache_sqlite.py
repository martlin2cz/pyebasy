from pathlib import Path
from typing import Dict, List, Tuple
import sqlite3
from datetime import datetime

from commons_base import Cache
from datas import File, Directory, StorageElement


########################################################################################################################

class SqliteTableHelper:
    """ The helper tool for the sqlite table manipulation. Encapsulates the SQL quering by nicer convience methods. """

    conn: sqlite3.Connection
    table_name: str

    def __init__(self, connection: sqlite3.Connection, table_name: str, table_def: Dict[str, str]):
        """ Creates the helper for the sqlite3 connection, working with table with given name and attributes. """
        self.conn = connection

        self.table_name = table_name
        self.table_columns_names = tuple(table_def.keys())

        self.create_table(table_def)

    def create_table(self, table_def: Dict[str, str]):
        """ Creates the table. Internal. """

        with self.conn:
            table_def_strs = [f"{col_name} {col_declaration}" for col_name, col_declaration in table_def.items()]
            table_def_str = f"({', '.join(table_def_strs)})"
            sql = f"CREATE TABLE IF NOT EXISTS  {self.table_name} {table_def_str}"
            self.conn.execute(sql)

    def insert_into(self, data: Dict[str, str]):
        """ Inserts given data into the table. """

        with self.conn:
            values = tuple(data.values())
            values_placeholders = ["?" for value in data.values()]

            columns_names_str = f"({', '.join(data.keys())})"
            values_placeholders_str = f"({', '.join(values_placeholders)})"

            sql = f"INSERT INTO {self.table_name} {columns_names_str} VALUES {values_placeholders_str}"
            self.conn.execute(sql, values)

    def update_in(self, new_data: Dict[str, any], where_statement: str, where_values: List[any]):
        """ Updates the data in the table to the given ones based on the condition. """

        with self.conn:
            values = tuple(new_data.values())
            assigned_columns_names = new_data.keys()

            columns_assignments_strs = [f"{column_name} = ?" for column_name in assigned_columns_names]
            columns_assignments_str = f"{', '.join(columns_assignments_strs)}"

            sql = f"UPDATE {self.table_name} SET {columns_assignments_str} WHERE {where_statement}"
            sql_values = [*values, *where_values]
            self.conn.execute(sql, sql_values)

    def select_from(self, where_statement: str = None, where_values: List[any] = None) -> List[Dict[str, any]]:
        """ Selects the records from the table (optionally only those matcing the criteria). """

        with self.conn:
            cursor = self._do_select(where_statement, where_values)
            return [self._tuple_to_dict(record) for record in cursor.fetchall()]

    def select_one(self, where_statement: str = None, where_values: List[any] = None):
        """ Retrieves one and only one record form the table. """
        with self.conn:
            cursor = self._do_select(where_statement, where_values)
            fetched = cursor.fetchmany(2)
            if len(fetched) == 0:
                return None
            elif len(fetched) == 1:
                return self._tuple_to_dict(fetched[0])
            else:
                raise ValueError("Not one record matching: " + str(fetched))

    def _do_select(self, where_statement, where_values):
        columns_str = f"{', '.join(self.table_columns_names)}"

        if where_statement is None:
            sql = f"SELECT {columns_str} FROM {self.table_name}"
            return self.conn.execute(sql)
        else:
            args = where_values if where_values is not None else []
            sql = f"SELECT {columns_str} FROM {self.table_name} WHERE {where_statement}"
            return self.conn.execute(sql, args)

    def _tuple_to_dict(self, values: Tuple[any]):
        if values is None:
            return None
        else:
            return {column_name: values[i] for i, column_name in enumerate(self.table_columns_names)}

########################################################################################################################


class SqliteCache(Cache):
    """ The cache which keeps the files and directories in a sqlite database file. """

    def __init__(self, db_path: Path = Path("cache.db")):
        self.conn = sqlite3.connect(db_path)
        self.files = SqliteTableHelper(self.conn, "files", {
            "path": "TEXT PRIMARY KEY",
            "size": "INTEGER",
            "date_of_creation": "TEXT",
            "date_of_last_modification": "TEXT"
        })

        self.directories = SqliteTableHelper(self.conn, "directories",{
            "path": "TEXT PRIMARY KEY",
            "date_of_creation": "TEXT"
        })

    def store_file(self, file: File):

        self.files.insert_into({
            "path": str(file.path),
            "size": file.size,
            "date_of_creation": file.date_of_creation.isoformat(),
            "date_of_last_modification": file.date_of_last_modification.isoformat()
        })

    def store_directory(self, directory: Directory):

        self.directories.insert_into({
            "path": str(directory.path),
            "date_of_creation": directory.date_of_creation.isoformat()
        })

    def has(self, path: Path) -> bool:
        file = self.get_file(path)
        if file:
            return True

        directory = self.get_directory(path)
        if directory:
            return True

        return False

    def get(self, path: Path) -> StorageElement:
        file = self.get_file(path)
        if file:
            return file

        directory = self.get_directory(path)
        if directory:
            return directory

        raise ValueError(f"No such storage element with path {path}")

    def get_file(self, path: Path):
        row = self.files.select_one("path = ?", [str(path)])
        if row:
            return File(
                path=Path(row["path"]),
                size=row["size"],
                date_of_creation=datetime.fromisoformat(row["date_of_creation"]),
                date_of_last_modification=datetime.fromisoformat(row["date_of_last_modification"])
            )

    def get_directory(self, path):
        row = self.directories.select_one("path = ?", [str(path)])
        if row:
            return Directory(
                path=Path(row["path"]),
                date_of_creation=datetime.fromisoformat(row["date_of_creation"])
            )

