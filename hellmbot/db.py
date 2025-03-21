# -*- coding: utf-8 -*-
from hellmbot.env import env
from hellmbot.logger import logger
from aiosqlite import connect as sqlite_connect
from typing import Any, Iterable
from enum import Enum


##############################
# sqlite Database Management #
##############################


class DBColumnsTypes(Enum):
    """
    Data types for sqlite table columns
    """

    stroke = "TEXT"
    integer_number = "INTEGER"
    float_number = "FLOAT"


class DataBase(object):
    """
    Describes the interaction with the database sqlite3
    """

    DB_PATH = env.DB_PATH

    @staticmethod
    def __getcolumns(columns: dict[str:DBColumnsTypes]) -> str:
        """
        Converts dictionary to a string for a sqlite query

        :param columns: Dict["column_title": ColumnType]
        :return: Part of sqlite query
        """
        keys = tuple(columns.keys())
        values = tuple(columns.values())
        lst = zip(keys, values)
        lst = [
            f"{column_title.lower()} {column_type.value}"
            for column_title, column_type in lst
        ]
        return ", ".join(lst)

    async def _execute(self, request: str, params: Iterable[Any] = None) -> None:
        """
        Executes sqlite query

        :param request: Query text
        :param params: Additional parameters for the request
        """
        async with sqlite_connect(self.DB_PATH) as db:
            cursor = await db.cursor()
            if params is None:
                await cursor.execute(request)
                return
            await cursor.execute(request, params)
            await db.commit()

    async def _gentable(self, table: str, columns: dict[str:DBColumnsTypes]) -> None:
        """
        Generates table in the database

        :param table: Name of the table
        :param columns: Columns in the table
        """
        request = f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, {self.__getcolumns(columns)})"
        await self._execute(request)

    async def _insert(self, table: str, items: dict[str:Any]) -> None:
        """
        Inserts data into a field of a database table

        :param table: Name of the table
        :param items: Dict["column_title": value]
        """
        columns = [title.lower() for title in tuple(items.keys())]
        columns = ", ".join(columns)
        values = tuple(items.values())
        request = (
            f"INSERT INTO {table} ({columns}) VALUES ({('?, ' * len(values))[:-2]})"
        )
        await self._execute(request, values)

    async def _get(
        self,
        table: str,
        column: list[str] = None,
        where: dict[str:Any] = None,
        order: str = None,
    ) -> list[Any]:
        """
        Returns data from sqlite table

        :param table: Name of the table
        :param column: List of the columns titles
        :param where: Dict['column_title': value]
        :param order: sqlite query order syntax stroke
        :return: List of values from table
        """
        args = None
        if column is None:  # if no column is specified, all columns are used by default
            column = "*"
        else:
            column = ", ".join(i.lower() for i in column)
        request = [f"SELECT {column} FROM {table}"]
        if where is not None:
            args = list(where.values())
            where = (
                f"WHERE {', '.join(tuple(where.keys()))} = ({('?, ' * len(args))[:-2]})"
            )
            request.append(where)
        if order is not None:
            order = f"ORDER BY {order}"
            request.append(order)
        request = [" ".join(request)]
        if args is not None:
            request.append(args)
        async with sqlite_connect(self.DB_PATH) as db:
            cursor = await db.cursor()
            await cursor.execute(*request)
            return await cursor.fetchall()

    async def _delete(self, table: str, where: dict[str:Any]) -> None:
        values = list(where.values())
        request = f"DELETE FROM {table} WHERE {', '.join(tuple(where.keys()))} = ({('?, ' * len(values))[:-2]})"
        await self._execute(request, values)


class ServersDB(DataBase):
    """
    Describes the server channel table in the database

    Attributes:
    - channels (tuple) - Tuple of server channel id's
    """

    TABLE = "servers"  # Table name constant

    def __init__(self, server_id: int) -> None:
        """
        Init Server DataBase object

        :param server_id: id of discord server
        """
        self.server = server_id

    async def gen_table(self):
        await self._gentable(
            self.TABLE,
            {
                "server_id": DBColumnsTypes.integer_number,  # id of discord server
                "channel_id": DBColumnsTypes.integer_number,  # id of discord voice channel id
                "loop": DBColumnsTypes.integer_number,  # Channel sequence number
            },
        )
        logger.info("The database was initialized successfully")

    async def check_server_exists(self) -> bool:
        """
        Checks the existence of the server in the database table
        """
        lst = await self._get(self.TABLE, ["server_id"], {"server_id": self.server})
        if len(lst) > 0:
            return True
        return False

    async def add_channel(self, channel_id: int, loop_number: int) -> None:
        """
        Adds channel to the database

        :param channel_id: id of discord channel
        :param loop_number: Channel sequence number in the group
        """
        await self._insert(
            self.TABLE,
            {"server_id": self.server, "channel_id": channel_id, "loop": loop_number},
        )

    @property
    async def channels(self) -> tuple:
        """
        Returns tuple of server channel id's

        :return: tuple of server channel id's
        """
        lst = await self._get(
            self.TABLE, ["channel_id"], {"server_id": self.server}, "loop"
        )
        if len(lst) == 0:
            raise IndexError("This server has no added channels")
        return tuple(map(lambda element: element[0], lst))

    async def clear_channels(self) -> None:
        """
        Deletes all server channels from the database
        """
        await self._delete(self.TABLE, {"server_id": self.server})
        logger.info(
            f"server id {self.server} channels have been successfully cleaned from database"
        )
