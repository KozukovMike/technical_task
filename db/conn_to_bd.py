import psycopg2
import pandas as pd
import os
from abc import ABC, abstractmethod
from typing import List, Iterable, Any, Dict
from statements.sql_statements import sql_all_currencies
from dotenv import load_dotenv


load_dotenv()


class DBClient(ABC):

    @staticmethod
    @abstractmethod
    def to_bd() -> None:
        pass

    @staticmethod
    @abstractmethod
    def from_bd() -> List:
        pass


class PostgresClient(DBClient):

    @staticmethod
    def to_bd() -> None:
        pass

    @staticmethod
    def from_bd(table_name: str) -> List[Dict]:
        USER = 'postgres'
        PASSWORD = 'fantasy27'
        HOST = 'localhost'
        PORT = '5432'
        DBNAME = 'TechnicalTask'
        conn = psycopg2.connect(
            dbname=DBNAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
        )
        if table_name == 'currencies':
            return pd.read_sql(sql=sql_all_currencies, con=conn).to_dict(orient='records')

