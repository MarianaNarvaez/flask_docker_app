from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy import create_engine

CONN: str = os.getenv("DATABASE_CONN_STRING")
GROUP: str = os.getenv("LOGGIN_GROUP")
database_p = ""
userandpass = ''
engine = create_engine('mssql+pyodbc:'+userandpass+database_p+'?driver=ODBC+Driver+17+for+SQL+Server', fast_executemany=True)

LIST_OF_PLANTS = """
select...
""".replace('\n', '')

LAST_DATE_PLANT = """
select...
""".replace('\n', '')

LIST_DATES_PLANT = """
select...
""".replace('\n', '')

SEL_ROLPSEEXCE = """
select...
""".replace('\n', '')

TRE_BLOCK_CATEG = """
select...
""".replace('\n', '')

TRE_BLOCK_CROLE = """
select...
""".replace('\n', '')

SEL_FACT_EXEP = """
select...
""".replace('\n', '')

DEL_FACT_EXEP = """
delete...
""".replace('\n', '')

LABOR_ROLE = """
select...
""".replace('\n', '')

LABOR_AREA = """
select...
""".replace('\n', '')

TRE_LABOR_AREA = """
select...
""".replace('\n', '')

DEL_FACT_WORK = """
delete...
""".replace('\n', '')

SEL_WORKSHEET = """
select...
""".replace('\n', '')

SEL_PSEUDOROLE = """
select...
""".replace('\n', '')

SEL_PLANTDATA = """
select...
where [dateId] = ? and 
[plantId] = ?
""".replace('\n', '')

SEL_APPEC = """
select...
""".replace('\n', '')

SEL_APPECDOS = """
select...
where Type = ? and type1 = ? and quantity = ?  
""".replace('\n', '')

SEL_JOBW = """
select...
where Week = ?
""".replace('\n', '')

SEL_APPEDFIXFL = """
select...
""".replace('\n', '')

SEL_APPEDFIXFLDOS = """
select...
""".replace('\n', '')

SEL_JOBCHANGES = """
select...
""".replace('\n', '')

SEL_ALLONAME = """
select...
""".replace('\n', '')

DEL_MONTHR = """
delete...
where dateid = ? and plantid = ?
""".replace('\n', '')

SEL_MONTHLYR = """
select...
where dateId = ? and plantId = ?
""".replace('\n', '')

DEL_PLANTA = """
delete...
where dateid = ? and plantid = ?
""".replace('\n', '')

SEL_JOBTITLE = """
select...
""".replace('\n', '')

SEL_SECALLOROLE = """
select...
""".replace('\n', '')

DEL_ALLOCA = """
delete...
where dateid = ? and plantid = ? 
""".replace('\n', '')

LIST_SECLISTCERO = ['','']
LIST_APPENDCERO = ['','','']

LABELSA = { 
    "": ['', '', 0],
    "": ['', '', 0],
    "": ['', '', 0],
    "": ['', '', 0],
}

LABELSB = {
    "": ['', '', '', 0],
    "": ['', '', '', 0],
    "": ['', '', '', 0],
    "": ['', '', '', 0],
    "": ['', '', '', 0]
}

LABELEXEP = {
    "" : '',
    "" : '',
    "" : '',
    "" : '',
    "" : ''
}