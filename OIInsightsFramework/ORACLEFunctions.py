# Load libraries
import cx_Oracle
import pandas as pd
import logging
from typing import Optional


class ORACLEFunctions:
    def __init__(self,
                 user: Optional[str] = None,
                 pwd: Optional[str] = None,
                 service: Optional[str] = None,
                 lib_dir: Optional[str] = None):
        if lib_dir is None:
            cx_Oracle.init_oracle_client(lib_dir="C:\oracle")
        else:
            cx_Oracle.init_oracle_client(lib_dir=lib_dir)
        self.connection: cx_Oracle.connect = cx_Oracle.connect(
            user, pwd, service)
        logging.info("Created ORACLE Connection: {} {}  ".format(
            user, service))

    def execute_query_ORACLE(self, query: str, args=[]) -> pd.DataFrame:
        logging.info("Executing ORACLE query: {} , args:{}".format(query,args))
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        result = pd.DataFrame(cursor.fetchall())
        names = list(map(lambda x: x[0], cursor.description))
        if len(result)==0:
            result= pd.DataFrame(columns=names)
        else:
            result.columns = names
        logging.info("Executed ORACLE query, results: {}".format(len(result)))
        return result
