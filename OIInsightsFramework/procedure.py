import globals
from SQLFunctions import *
from configManager import *
from SendEmail import *
import uuid
from datetime import datetime
import os
import traceback
import logging
import logging.config
from pathlib import Path
from typing import Optional


class Procedure:
    def __init__(self, IdName: str, IdRun: Optional[str] = None):
        self.IdName: str = IdName
        self.connection: str = globals.CONN
        self.config: configparser.ConfigParser = None
        self.process: str = None
        self.IdRun: str = str(uuid.uuid1()) if (IdRun is None) else IdRun
        self.ComputerName: str = os.getenv('COMPUTERNAME', 'defaultValue')
        self.sqlfunctions: SQLFunctions = SQLFunctions(self.connection)
        self.mainpath: Path = Path(globals.PATH) / self.IdName
        _logpath: Path = self.mainpath / "Logs"
        if not self.mainpath.exists():
            os.makedirs(self.mainpath)
        if not _logpath.exists():
            os.makedirs(_logpath)
        # Create logger
        _logFileName = _logpath / (self.IdRun + ".log")
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=_logFileName,
                            level=logging.DEBUG,
                            format=globals.LOGGER_FORMAT)
        self.logger: logging.Logger = logging.getLogger()
        self.logger.info('Succesfully instantiated Procedure for {}'.format(
            self.IdName))

    def writelog(self, message: str, level: Optional[str] = 'INFO'):
        try:
            print(message)
            if level == 'INFO':
                self.logger.info(message)
            elif level == 'ERROR':
                self.logger.error(message)
            elif level == 'DEBUG':
                self.logger.debug(message)
            elif level == 'WARNING':
                self.logger.warning(message)
            else:
                self.logger.critical(message)

            LogStatement = globals.STATEMENT_INSERT_LOG
            inserted = self.sqlfunctions.execute_statement_SQL(
                statement=LogStatement,
                args=[
                    self.IdRun,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                    message
                ])
        except:
            self.logger.critical(
                "Unable to log to database, message: {} \nLogStatement: {} ".
                format(message, LogStatement))

    def start(self):
        try:
            self.process = self.sqlfunctions.execute_query_SQL(
                query=globals.STATEMENT_SELECT_PROCESS, args=[self.IdName])
            if len(self.process) == 1:
                self.config = config_fromstring(
                    self.process['ConfigDictionary'][0])
                statement = globals.STATEMENT_INSERT_RUN
                inserted = self.sqlfunctions.execute_statement_SQL(
                    statement=statement,
                    args=[
                        self.IdRun, self.IdName,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                        1, self.ComputerName
                    ])
                if inserted != 1:
                    raise Exception("murio- se estalla - no pudo insertar")
                self.writelog("Process Started")
            else:
                raise Exception("murio- se estalla - no puso leer proceso")
        except:
            self.writelog(traceback.format_exc())
        finally:
            pass

    def finish(self, notify_developer: bool = False):
        try:
            status = "OK"
            affected = self.sqlfunctions.execute_statement_SQL(
                statement=globals.STATEMENT_UPDATE_RUN, args=[0, self.IdRun])
            self.writelog("Process Finished")
        except:
            self.writelog(traceback.format_exc())
            notify_developer = True
            status = "ERROR"
        finally:
            if notify_developer:
                Email(sender_email=globals.SENDER_EMAIL,
                      receiver_email=self.process['Developer'][0],
                      body=status,
                      subject='Process {} finished'.format(
                          self.IdName)).SendEmail()
