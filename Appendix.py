import sys
#sys.path.insert(1, '/var/www/app/OIInsightsFramework')
sys.path.insert(1, './OIInsightsFramework')
#sys.path.insert(1, 'C:\Users\u569834\OneDrive - O-I\Desktop\Manning\DlloManningV2\manningUpdated\OIInsightsFramework')
from flask import Flask, render_template, url_for, request, redirect, Blueprint, session
import Config as con
from pandas import DataFrame
import numpy as np
import pandas as pd
from datetime import datetime
from LdapAuthentication import LdapAuthentication
from SQLFunctions import SQLFunctions
from sqlalchemy import create_engine
 
Appendix = Blueprint('Appendix', __name__, template_folder='templates')

SQLFunctions = SQLFunctions(con.CONN)

class Append():

    @Appendix.route('/AppendixA', methods=['GET', 'POST'])
    def AppendixA():

        plantId = session.get('plantId', None)
        dateUpdateInt = session.get('dateUpdateInt', None)
        MonthToFillAllo = session.get('MonthToFill', None)
        yearToFill = session.get('yearToFill', None)
        plantName = session.get('plantName', None)
        dateUpdate = session.get('dateUpdate', None)
        LastDate = session.get('LastDate', None)
        user = session.get('USERNAME', None) 
        
        #try:

        if session.get("dicPseudo") is None:
            workSheet = SQLFunctions.execute_query_SQL(
                con.SEL_WORKSHEET, [dateUpdateInt, plantId])

            #if Allocation is empty for the month selected then it brings the data of last month loaded in Allocation
            if len(workSheet) <= 0:

                while len(workSheet) <= 0:
                    if MonthToFillAllo == 1:
                        MonthPreLoad = 12
                        yearPreLoad = yearToFill-1 
                    else:
                        MonthToFillAllo = MonthToFillAllo-1
                        MonthPreLoad = MonthToFillAllo
                        yearPreLoad = yearToFill  

                    DatePreLoad = datetime(year=int(yearPreLoad),
                                        month=MonthPreLoad, day=1).date()
                    IntPreLoad = int(str(DatePreLoad)[
                                    0:4]+str(DatePreLoad)[5:7]+str(DatePreLoad)[8:10])
                    workSheet = SQLFunctions.execute_query_SQL(
                        con.SEL_WORKSHEET, [IntPreLoad, plantId])

            #pd.set_option('display.max_columns', None)
            #pd.set_option('display.max_rows', None)

            TreArea = SQLFunctions.execute_query_SQL(con.TRE_LABOR_AREA)
            mergWorkTre = pd.merge(left=workSheet, right=TreArea[[
                                'laborAreaRoleId', 'laborAreaId', 'laborRoleId']], on='laborAreaRoleId', how='left').drop(columns='laborAreaRoleId')

            pseudo = SQLFunctions.execute_query_SQL(con.SEL_PSEUDOROLE)
            pseudoValiApp = pseudo[['Pseudo','laborRoleName','IdValidation']]
            session['pseudoValiApp'] = pseudoValiApp
            preDic = pd.merge(left=mergWorkTre ,right=pseudo, left_on=['laborAreaId','laborRoleId'], right_on=['laborAreaId','RoleId'], how='left').drop(columns=['plantId','dateId','RoleId'])

            preDic['tempHeadCount'] = preDic['tempHeadCount'].replace(0, '', inplace=False)
            preDic['staffHeadCount'] = preDic['staffHeadCount'].replace(0, '', inplace=False)
            preDic['dailyShiftHourlyHeadCount'] = preDic['dailyShiftHourlyHeadCount'].replace(0, '', inplace=False)
            preDic['dailyHourlyHeadCount'] = preDic['dailyHourlyHeadCount'].replace(0, '', inplace=False)
            preDic['outsorceHeadCount'] = preDic['outsorceHeadCount'].replace(0, '', inplace=False)
            preDic['otherHeadCount'] = preDic['otherHeadCount'].replace(0, '', inplace=False)
            preDic['Comments'] = preDic['Comments'].replace(np.nan, '', inplace=False)

            preDic = preDic[["laborRoleName","tempHeadCount","staffHeadCount","dailyShiftHourlyHeadCount","dailyHourlyHeadCount","outsorceHeadCount","otherHeadCount", "Pseudo", "TempName", "StaffName", "DailyName", "ShiftName", "OutName", "OthName", "laborAreaId", "PseudoComm", "Comments"]]

            session['TreArea'] = TreArea 
            session['pseudo'] = pseudo 
        else:
            preDic = session.get('dicPseudo', None)

        preDic = preDic.sort_values('laborRoleName')

        AMgmt = preDic.loc[preDic['laborAreaId']==1].set_index('Pseudo').T.to_dict('list')
        ABatchFurnt = preDic.loc[preDic['laborAreaId']==2].set_index('Pseudo').T.to_dict('list')
        AForming = preDic.loc[preDic['laborAreaId']==3].set_index('Pseudo').T.to_dict('list')
        AMachinRepa = preDic.loc[preDic['laborAreaId']==4].set_index('Pseudo').T.to_dict('list')
        AMoldRepa = preDic.loc[preDic['laborAreaId']==5].set_index('Pseudo').T.to_dict('list')
        ALehr = preDic.loc[preDic['laborAreaId']==6].set_index('Pseudo').T.to_dict('list')
        ASelCol = preDic.loc[preDic['laborAreaId']==7].set_index('Pseudo').T.to_dict('list')
        AQuaAssu = preDic.loc[preDic['laborAreaId']==8].set_index('Pseudo').T.to_dict('list')
        AColdEnd = preDic.loc[preDic['laborAreaId']==9].set_index('Pseudo').T.to_dict('list')
        ABuiMain = preDic.loc[preDic['laborAreaId']==10].set_index('Pseudo').T.to_dict('list')
        ALogis = preDic.loc[preDic['laborAreaId']==13].set_index('Pseudo').T.to_dict('list')
        AOther = preDic.loc[preDic['laborAreaId']==11].set_index('Pseudo').T.to_dict('list')
        AAdmin = preDic.loc[preDic['laborAreaId']==12].set_index('Pseudo').T.to_dict('list')

        #except:
        #    e = str(sys.exc_info()[0])
        #    insError = [[user,plantId,dateUpdateInt,e,datetime.now(),'/AppendixA']]
        #    insError = DataFrame(insError,columns=['User','PlantID','DateId','Error','DateRow', 'Comment'])
        #    insError.to_sql('ErrorLog', schema='dw', con=con.engine, if_exists='append', index=False)

        return render_template('appendix.html', plantName=plantName, dateUpdate=dateUpdate, LastDate=LastDate, AMgmt = AMgmt, ABatchFurnt = ABatchFurnt, AForming = AForming, AMachinRepa = AMachinRepa, AMoldRepa = AMoldRepa, ALehr = ALehr, ASelCol = ASelCol, AQuaAssu = AQuaAssu, AColdEnd = AColdEnd, ABuiMain = ABuiMain, ALogis=ALogis, AOther = AOther, AAdmin = AAdmin)

    @Appendix.route('/GetAppendix', methods=['GET', 'POST'])
    def GetAppendix():

        TreAreaA = session.get('TreArea', None)
        pseudo = session.get('pseudo', None)
        plantId = session.get('plantId', None)
        dateUpdateInt = session.get('dateUpdateInt', None)
        plantName = session.get('plantName', None)
        dateUpdate = session.get('dateUpdate', None)
        LastDate = session.get('LastDate', None)
        user = session.get('USERNAME', None)

        #try:

        for index, row in pseudo.iterrows():
            TemValue = request.form.get(row['TempName'])
            StaffValue = request.form.get(row['StaffName'])
            DailyValue = request.form.get(row['DailyName'])
            ShiftValue = request.form.get(row['ShiftName'])
            OutValue = request.form.get(row['OutName'])
            OthValue = request.form.get(row['OthName'])
            commValue = request.form.get(row['PseudoComm'])
            pseudo.at[index,'tempHeadCount'] = TemValue
            pseudo.at[index,'staffHeadCount'] = StaffValue
            pseudo.at[index,'dailyShiftHourlyHeadCount'] = DailyValue
            pseudo.at[index,'dailyHourlyHeadCount'] = ShiftValue
            pseudo.at[index,'outsorceHeadCount'] = OutValue
            pseudo.at[index,'otherHeadCount'] = OthValue
            pseudo.at[index,'Comments'] = commValue

        facWork = pseudo
        dicPseudo = pseudo[["laborRoleName","tempHeadCount","staffHeadCount","dailyShiftHourlyHeadCount","dailyHourlyHeadCount","outsorceHeadCount","otherHeadCount", "Pseudo", "TempName", "StaffName", "DailyName", "ShiftName", "OutName", "OthName", "laborAreaId", "PseudoComm", "Comments"]]
        session['dicPseudo'] = dicPseudo

        if request.form['action'] == 'Back':  

            insLog = [[user,plantId,dateUpdateInt,'Back Exceptions',datetime.now()]]
            insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
            insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)

            exepBack = session.get('exepBack', None) 
            exepBack['employees'] = exepBack['employees'].replace(0, '', inplace=False)
            exepBack['Comments'] = exepBack['Comments'].replace(np.nan, '', inplace=False)
            exepBack = exepBack[['Pseudo','Role','employees','IdCategory','PseudoComm','Comments']]

            outCate = exepBack.loc[exepBack['IdCategory']==1].set_index('Pseudo').T.to_dict('list')
            nonCate = exepBack.loc[exepBack['IdCategory']==2].set_index('Pseudo').T.to_dict('list')
            autCate = exepBack.loc[exepBack['IdCategory']==3].set_index('Pseudo').T.to_dict('list')
            secCate = exepBack.loc[exepBack['IdCategory']==4].set_index('Pseudo').T.to_dict('list')
            adminCate = exepBack.loc[exepBack['IdCategory']==5].set_index('Pseudo').T.to_dict('list')
            return render_template('exception.html', plantName=plantName, dateUpdate=dateUpdate, LastDate=LastDate, outCate=outCate, nonCate=nonCate, autCate=autCate, secCate=secCate, adminCate=adminCate)


        sumTotalOI = request.form.get('sumTotalOI')
        session['sumAppenTot'] = sumTotalOI
        sumTotalOut = request.form.get('sumTotalOut')
        session['sumTotalOut'] = sumTotalOut

        facWork['dateId'] = dateUpdateInt
        facWork['populationDate'] = datetime.now()
        facWork['plantId'] = plantId

        facWork = pd.merge(left=facWork, right=TreAreaA[['laborAreaRoleId','laborAreaId','laborRoleId']], left_on=['laborAreaId','RoleId'], right_on=['laborAreaId','laborRoleId'], how='left').drop(columns=['laborRoleName'])

        facWork['tempHeadCount'] = facWork['tempHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        facWork['staffHeadCount'] = facWork['staffHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        facWork['dailyShiftHourlyHeadCount'] = facWork['dailyShiftHourlyHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        facWork['dailyHourlyHeadCount'] = facWork['dailyHourlyHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        facWork['outsorceHeadCount'] = facWork['outsorceHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        facWork['otherHeadCount'] = facWork['otherHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        facWork['Comments'] = facWork['Comments'].replace('', np.nan, inplace=False)

        insFacWork = facWork[['plantId','dateId','laborAreaRoleId','tempHeadCount','staffHeadCount','dailyShiftHourlyHeadCount','dailyHourlyHeadCount','outsorceHeadCount','otherHeadCount','populationDate','laborAreaId','laborRoleId','Comments']]
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        session['insFacWork'] = insFacWork

        insLog = [[user,plantId,dateUpdateInt,'Go Validations',datetime.now()]]
        insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
        insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)

        #except:
        #    e = str(sys.exc_info()[0])
        #    insError = [[user,plantId,dateUpdateInt,e,datetime.now(),'/GetAppendix']]
        #    insError = DataFrame(insError,columns=['User','PlantID','DateId','Error','DateRow', 'Comment'])
        #    insError.to_sql('ErrorLog', schema='dw', con=con.engine, if_exists='append', index=False)

        return redirect(url_for('Validation.PlantDetails'))

 
