# Load libraries
import pyhdb
import pandas as pd
import logging
from typing import Optional


class HANAFunctions:
    def __init__(self,
                 host: str = "",
                 port: int = '',
                 user: Optional[str] = None,
                 pwd: Optional[str] = None):
        self.connection: pyhdb.connect = pyhdb.connect(host=host,
                                                       port=port,
                                                       user=user,
                                                       password=pwd)
        logging.info("Created HANA Connection: {} {} {} ".format(
            host, port, user))

    def execute_query_HANA(self, query: str, args=None) -> pd.DataFrame: 
        logging.info("Executing HANA query: {}".format(query))
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        result = pd.DataFrame(cursor.fetchall())
        names = list(map(lambda x: x[0], cursor.description))
        if len(result)==0:
            result= pd.DataFrame(columns=names)
        else:
            result.columns = names
        logging.info("Executed HANA query, results: {}".format(len(result)))
        return result
