# -*- coding: utf-8 -*-
from hellmbot.env import ENV
from sqlite3 import connect as sqlite
from typing import Any, Iterable
from enum import Enum


##############################
# sqlite Database Management #
##############################


# Data types for sqlite table columns
class DBColumnsTypes(Enum):
    stroke = "TEXT"
    integer_number = "INTEGER"
    float_number = "FLOAT"


class DataBase(object):
    DB_PATH = ENV.DB_PATH

    @staticmethod
    def __getcolumns(columns: dict[str: DBColumnsTypes]) -> str:
        """
        Converts dictionary to a string for a sqlite query

        :param columns: Dict["column_title": ColumnType]
        :return: Part of sqlite query
        """
        keys = tuple(columns.keys())
        values = tuple(columns.values())
        lst = zip(keys, values)
        lst = [f"{column_title.lower()} {column_type.value}" for column_title, column_type in lst]
        return ", ".join(lst)

    def execute(self, request: str, params: list[Any] = None) -> None:
        """
        Executes sqlite query

        :param request: Query text
        :param params: Additional parameters for the request
        """
        with sqlite(self.DB_PATH) as db:
            cursor = db.cursor()
            if params is None:
                cursor.execute(request)
                return
            cursor.execute(request, params)
            db.commit()

    def gentable(self, table: str, columns: dict[str: DBColumnsTypes]) -> None:
        """
        Generates table in the database

        :param table: Name of the table
        :param columns: Columns in the table
        """
        request = f"""
        CREATE TABLE IF NOT EXISTS {table}
        (id INTEGER PRIMARY KEY, {self.__getcolumns(columns)})"""
        self.execute(request)

    def insert(self, table: str, items: dict[str: Any]) -> None:
        """
        Inserts data into a field of a database table

        :param table: Name of the table
        :param items: Dict["column_title": value]
        """
        columns = [title.lower() for title in tuple(items.keys())]
        columns = ", ".join(columns)
        values = list(items.values())
        request = f"""
        INSERT INTO {table} ({columns}) VALUES ({("?, " * len(values))[:-2]})"""
        self.execute(request, values)

    def get(self, table: str, column: list[str] = None, where: dict[str: Any] = None, order: str = None) -> list[Any]:
        """
        Returns data from sqlite table

        :param table: Name of the table
        :param column: List of the columns titles
        :param where: Dict['column_title': value]
        :param order: sqlite query order syntax stroke
        :return: List of values from table
        """
        values = None
        if column is None:
            column = "*"
        else:
            column = ", ".join(i.lower() for i in column)
        request = [f"SELECT {column} FROM {table}"]
        if where is not None:
            values = list(where.values())
            where = f"WHERE {", ".join(tuple(where.keys()))} = ({("?, " * len(values))[:-2]})"
            request.append(where)
        if order is not None:
            order = f"ORDER BY {order}"
            request.append(order)
        request = [" ".join(request)]
        if values is not None:
            request.append(values)
        with sqlite(self.DB_PATH) as db:
            cursor = db.cursor()
            cursor.execute(*request)
            return cursor.fetchall()

    def delete(self, table: str, where: dict[str: Any]) -> None:
        values = list(where.values())
        request = f"DELETE FROM {table} WHERE {", ".join(tuple(where.keys()))} = ({("?, " * len(values))[:-2]})"
        self.execute(request, values)


class ServersDB(DataBase):
    TABLE = "servers"

    def __init__(self, server_id: int) -> None:
        self.gentable(self.TABLE, {
            "server_id": DBColumnsTypes.integer_number,
            "channel_id": DBColumnsTypes.integer_number,
            "loop": DBColumnsTypes.integer_number
        })
        self.server = server_id

    def check_server_exists(self) -> bool:
        """
        Checks the existence of the server in the database table
        """
        lst = self.get(self.TABLE, ["server_id"])
        if len(lst) > 0:
            return True
        return False

    def add_channel(self, channel_id: int) -> None:
        """
        Adds channel to the database

        :param channel_id: id of discord channel
        """
        self.insert(self.TABLE, {
            "server_id": self.server,
            "channel_id": channel_id
        })

    @property
    def get_channels(self) -> tuple:
        """
        Returns tuple of server channel id's

        :return: tuple of server channel id's
        """
        lst = self.get(self.TABLE, ["channel_id"], {"server_id": self.server}, "loop")
        if len(lst) == 0:
            raise IndexError("This server has no added channels")
        return tuple(map(lambda element: element[0], lst))

    def clear_channels(self) -> None:
        """
        Deletes all server channels from the database
        """
        self.delete(self.TABLE, {"server_id": self.server})

    def __iter__(self) -> Iterable[int]:
        """
        Returns iterable object of server channel id's
        """
        return iter(self.get_channels)

    def __bool__(self) -> bool:
        """
        Checks the existence of the server in the database table
        """
        return self.check_server_exists()
