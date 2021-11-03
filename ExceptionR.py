import sys
#sys.path.insert(1, '/var/www/app/OIInsightsFramework')
sys.path.insert(1, './OIInsightsFramework')
from flask import Flask, render_template, url_for, request, redirect, Blueprint, session
import Config as con
from pandas import DataFrame
import numpy as np
import pandas as pd
from datetime import datetime
from LdapAuthentication import LdapAuthentication
from SQLFunctions import SQLFunctions
 
ExceptionR = Blueprint('ExceptionR', __name__, template_folder='templates')

SQLFunctions = SQLFunctions(con.CONN)

class Except():

    @ExceptionR.route('/ExceptionRep', methods=['GET','POST'])
    def ExceptionRep():

        plantId = session.get('plantId', None)
        dateUpdateInt = session.get('dateUpdateInt', None)
        MonthToFillExc = session.get('MonthToFill', None)
        yearToFill = session.get('yearToFill', None)
        LastDateStr = session.get('LastDateStr', None)
        plantName = session.get('plantName', None)
        dateUpdate = session.get('dateUpdate', None)
        LastDate = session.get('LastDate', None)
        user = session.get('USERNAME', None) 

        #try:

        if session.get("dicPseudo") is None:
            #dateUpdateInt = 20210601

            #Get data exceptions
            factExcep = SQLFunctions.execute_query_SQL(con.SEL_FACT_EXEP,[dateUpdateInt,plantId])
            
            #if Exception is empty for the month selected then it brings the data of last month loaded in exceptions
            if len(factExcep) <= 0:
                
                while len(factExcep) <= 0:
                    if MonthToFillExc == 1:
                        MonthPreLoad = 12
                        yearPreLoad = yearToFill-1
                    else: 
                        MonthToFillExc = MonthToFillExc-1
                        MonthPreLoad = MonthToFillExc
                        yearPreLoad = yearToFill
                    DatePreLoad = datetime(year=int(yearPreLoad), month=MonthPreLoad, day=1).date()
                    IntPreLoad = int(str(DatePreLoad)[0:4]+str(DatePreLoad)[5:7]+str(DatePreLoad)[8:10])
                    dateUpdateInt = IntPreLoad
                    factExcep = SQLFunctions.execute_query_SQL(con.SEL_FACT_EXEP,[IntPreLoad,plantId])     

            TreLabCatRole = SQLFunctions.execute_query_SQL(con.TRE_BLOCK_CROLE)
            factExcep = pd.merge(left=factExcep, right=TreLabCatRole[['laborBlockCategoryRoleId','laborBlockCategoryId','laborRoleId']],
            on='laborBlockCategoryRoleId',how='left').drop(columns=['populationDate','plantId','dateId'])

            pseudoExce = SQLFunctions.execute_query_SQL(con.SEL_ROLPSEEXCE,[dateUpdateInt,plantId])
            pseudoValiExce = pseudoExce[['Pseudo','Role','IdValidation']]
            session['pseudoValiExce'] = pseudoValiExce

            factExcep = pd.merge(left=factExcep, right=pseudoExce[['IdRole','IdCategory','Role','Pseudo','PseudoComm']], left_on=['laborRoleId', 'laborBlockCategoryId'], right_on=['IdRole', 'IdCategory'], how='left').drop(columns=['IdRole'])
            
        else: 
            
            exepBack = session.get('exepBack', None)
            factExcep =  exepBack

        factExcep['employees'] = factExcep['employees'].replace(0, '', inplace=False)
        factExcep['Comments'] = factExcep['Comments'].replace(np.nan, '', inplace=False)
        preDicFactExcep = factExcep[['Pseudo','Role','employees','IdCategory','PseudoComm','Comments']]

        #Split dataset in subsets
        outCate = preDicFactExcep.loc[preDicFactExcep['IdCategory']==1].set_index('Pseudo').T.to_dict('list')
        nonCate = preDicFactExcep.loc[preDicFactExcep['IdCategory']==2].set_index('Pseudo').T.to_dict('list')
        autCate = preDicFactExcep.loc[preDicFactExcep['IdCategory']==3].set_index('Pseudo').T.to_dict('list')
        secCate = preDicFactExcep.loc[preDicFactExcep['IdCategory']==4].set_index('Pseudo').T.to_dict('list')
        adminCate = preDicFactExcep.loc[preDicFactExcep['IdCategory']==5].set_index('Pseudo').T.to_dict('list')

        session['factExcep'] = factExcep

        #except:
        #    e = str(sys.exc_info()[0])
        #    insError = [[user,plantId,dateUpdateInt,e,datetime.now(),'/ExceptionRep']]
        #    insError = DataFrame(insError,columns=['User','PlantID','DateId','Error','DateRow', 'Comment'])
        #    insError.to_sql('ErrorLog', schema='dw', con=con.engine, if_exists='append', index=False)
        
        return render_template('exception.html', plantName=plantName, dateUpdate=dateUpdate, LastDate=LastDate, outCate=outCate, nonCate=nonCate, autCate=autCate, secCate=secCate, adminCate=adminCate)

    @ExceptionR.route('/GetException', methods=['GET','POST'])
    def GetException():    

        plantId = session.get('plantId', None)
        dateUpdateInt = session.get('dateUpdateInt', None)
        plantName = session.get('plantName', None)
        dateUpdate = session.get('dateUpdate', None)
        LastDate = session.get('LastDate', None)
        factExcep = session.get('factExcep', None)
        user = session.get('USERNAME', None)

        #try:
        for index, row in factExcep.iterrows():
            employees = request.form.get(row['Pseudo'])
            comment = request.form.get(row['PseudoComm'])
            if comment == '':
                comment = np.nan
            factExcep.at[index,'employees'] = 0 if employees=="" else float(employees)
            factExcep.at[index,'Comments'] = comment

        factExcep['dateId'] = dateUpdateInt
        factExcep['plantId'] = plantId 
        factExcep['populationDate'] = datetime.now()

        factExcep['employees'] = factExcep['employees'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        factExcep['Comments'] = factExcep['Comments'].replace('', np.nan, inplace=False)

        exepBack = factExcep[['Pseudo','Role','employees','IdCategory','PseudoComm','Comments','laborBlockCategoryRoleId']]
        #data set to go back
        session['exepBack'] = exepBack

        insExeption = factExcep[['plantId','dateId','laborBlockCategoryRoleId','employees','populationDate','Comments']]
        #data set to insert
        session['insExeption'] = insExeption

        session['totfirstBlockExe'] = request.form.get('totalfirstBlock')
        session['totSecBlockExe'] = request.form.get('totalSecBlock')

        if request.form['action'] == 'Back':  
            labelsA = session.get('labelsA', None)
            labelsB = session.get('labelsB', None)
            insLog = [[user,plantId,dateUpdateInt,'Back PlantData',datetime.now()]]
            insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
            #insert action in log
            insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)
            return render_template('plantData.html', plantName=plantName, dateUpdate=dateUpdate, LastDate=LastDate, labelsA=labelsA, labelsB=labelsB)

        insLog = [[user,plantId,dateUpdateInt,'Go Appendix',datetime.now()]]
        insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
        insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)
        
        #except:
        #    e = str(sys.exc_info()[0])
        #    insError = [[user,plantId,dateUpdateInt,e,datetime.now(),'/ExceptionRep']]
        #    insError = DataFrame(insError,columns=['User','PlantID','DateId','Error','DateRow', 'Comment'])
        #    insError.to_sql('ErrorLog', schema='dw', con=con.engine, if_exists='append', index=False)

        return redirect(url_for('Appendix.AppendixA')) 