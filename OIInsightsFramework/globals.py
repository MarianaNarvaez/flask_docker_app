LOGGER_FORMAT: str = "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s"

HOST: str = ''

PORT: int = ''

SENDER_EMAIL: str = ''

CONN: str = """Driver={SQL Server};Server='';Database='';Trusted_Connection=yes;"""

PATH: str = "C:/DocumentsInsight"

STATEMENT_SELECT_PROCESS: str = """
SELECT * 
FROM ''
WHERE [IdName] = ?
""".replace("\n", "")

STATEMENT_INSERT_LOG: str = """
INSERT INTO 
''
VALUES  (?,?,?)
""".replace("\n", "")

STATEMENT_INSERT_RUN: str = """
INSERT INTO '' 
VALUES (?,?,?,?,?)
""".replace("\n", "")

STATEMENT_UPDATE_RUN: str = """
UPDATE ''
SET [State] = ? 
WHERE [IdRun] = ?
""".replace("\n", "")
