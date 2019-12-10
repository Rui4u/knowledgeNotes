# -*- coding: utf-8 -*-
"""Module for the management of DataBases in Python.
| For now this Lib includes management for:
| - SQLite3 Connection
| - MySQL Connection
| - SQLServer
| - PostgreSQL
"""

import enum
import importlib
import os.path


class DBType(enum.Enum):
    """
    Simple Enum class for setting allowed connections.
    """

    SQLITE3 = 1
    MYSQL = 2
    SQLSERVER = 3
    POSTGRESQL = 4


class DBManager:
    """
    Connection that allows any DBType Enum connection type.

    Parameters
    ----------
    user : str
        The user to connect to DataBase.
    password : str
        The password needed to connect the DataBase.
        ("" in case password is not needed)
    dbname : str
        The name of the DB to connect.
    conex_type : :class:`DBType`
        The type of the connection.
    host : str
        The host to connect.
        (By default is "localhost")
    port : str
        The port used for the connection.
        (If port is not given, it will get it by default
        depending on the DBType)
    sslmode : bool
        Declares if SSLMODE is required.
        (False by default)
    """

    __slots__ = ['__user', '__password', '__dbname', '__conex_type',
                 '__host', '__port', '__sslmode', '__conex', '__cursor']

    def __init__(self, **kwargs):
        self._update(**kwargs)
        self.__conex = None
        self.__cursor = None

    def _update(self, **kwargs):
        self.__user = kwargs.get('user')
        self.__password = kwargs.get('password')
        self.__dbname = kwargs.get('dbname')
        self.__conex_type = kwargs.get('conex_type')
        if 'host' in kwargs:
            self.__host = kwargs.get('host')
        else:
            self.__host = "localhost"
        if 'port' in kwargs:
            self.__port = kwargs.get('port')
        else:
            self.__port = self._get_port()
        if 'sslmode' in kwargs:
            self.__sslmode = kwargs.get('sslmode')
        else:
            self.__sslmode = False

    def _connect(self):
        """
        This method check the DBType of the connection and makes a conect
        depending on it.
        """

        connection = self._get_driver()
        if self.__conex_type is DBType.MYSQL:
            self.__conex = connection.MySQLConnection(user=self.__user,
                                                      password=self.__password,
                                                      database=self.__dbname,
                                                      host=self.__host,
                                                      port=int(self.__port))
        elif self.__conex_type is DBType.SQLITE3:
            # SQLite3 is local so we just need the path
            self.__conex = connection.connect(self.__dbname)
        elif self.__conex_type is DBType.SQLSERVER:
            self.__conex = connection.connect(
                driver="{SQL Server}",
                server=self.__host,
                database=self.__dbname,
                uid=self.__user,
                pwd=self.__password
            )
        elif self.__conex_type is DBType.POSTGRESQL:
            if self.__sslmode:
                self.__conex = connection.connect(dbname=self.__dbname,
                                                  user=self.__user,
                                                  password=self.__password,
                                                  host=self.__host,
                                                  port=self.__port,
                                                  sslmode="require")
            else:
                self.__conex = connection.connect(dbname=self.__dbname,
                                                  user=self.__user,
                                                  password=self.__password,
                                                  host=self.__host,
                                                  port=self.__port)

        # Setting cursor
        self.__cursor = self._get_cursor_type()

    def _close(self):
        """
        Simple method that closes the connection.
        """

        self.__cursor.close()
        self.__conex.close()

    def _get_cursor_type(self):
        """
        Since MySQL needs (buffered=True) to read Data, I made this simple
        method to manage that param.

        Returns
        -------
        cursor() -> self.__conex.cursor(buffered=True) | self.__conex.cursor()
            Returns the needed cursor depending on the DB connection.
        """

        if self.__conex_type is DBType.MYSQL:
            return self.__conex.cursor(buffered=True)
        return self.__conex.cursor()

    def _get_driver(self):
        """
        Since every connection needs a special module, this method
        will get every driver depending on the connection type.

        Returns
        -------
        connection -> module
            The module for the connection.
        """

        try:
            if self.__conex_type is DBType.MYSQL:
                return importlib.import_module("mysql.connector.connection")
            elif self.__conex_type is DBType.SQLITE3:
                return importlib.import_module("sqlite3")
            elif self.__conex_type is DBType.SQLSERVER:
                return importlib.import_module("pyodbc")
            elif self.__conex_type is DBType.POSTGRESQL:
                return importlib.import_module("psycopg2")
            else:
                raise Exception("Not Supported Connection Type")
        except ModuleNotFoundError as ex:
            print("Missing module/driver, -> {}".format(ex.name))
            print("Please install it.")

    def _get_port(self):
        """
        Simple method to get a Port by default.
        """

        if self.get_conex_type is DBType.MYSQL:
            return "3306"
        elif self.get_conex_type is DBType.SQLSERVER:
            return "1433"
        elif self.get_conex_type is DBType.POSTGRESQL:
            return "5432"
        return ""

    def execute(self, sql: str, commit: bool = True, returns: bool = False) -> list:
        """
        This method will execute either a File.sql as well as pure SQL code.

        Parameters
        ----------
        sql : str
            If it's valid path to file, reads and executes the .sql file.
            Otherwise execute the source code given.
        commit : bool
            If it's True it will commit changes.
        returns : bool
            If it's True it will returns the values selected.

        Returns
        -------
        values -> list[tuple1, tuple2, ...]
            A list of the values selected.
        """

        self._connect()
        delimiter = ";"
        lines = None

        if os.path.isfile(sql):
            try:
                with open(sql, "r") as file:
                    lines = file.read().splitlines()
            except FileNotFoundError:
                print("Cannot read the file.")
        else:
            lines = sql.splitlines()

        sql = " ".join(line.strip() for line in lines)
        queries = [str(query) + delimiter for query in sql.split(delimiter) if str(query)]
        if queries:
            list(map(self.__cursor.execute, queries))

        if commit:
            self.__conex.commit()

        if returns:
            values = self.__cursor.fetchall()
            self._close()
            return values
        else:
            self._close()

    def select(self, table: str, *columns, condition: str = None, order: str = None) -> list:
        """
        This method gets every row in a list with tuples following the next
        sentence:
        | [row1, row2, row3, ...] -> [(column1, column2), (column1, column2), ...]

        Parameters
        ----------
        table : str
            The table we want the values from.
        columns : *str
            The columns we want the values from.
        condition : str
            The condition to select the values. Ex: condition="id = 1"
            | By default there's no condition.
        order : str
            Sets the order to returns the SELECT.
            | Ex: order="id ASC"

        Returns
        -------
        result -> list[tuple1, tuple2, ...]
            A list with every row selected as a tuple.
        """

        if self.__conex_type is DBType.POSTGRESQL:
            table = '"%s"' % table  # Checking for UpperCases
        sql = "SELECT {0} FROM {1}".format(", ".join(columns), table)

        if condition:
            sql += " WHERE {}".format(condition)
        if order:
            sql += " ORDER BY {}".format(order)

        sql += ";"

        values = self.execute(sql, commit=False, returns=True)

        if values:
            if len(values) < 2:
                values = values[0]  # Returning one tuple
                if len(values) < 2:  # Returning one value
                    values = values[0]

        return values

    def show_select(self, table: str, *columns, condition: str = None):
        """
        Simple method to show on Console the result of the select.

        Parameters
        ----------
        table : str
            The table we want the values from.
        columns : *str
            The columns we want the values from.
        condition : str
            The condition to select the values. Ex: condition='(id = 1)'
            | By default there's no condition.
        """

        final_string = "({})\n".format(", ".join(str(column) for column in columns))
        values = self.select(table, *columns, condition=condition)
        if not isinstance(values, str):
            if isinstance(values, tuple):
                final_string += "{}".format(values)
            else:
                final_string += "\n".join(str(value) for value in values)
        else:
            final_string += values
        print(final_string)

    def insert(self, table: str, **values):
        """
        This method will insert in the given table by:
        | **values -> (name="user name", age=21, ...)
        | INSERT INTO table (name, age, ...) VALUES ('user name', 21, ...)

        Parameters
        ----------
        table : str
            The table we will insert the values into.
        **values : dict
            List of parameters and values to add.
        """

        if self.__conex_type is DBType.POSTGRESQL:
            table = '"%s"' % table  # Checking for UpperCases
        sql = "INSERT INTO {0} ({1}) VALUES ".format(table, ", ".join(str(key) for key in values.keys()))

        parsed_values = []
        for value in values.values():
            if isinstance(value, float) or isinstance(value, int):
                parsed_values.append("%s" % value)
            else:
                parsed_values.append("'%s'" % value)

        sql += "({});".format(", ".join(str(value) for value in parsed_values))
        self.execute(sql)

    def delete(self, table: str, condition: str):
        """
        This method will remove entries where condition is True.
        | condition -> ("id=12 AND name="Juan")

        Parameters
        ----------
        table : str
            The table we will remove the entries from.
        condition : str
            The condition to remove entries.
        """

        if self.__conex_type is DBType.POSTGRESQL:
            table = '"%s"' % table  # Checking for UpperCases
        sql = "DELETE FROM %s " % table
        if condition:
            sql += "WHERE %s;" % condition
        else:
            sql += ";"

        self.execute(sql)

    def update(self, table: str, condition: str = None, **sets):
        """
        This method will update rows from a table.
        | Sets parameter will be the values to update following
        the next syntax:
        | update(table, condition, id = 1231, name = "TestName", ...)

        Parameters
        ----------
        table : str
            The table we will update.
        condition : str
            The condition used to select the row to update.
        **sets : dict
            The values used to update.
            Example: id = 1231, name = "TestName", ...
        """

        parsed_values = []
        key = 0  # Static value for getting keys in items tuple
        value = 1  # Static value for getting values in items tuple
        for item in sets.items():
            if isinstance(item[value], float) or isinstance(item[value], int):
                parsed_values.append("%s = %s" % (item[key], item[value]))
            else:
                parsed_values.append("%s = '%s'" % (item[key], item[value]))

        sql = "UPDATE {0} SET {1} ".format(table, ", ".join(parsed_values))

        if condition:
            sql += "WHERE %s;" % condition
        else:
            sql += ";"
        self.execute(sql)

    def create_table(self, table: str, **values):
        """
        This method will create a table with the syntax in **values.
        | **values -> (id="INTEGER(8) PRIMARY KEY NOT NULL", name="VARCHAR(255)", ...)

        Parameters
        ----------
        table : str
            The name of the table to create.
        **values : dict
            List of parameters for the table
        """

        sql = "CREATE TABLE IF NOT EXISTS {0} ({1});".format(table, ", ".join(
            (str(value[0]) + " " + str(value[1])) for value in values.items()))

        self.execute(sql)

    def drop_table(self, table: str):
        """
        This method remove a table from a Database.

        Parameters
        ----------
        table : str
            The name of the table to remove.
        """

        if self.__conex_type is DBType.POSTGRESQL:
            table = '"%s"' % table  # Checking for UpperCases
        self.execute("DROP TABLE IF EXISTS %s;" % table)

    def create_database(self, dbname: str):
        """
        Creates a Database.

        Parameters
        ----------
        dbname : str
            The name used to create the database.
        """
        
        if self.__conex_type is DBType.POSTGRESQL:
            self._connect()
            iso_lvl = importlib.import_module("psycopg2.extensions").ISOLATION_LEVEL_AUTOCOMMIT
            self.__conex.set_isolation_level(iso_lvl)
            self.__cursor = self.__conex.cursor()
            self.__cursor.execute("CREATE DATABASE %s;" % dbname)
            self.__conex.commit()
            self._close()
        else:
            self.execute("CREATE DATABASE IF NOT EXISTS %s;" % dbname)

    def drop_database(self, dbname: str):
        """
        Deletes a Database.

        Paramaters
        ----------
        dbname : str
            The name of the Database to drop.
        """

        if self.__conex_type is DBType.POSTGRESQL:
            self._connect()
            iso_lvl = importlib.import_module("psycopg2.extensions").ISOLATION_LEVEL_AUTOCOMMIT
            self.__conex.set_isolation_level(iso_lvl)
            self.__cursor = self.__conex.cursor()
            self.__cursor.execute("DROP DATABASE IF EXISTS %s;" % dbname)
            self.__conex.commit()
            self._close()
        else:
            self.execute("DROP DATABASE IF EXISTS %s;" % dbname)

    def callproc(self, name: str, *args, returns: bool = False):
        """
        Calls a Stored Procedure with the arguments in args.

        Parameters
        ----------
        name : str
            The name of the procedure to call.
        args : tuple
            The parameters required by the procedure.
        returns : bool
            If it's True it will return the result of the procedure.
        """

        values = None
        if len(args) == 1 and not args[0]:
            args = ()

        if self.__conex_type is DBType.MYSQL or self.__conex_type is DBType.POSTGRESQL:
            self._connect()
            values = self.__cursor.callproc(name, args)
            self._close()
        elif self.__conex_type is DBType.SQLSERVER:
            parsed_values = []
            for value in args:
                if isinstance(value[1], str):
                    parsed_values.append("%s = '%s'" % (value[0], value[1]))
                else:
                    parsed_values.append("%s = %s" % (value[0], value[1]))
            self.execute("EXEC {0} {1}".format(name, ", ".join(parsed_values)))
        else:
            raise Exception("%s has no 'CALL PROCEDURE' method." % self.__conex_type.name)

        if returns and values:
            return values

    @property
    def get_user_name(self) -> str:
        """
        This method will return the user name.

        Returns
        -------
        self.__user -> str
            A String with the User Name.
        """

        if self.__conex_type is not DBType.SQLITE3:
            return self.__user
        return "SQLite3 hasn't user."

    @property
    def get_dbname(self) -> str:
        """
        This method will return the DB name.

        Returns
        -------
        self.__dbname -> str
            A String with Data Base's name.
        """

        return self.__dbname

    @property
    def get_port(self) -> int:
        """
        This method will return the port used.

        Returns
        -------
        self.__port -> int
            An Integer with the port.
        """

        if self.__conex_type is not DBType.SQLITE3:
            return int(self.__port)
        return 0

    @property
    def get_host(self):
        """
        This method will return the Host used.

        Returns
        -------
        self.__host -> str
            The Host used as String.
        """

        if self.__conex_type is not DBType.SQLITE3:
            return int(self.__host)
        return "SQLite3 hasn't Host."

    @property
    def get_conex_type(self) -> DBType:
        """
        This method will return a Enum with the actual DBType.

        Returns
        -------
        self.__conex_type -> DBType
            A Enum DBType.
        """

        return self.__conex_type

    @property
    def get_conex(self):
        """
        This method will return the Connection Object.
        The object returned is close once is sended.

        Returns
        -------
        self.__conex -> Connection Object
            The actual Connection Object.
        """

        self._connect()
        conex = self.__conex
        self._close()
        return conex


class MySQLConnection(DBManager):
    """
    Connection with type MySQL.

    Parameters
    ----------
    user : str
        The user used to connect the DataBase.
    password : str
        The password needed to connect the DataBase.
        ("" if password is not necessary)
    dbname : str
        The name of the DB to connect.
    host : str
        The name of the host to connect.
        (By default is localhost)
    port : str
        The port used for the connection.
        (By default is 3306)
    sslmode : bool
        If it's True, SSL checker will be used.
        (By default is False)
    """

    def __init__(self, user: str, password: str, dbname: str,
                 host: str = "localhost", port: str = "3306", sslmode: bool = False):
        super().__init__(user=user, password=password, dbname=dbname,
                         conex_type=DBType.MYSQL, host=host, port=port, sslmode=sslmode)


class SQLite3(DBManager):
    """
    Connection with type SQLite3.

    Parameters
    ----------
    db : str
        The URL where DataBase.sqlite3 is stored.
    """

    def __init__(self, db: str):
        super().__init__(user="", password="", dbname=db, conex_type=DBType.SQLITE3)


class SQLServer(DBManager):
    """
    Connection with type SQLServer.

    Parameters
    ----------
    user : str
        The user used to connect.
    password : str
        The password needed to connect.
        ("" if password is not required)
    dbname : str
        The name of the DB to connect.
    host : str
        The host used to connect the DB.
        (By default is "localhost\\sqlexpress")
    port : str
        The port used for the connection.
        (By default is 1433)
    sslmode : bool
        If it's ``True``, SSL checker will be used.
        (By default is False)
    """

    def __init__(self, user: str, password: str, dbname: str,
                 host: str = "localhost\\sqlexpress", port: str = "1433", sslmode: bool = False):
        super().__init__(user=user, password=password, dbname=dbname,
                         conex_type=DBType.SQLSERVER, host=host, port=port, sslmode=sslmode)


class PostgreSQL(DBManager):
    """
    Connection with type PostgreSQL.

    Parameters
    ----------
    user : str
        The user used to connect.
    password : str
        The password needed to connect.
        ("" if password is not required)
    dbname : str
        The name of the DB to connect.
    host : str
        The host used to connect the DB.
        (By default is "localhost")
    port : str
        The port used for the connection.
        (By default is 5432)
    sslmode : bool
        If it's ``True``, SSL checker will be used.
        (By default is False)
    """

    def __init__(self, user: str, password: str, dbname: str,
                 host: str = "localhost", port: str = "5432", sslmode: bool = False):
        super().__init__(user=user, password=password, dbname=dbname,
                         conex_type=DBType.POSTGRESQL, host=host, port=port, sslmode=sslmode)
