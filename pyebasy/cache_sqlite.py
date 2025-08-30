from pathlib import Path
from typing import Dict, List, Tuple
import sqlite3
from datetime import datetime

import loggr
from commons_base import Cache, DirectoryContents
from datas import File, Directory, StorageElement, TopDirectory, ADirectory


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
            loggr.log_technical(f"Executing create table SQL: {sql}")
            self.conn.execute(sql)

    def insert_into(self, data: Dict[str, str]):
        """ Inserts given data into the table. """

        with self.conn:
            values = tuple(data.values())
            values_placeholders = ["?" for value in data.values()]

            columns_names_str = f"({', '.join(data.keys())})"
            values_placeholders_str = f"({', '.join(values_placeholders)})"

            sql = f"INSERT INTO {self.table_name} {columns_names_str} VALUES {values_placeholders_str}"
            loggr.log_technical(f"Executing insert SQL: {sql}")
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
            loggr.log_technical(f"Executing update SQL: {sql}")
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
            loggr.log_technical(f"Executing select one SQL: {sql}")
            return self.conn.execute(sql)
        else:
            args = where_values if where_values is not None else []
            sql = f"SELECT {columns_str} FROM {self.table_name} WHERE {where_statement}"
            loggr.log_technical(f"Executing e more: {sql}")
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
        loggr.log_detailed(f"Preparing SQLite cache in file {db_path}")

        self.conn = sqlite3.connect(db_path)
        self.files = SqliteTableHelper(self.conn, "files", {
            "path": "TEXT PRIMARY KEY",
            "parent_path": "TEXT",
            "size": "INTEGER",
            "date_of_creation": "TEXT",
            "date_of_last_modification": "TEXT"
        })

        self.directories = SqliteTableHelper(self.conn, "directories",{
            "path": "TEXT PRIMARY KEY",
            "parent_path": "TEXT",
            "date_of_creation": "TEXT"
        })

    @staticmethod
    def drop_existing(db_path: Path):
        if db_path.exists():
            loggr.log_detailed(f"Dropping already existing cache file {db_path}")
            db_path.unlink()

    def store_file(self, file: File):
        loggr.log_detailed(f"Storing file {file.path} into the cache")

        self.files.insert_into({
            "path": self._path_to_str(file.path),
            "parent_path": self._path_to_str(file.path.parent),
            "size": file.size,
            "date_of_creation": file.date_of_creation.isoformat(),
            "date_of_last_modification": file.date_of_last_modification.isoformat()
        })

    def store_directory(self, directory: ADirectory):
        loggr.log_detailed(f"Storing directory {directory.path} into the cache")

        path = self._path_to_str(directory.path)

        if isinstance(directory, Directory):
            parent_path = self._path_to_str(directory.path.parent)
            date_of_creation = directory.date_of_creation.isoformat()

            self.directories.insert_into({
                "path": path,
                "parent_path": parent_path,
                "date_of_creation": date_of_creation
            })
        else:
            self.directories.insert_into({
                "path": path,
                "parent_path": None,
                "date_of_creation": None
            })

    def get_contents(self, path: Path) -> DirectoryContents:
        owner_path_str = self._path_to_str(path)

        files_rows = self.files.select_from("parent_path == ?", [owner_path_str])
        files = [self._row_to_file(r) for r in files_rows]

        directories_rows = self.directories.select_from("parent_path == ?", [owner_path_str])
        directories = [self._row_to_directory(r) for r in directories_rows]

        return DirectoryContents(files, directories)

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
        row = self.files.select_one("path = ?", [self._path_to_str(path)])
        if row:
            return self._row_to_file(row)

    def get_directory(self, path):
        row = self.directories.select_one("path = ?", [self._path_to_str(path)])
        if row:
            return self._row_to_directory(row)

    def _row_to_file(self, row) -> File:
        return File(
            path=Path(row["path"]),
            size=row["size"],
            date_of_creation=datetime.fromisoformat(row["date_of_creation"]),
            date_of_last_modification=datetime.fromisoformat(row["date_of_last_modification"]))

    def _row_to_directory(self, row) -> Directory:
        has_parent_path = row["parent_path"]
        path = Path(row["path"])

        if has_parent_path:
            date_of_creation = datetime.fromisoformat(row["date_of_creation"])
            return Directory(path=path, date_of_creation=date_of_creation)
        else:
            return TopDirectory()

    def _path_to_str(self, path: Path):
        if str(path) != ".":
            return "./" + path.as_posix()
        else:
            return "."
