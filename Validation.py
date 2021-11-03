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
import math

Validation = Blueprint('Validation', __name__, template_folder='templates')

SQLFunctions = SQLFunctions(con.CONN)

class Vali():

    @Validation.route('/PlantDetails', methods=['GET', 'POST'])
    def PlantDetails():

        plantId = session.get('plantId', None)
        dateUpdateInt = session.get('dateUpdateInt', None)
        plantName = session.get('plantName', None)
        dateUpdate = session.get('dateUpdate', None)
        LastDate = session.get('LastDate', None)
        sumAppenTot = session.get('sumAppenTot', None)
        totfirstBlockExe = session.get('totfirstBlockExe', None)
        sumTotalOut = session.get('sumTotalOut', None)
        pseudoValiExce = session.get('pseudoValiExce', None)
        exepBack = session.get('exepBack', None) 
        pseudoValiApp = session.get('pseudoValiApp', None)
        append = session.get('dicPseudo', None)
        insFacWork = session.get('insFacWork', None)
        user = session.get('USERNAME', None) 
 
        #pd.set_option('display.max_columns', None)
        #pd.set_option('display.max_rows', None)

        #try:

        #Plant Details
        totfirstBlockExe = float(session.get('totfirstBlockExe', None))
        totSecBlockExe = float(session.get('totSecBlockExe', None))
        PlantData = session.get('PlantData', None)

        daysPerYear = 365 
        weeksPerYear = 52
        daysPerWorkW = 5
        vacDaysPerY = 25
        holiPerY = 15

        #Get plant data values
        cavities = int(PlantData.loc[PlantData['key'] == 'cavities', "value"])
        seccions = int(PlantData.loc[PlantData['key'] == 'seccions', "value"])
        wPerYear = int(PlantData.loc[PlantData['key'] == 'wPerYear', "value"])
        wPerWeek = round((float(PlantData.loc[PlantData['key'] == 'wPerWeek', "value"])),2)
        wPerShift = round((float(PlantData.loc[PlantData['key'] == 'wPerShift', "value"])),2)
        shifVacDay = round((float(PlantData.loc[PlantData['key'] == 'shifVacDay', "value"])),2)
        shiftAbsent = float(PlantData.loc[PlantData['key'] == 'shiftAbsent', "value"])
        shiftOver = float(PlantData.loc[PlantData['key'] == 'shiftOver', "value"])
        sPerDay = int(PlantData.loc[PlantData['key'] == 'sPerDay', "value"]) 
        tCouHoli = round((float(PlantData.loc[PlantData['key'] == 'tCouHoli', "value"])),2)
        dayVacDay = round((float(PlantData.loc[PlantData['key'] == 'dayVacDay', "value"])),2)
        daiAbsent = float(PlantData.loc[PlantData['key'] == 'daiAbsent', "value"]) 
        daiOver = float(PlantData.loc[PlantData['key'] == 'daiOver', "value"]) 
        opeLines = int(PlantData.loc[PlantData['key'] == 'opeLines', "value"])
        opeFur = int(PlantData.loc[PlantData['key'] == 'opeFur', "value"])
        tonPulled = int(PlantData.loc[PlantData['key'] == 'tonPulled', "value"])
        coldDec = int(PlantData.loc[PlantData['key'] == 'coldDec', "value"])
        jobChanges = int(PlantData.loc[PlantData['key'] == 'jobChanges', "value"]) 
        currLabor = float(PlantData.loc[PlantData['key'] == 'currLabor', "value"])

        #Business rules
        cavPerSec = cavities/seccions if seccions else 0
        cavMultiHE = 1.5 if cavPerSec <= 2 else 2
        cavMultiCE = 1 if cavPerSec <= 2 else 1

        jobChanW = math.ceil(int(PlantData.loc[PlantData['key'] == 'jobChanges', "value"])/(52/12))
        curentOut = round(currLabor+totfirstBlockExe,0)

        shiftWorkDaiPerY = round(-(((((wPerYear*wPerWeek)/wPerShift)-shifVacDay)/100)*shiftAbsent *100 )+(((((wPerYear*wPerWeek)/wPerShift)-shifVacDay)/100)*shiftOver*100 )+((((wPerYear*wPerWeek)/wPerShift)-shifVacDay)),0)

        shiftWorkHIndex = round((daysPerYear*sPerDay)/shiftWorkDaiPerY,2) if shiftWorkDaiPerY else 0
        workDayPerY = round(-(((tCouHoli-dayVacDay)/100)*daiAbsent*100 )+(((tCouHoli-dayVacDay)/100)*daiOver*100 )+(tCouHoli-dayVacDay),0)
        DaiWorkHIndex = round(((weeksPerYear*daysPerWorkW) - (vacDaysPerY) - holiPerY)/workDayPerY,2) if workDayPerY else 0
        
        staff = 1 
        #-------------------------
        #Appenndix C
        #-------------------------
        appenC = SQLFunctions.execute_query_SQL(con.SEL_APPEC)
        appenCLstaffLines = appenC.loc[(appenC['Type'] == 'DAILY') & (appenC['type1'] == 'Lines') & (appenC['quantity'] == opeLines) & (appenC['staff'] == staff), 'Expected'].astype(int).sum()
        appenCLstaffFurn = appenC.loc[(appenC['Type'] == 'DAILY') & (appenC['type1'] == 'Furnaces') & (appenC['quantity'] == opeFur) & (appenC['staff'] == staff), 'Expected'].astype(int).sum()
        appenCLstaffFixed = appenC.loc[(appenC['Type'] == 'DAILY') & (appenC['type1'] == 'Fixed') & (appenC['quantity'] == 1) & (appenC['staff'] == staff), 'Expected'].astype(int).sum()

        numDaiStaffWork = appenCLstaffLines+appenCLstaffFurn+appenCLstaffFixed

        appenCDaiLines = appenC.loc[(appenC['Type'] == 'DAILY') & (appenC['type1'] == 'Lines') & (appenC['quantity'] == opeLines), 'Expected'].astype(int).sum()
        appenCDaiFurn = appenC.loc[(appenC['Type'] == 'DAILY') & (appenC['type1'] == 'Furnaces') & (appenC['quantity'] == opeFur), 'Expected'].astype(int).sum()
        appenCDaiFix = appenC.loc[(appenC['Type'] == 'DAILY') & (appenC['type1'] == 'Fixed') & (appenC['quantity'] == 1), 'Expected'].astype(int).sum()

        divFork = round((tonPulled/(int(appenC.loc[(appenC['JobTitle'] == 'Logistics Forklift Drivers (FLT Drivers)'), 'Expected']))),2)
        divWare = round((tonPulled/(int(appenC.loc[(appenC['JobTitle'] == 'Warehouse Dispatch'), 'Expected']))),2)
        divMould = round((cavities/(int(appenC.loc[(appenC['JobTitle'] == 'Mould Maintenance Operator'), 'Expected']))),2)
        divCEMain = round((coldDec/(int(appenC.loc[(appenC['JobTitle'] == 'CE Maintenance (Supervisor included)'), 'Expected']))),2)
        divMachine = round((cavities/(int(appenC.loc[(appenC['JobTitle'] == 'Machine Maintenance (Supervisor included)'), 'Expected']))),2)
        numDaiHourWork = round(appenCDaiLines+appenCDaiFurn+appenCDaiFix+divFork+divWare+divMould+divCEMain+divMachine-numDaiStaffWork,0)

        appenCShifLines = appenC.loc[(appenC['Type'] == 'SHIFT') & (appenC['type1'] == 'Lines') & (appenC['quantity'] == opeLines), 'Expected'].astype(int).sum()
        appenCShifFurn = appenC.loc[(appenC['Type'] == 'SHIFT') & (appenC['type1'] == 'Furnaces') & (appenC['quantity'] == opeFur), 'Expected'].astype(int).sum()
        appenCShifFix = appenC.loc[(appenC['Type'] == 'SHIFT') & (appenC['type1'] == 'Fixed') & (appenC['quantity'] == 1), 'Expected'].astype(int).sum()
        numShiftWork = round((appenCShifLines+appenCShifFurn+appenCShifFix+math.ceil((opeLines*(cavMultiHE+cavMultiCE)))),2)

        totWorkPosi = round((numDaiStaffWork+numDaiHourWork+numShiftWork),0)
        totWorkPeo = round(((numDaiHourWork*DaiWorkHIndex)+(numShiftWork*shiftWorkHIndex)+numDaiStaffWork),0)

        jobChangesSav = jobChanges
        jobChanges = 25 if jobChanW > 25 else jobChanW
        
        jobChanCrew = int(SQLFunctions.execute_query_SQL(con.SEL_JOBW, [jobChanges]).values[0])
        totPeoInPlant = round((jobChanCrew+totWorkPeo+totSecBlockExe),0)

        MannBefExcep = round((curentOut/(jobChanCrew+totWorkPeo)),2) if round((curentOut/(jobChanCrew+totWorkPeo)),2) else 0
        purePerfMann = round((curentOut/totPeoInPlant),2) if round((curentOut/totPeoInPlant),2) else 0 

        #-------------------------
        #Appenndix D
        #-------------------------

        #Fixed
        type1 = 'Fixed'
        appenD = SQLFunctions.execute_query_SQL(con.SEL_APPEDFIXFL)
        appenDFix = appenD[(appenD['type1'] == 'Fixed')]
        appenDFix['section'] = 1

        for index, row in appenDFix.iterrows():
            if row['staff'] == False:
                if row['type'] == 'DAILY':
                    appenDFix.at[index,'expected'] = round((row['expected']*DaiWorkHIndex),1)
                elif row['type'] == 'SHIFT': 
                    appenDFix.at[index,'expected'] = round((row['expected']*shiftWorkHIndex),1)

        #print("appenDFix")
        #print(appenDFix)

        #Furnaces and Lines 
        type1 = 'Furnaces'
        type2 = 'Lines'
        appenDFurLin = appenD[(appenD['type1'] == type1) | (appenD['type1'] == type2)]
        newDFurLin = pd.DataFrame(columns=['title','type','type1','staff','expected','quantity','section'])

        for index, row in appenDFurLin.iterrows():
            if row['staff'] == True:
                if (row['type1'] == 'Furnaces' and row['quantity'] == opeFur) or (row['type1'] == 'Lines' and row['quantity'] == opeLines):
                    newRow = {'title': row['title'], 'type': row['type'], 'type1': row['type1'], 'staff': row['staff'], 'expected': row['expected'], 'quantity': row['quantity'], 'section':1}
                    newDFurLin = newDFurLin.append(newRow, ignore_index=True)
            elif row['staff'] == False:
                if (row['type1'] == 'Furnaces' and row['quantity'] == opeFur) or (row['type1'] == 'Lines' and row['quantity'] == opeLines):
                    if row['type'] == 'DAILY':
                        newVal = round((row['expected']*DaiWorkHIndex),2)
                    elif row['type'] == 'SHIFT': 
                        newVal = round((row['expected']*shiftWorkHIndex),2)
                    newRow = {'title': row['title'], 'type': row['type'], 'type1': row['type1'], 'staff': row['staff'], 'expected': newVal, 'quantity': row['quantity'], 'section':1}
                    newDFurLin = newDFurLin.append(newRow, ignore_index=True)
        #print("newDFurLin")
        #print(newDFurLin)

        #Formulas
        type1 = 'Formula'
        appenDFormu = appenD[(appenD['type1'] == type1)]
        appenDFormu['section'] = 1

        for index, row in appenDFormu.iterrows():
            if row['title']=='Shift Forming Operators':
                appenDFormu.at[index,'expected'] = round((opeLines*cavMultiHE),0)*shiftWorkHIndex
            elif row['title']=='Shift Selecting Cold End Operators':
                appenDFormu.at[index,'expected'] = round((opeLines*cavMultiCE),0)*shiftWorkHIndex
            elif row['title']=='Logistics Forklift Drivers (FLT Drivers)' or row['title']=='Warehouse Dispatch':
                appenDFormu.at[index,'expected'] = round(((tonPulled/row['expected'])*DaiWorkHIndex),2)
            elif row['title']=='Mould Maintenance Operator' or row['title']=='Machine Maintenance (Supervisor included)':
                appenDFormu.at[index,'expected'] = round(((cavities/row['expected'])*DaiWorkHIndex),2)
            elif row['title']=='CE Maintenance (Supervisor included)':
                appenDFormu.at[index,'expected'] = round(((coldDec/row['expected'])*DaiWorkHIndex),2)
        #print("appenDFormu")
        #print(appenDFormu)

        #Other
        otherDic = {'title':'Resort', 'type':np.nan, 'type1':np.nan, 'staff':np.nan, 'expected':0, 'quantity':1, 'section':3}
        Other = pd.DataFrame(otherDic, index=[0])

        #Cero
        secOne = {'title':con.LIST_SECLISTCERO, 'type':np.nan, 'type1':np.nan, 'staff':np.nan, 'expected':0, 'quantity':1, 'section':1}
        newsecOneCero = pd.DataFrame(secOne)
        d = {'title':con.LIST_APPENDCERO, 'type':np.nan, 'type1':np.nan, 'staff':np.nan, 'expected':0, 'quantity':1, 'section':4}
        newAppenDCero = pd.DataFrame(d)

        #JobChanges
        jobChangesT = SQLFunctions.execute_query_SQL(con.SEL_JOBCHANGES,[jobChanges])
        jobChangesT['section']=2 

        #Exception
        exeption = session.get('exepBack', None)
        exeption = pd.DataFrame.from_dict(exeption) 
        i = exeption[((exeption.IdCategory == 1)&(exeption.Role == 'Other'))].index
        j = exeption[((exeption.IdCategory == 1)&(exeption.Role == 'Gardening'))].index
        exeption = exeption.drop(i)
        exeption = exeption.drop(j) 

        alloName = SQLFunctions.execute_query_SQL(con.SEL_ALLONAME)
        alloIdName = alloName[['laborAllocationRoleId','title']]
        alloName = alloName[['title','type','type1','staff','quantity']]
        mergeAlloExep = pd.merge(left=alloName, right=exeption[['Role','employees']], left_on='title', right_on='Role', how='inner').drop(columns=['Role'])
        mergeAlloExep.rename(columns={'employees':'expected'}, inplace = True) 
        newExcep = mergeAlloExep[['title','type','type1','staff','expected','quantity']]
        newExcep['section']=4
        
        #Final AppendixD
        dfList = [appenDFix, newDFurLin, appenDFormu, Other, newsecOneCero, newAppenDCero, jobChangesT, newExcep]
        appendD = pd.concat(dfList)
        appendD =  appendD.reset_index(drop=True)

        jobTitle = SQLFunctions.execute_query_SQL(con.SEL_JOBTITLE)
        FacWork = insFacWork[['tempHeadCount','staffHeadCount','dailyShiftHourlyHeadCount','dailyHourlyHeadCount','laborAreaId','laborRoleId']]
        FacWork['Actual'] = FacWork[['tempHeadCount','staffHeadCount','dailyShiftHourlyHeadCount','dailyHourlyHeadCount']].sum(axis=1)
        FacWork = FacWork.drop(columns=['tempHeadCount','staffHeadCount','dailyShiftHourlyHeadCount','dailyHourlyHeadCount'])
        mergeTitleFac = pd.merge(left=jobTitle, right=FacWork, left_on=['laborAreaId','LaborRoleId'], right_on=['laborAreaId','laborRoleId'], how='left').drop(columns=['laborAreaId','LaborRoleId','laborRoleId'])
        groupTitleFac = mergeTitleFac.groupby(['JobTitle','Section']).sum()
        groupTitleFac = groupTitleFac.reset_index()
        groupTitleFac['JobTitle'] = groupTitleFac['JobTitle'].astype(str)
        groupTitleFac['Section'] = pd.to_numeric(groupTitleFac['Section'])
        #print(groupTitleFac)

        appendD['title'] = appendD['title'].astype(str)
        appendD['section'] = pd.to_numeric(appendD['section'])
        merAppedDNewTitle = pd.merge(left=appendD[['title','expected','section']], right=groupTitleFac[['JobTitle','Section','Actual']], left_on=['title','section'], right_on=['JobTitle','Section'], how='left').drop(columns=['JobTitle','Section'])
        merAppedDNewTitle['Actual'] = merAppedDNewTitle['Actual'].replace(np.nan, 0, inplace=False)

        mergeIdTitle = pd.merge(left=merAppedDNewTitle, right=alloIdName, on='title', how='left')

        secRole = SQLFunctions.execute_query_SQL(con.SEL_SECALLOROLE)
        mergeExpActuTre = pd.merge(left=mergeIdTitle, right=secRole, left_on=['section','laborAllocationRoleId'], right_on=['laborSectionId','laborAllocationRoleId'], how='left').drop(columns=['title','section','laborAllocationRoleId','laborSectionId'])
        mergeExpActuTre['dateId'] = dateUpdateInt
        mergeExpActuTre['populationDate'] = datetime.now()
        mergeExpActuTre['plantId'] = plantId
        mergeExpActuTre.rename(columns={'Actual':'actualManning','expected':'expectedManning'}, inplace = True)
        #print("mergeExpActuTre")
        #print(mergeExpActuTre)
        session['allocation'] = mergeExpActuTre            
     
        #-----------------
        #MontlyR
        #-----------------
        mr = {'plantId':[plantId], 'dateId':[dateUpdateInt], 'totalOpFurnaces':[opeFur], 'totalOpProductionLines':[opeLines], 'totalSections':[seccions], 'totalCavities':[cavities], 
        'maxDailyTonnesPulled':[tonPulled], 'totalColdEndDetectionDevices':[coldDec], 'totalJobChanges':[jobChangesSav], 'currentLabor':[currLabor], 'shiftAbsenteeismRate':[shiftAbsent],
        'shiftOverTimeRate':[shiftOver] ,'dailyAbsenteeismRate':[daiAbsent] , 'dailyOvertimeRate':[daiOver], 'purePerformanceManningIndex':[purePerfMann],
        'populationDate':[datetime.now()], 'jobChangeCrew':[jobChanCrew] , 'shiftWorkers':[numShiftWork], 'dailyStaffWorkers':[numDaiStaffWork],
        'dailyHourlyWorkers':[numDaiHourWork], 'totalExceptionsB2':[totSecBlockExe], 'totalExceptionsB1':[totfirstBlockExe],  'shiftWorkedHoursIndex':[shiftWorkHIndex], 
        'shiftWorkingDaysYear':[shiftWorkDaiPerY], 'dailyWorkedHoursIndex':[DaiWorkHIndex], 'dailyWorkingDaysYear':[workDayPerY], 'jobChangesWeek':[jobChanW], 'cavitiesSectionMCE': [cavMultiCE],
        'cavitiesSectionMHE':[cavMultiHE]}

        insMontlyR = pd.DataFrame(mr)
        session['insMontlyR'] = insMontlyR
        
        #Validations
        if abs(float(currLabor) - float(sumAppenTot)) < 1 :
            currVsAppe = True
        else: 
            currVsAppe = False

        if abs(round((float(totfirstBlockExe)),1) - round((float(sumTotalOut)),1)) < 1:
            ExeVsAppeOut = True
        else: 
            ExeVsAppeOut = False

        pseudoValiExce = pseudoValiExce[pseudoValiExce.IdValidation.notnull()]
        exepBack = exepBack[['Pseudo','employees','IdCategory']]
        pseudoValiExce = pd.merge(left=pseudoValiExce, right=exepBack, on='Pseudo', how='left')

        pseudoValiApp = pseudoValiApp[pseudoValiApp.IdValidation.notnull()]
        append = append[['Pseudo',"tempHeadCount","staffHeadCount","dailyShiftHourlyHeadCount","dailyHourlyHeadCount",'outsorceHeadCount']]

        append['tempHeadCount'] = append['tempHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        append['staffHeadCount'] = append['staffHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        append['dailyShiftHourlyHeadCount'] = append['dailyShiftHourlyHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        append['dailyHourlyHeadCount'] = append['dailyHourlyHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)
        append['outsorceHeadCount'] = append['outsorceHeadCount'].replace('', np.nan, inplace=False).fillna(0).astype(float)

        pseudoValiApp = pd.merge(left=pseudoValiApp, right=append, on='Pseudo', how='left')

        noMatched = pd.DataFrame(columns=['pseudo','exepRole','employee','appendRole','appendix'])

        for index, row in pseudoValiExce.iterrows():
            idValidation = row['IdValidation']
            sumExcep = row['employees']

            #if idValidation == 27:
            #    setAppendOther = pseudoValiApp.loc[pseudoValiApp['IdValidation']==41,['Pseudo','laborRoleName','IdValidation',"tempHeadCount","staffHeadCount","dailyShiftHourlyHeadCount","dailyHourlyHeadCount",'outsorceHeadCount']]
            #    setAppend = pseudoValiApp.loc[pseudoValiApp['IdValidation']==idValidation,['Pseudo','laborRoleName','IdValidation',"tempHeadCount","staffHeadCount","dailyShiftHourlyHeadCount","dailyHourlyHeadCount",'outsorceHeadCount']]
            #    setAppend = pd.concat([setAppendOther,setAppend])
            #    print(setAppend)
            #else:
            setAppend = pseudoValiApp.loc[pseudoValiApp['IdValidation']==idValidation,['Pseudo','laborRoleName','IdValidation',"tempHeadCount","staffHeadCount","dailyShiftHourlyHeadCount","dailyHourlyHeadCount",'outsorceHeadCount']]

            if row['IdCategory'] == 1:
                sumAppend = setAppend['outsorceHeadCount'].sum()
                sumAppendFour = 0
            else:
                sumAppendTemp = setAppend['tempHeadCount'].sum()
                sumAppendStaff = setAppend['staffHeadCount'].sum()
                sumAppendShif = setAppend['dailyShiftHourlyHeadCount'].sum() 
                sumAppendHour = setAppend['dailyHourlyHeadCount'].sum()
                if idValidation == 27 or idValidation == 15 or idValidation == 13 or idValidation == 14 :
                    sumOutsour = setAppend['outsorceHeadCount'].sum()
                    sumAppendFour = [sumAppendTemp,sumAppendStaff,sumAppendShif,sumAppendHour,sumOutsour]
                else:
                    sumAppendFour = [sumAppendTemp,sumAppendStaff,sumAppendShif,sumAppendHour]
                sumAppendFour = sum(sumAppendFour)

            if ((row['IdCategory'] == 1) and (abs(sumExcep-sumAppend) > 0.2)) or ((row['IdCategory'] != 1) and (sumAppendFour < sumExcep)):
                noMatchAppend = ''
                for index, rowA in setAppend.iterrows():
                    if noMatchAppend == '':
                        noMatchAppend += rowA['laborRoleName']
                    else:
                        noMatchAppend += "  " + '-' "  "+ rowA['laborRoleName']
                if row['IdCategory'] == 1:
                    newRow = {'pseudo':row['Pseudo'],'exepRole':row['Role'],'employee':sumExcep,'appendRole':noMatchAppend,'appendix':sumAppend}
                else: 
                    newRow = {'pseudo':row['Pseudo'],'exepRole':row['Role'],'employee':sumExcep,'appendRole':noMatchAppend,'appendix':sumAppendFour}
                noMatched = noMatched.append(newRow, ignore_index=True)

        noMatched = noMatched.set_index('pseudo').T.to_dict('list')

        if len(noMatched) <= 0:
            exepAppenVali = True
        else: 
            exepAppenVali = False

        #except:
        #    e = str(sys.exc_info()[0])
        #    insError = [[user,plantId,dateUpdateInt,e,datetime.now(),'/PlantDetails']]
        #    insError = DataFrame(insError,columns=['User','PlantID','DateId','Error','DateRow', 'Comment'])
        #    insError.to_sql('ErrorLog', schema='dw', con=con.engine, if_exists='append', index=False)

        return render_template('validation.html', plantName=plantName, dateUpdate=dateUpdate, LastDate=LastDate, currVsAppe=currVsAppe, ExeVsAppeOut=ExeVsAppeOut, exepAppenVali=exepAppenVali, noMatched=noMatched, currLabor=currLabor, sumAppenTot=sumAppenTot, totfirstBlockExe=totfirstBlockExe, sumTotalOut=sumTotalOut)

    @Validation.route('/GetPlantDetails', methods=['GET', 'POST'])
    def GetPlantDetails():

        plantId = session.get('plantId', None)
        dateUpdateInt = session.get('dateUpdateInt', None)
        plantName = session.get('plantName', None)
        dateUpdate = session.get('dateUpdate', None)
        LastDate = session.get('LastDate', None)
        user = session.get('USERNAME', None)

        #try:

        if request.form['action'] == 'backAppend':

            insLog = [[user,plantId,dateUpdateInt,'Back Appendix',datetime.now()]]
            insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
            insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)

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

            return render_template('appendix.html', plantName=plantName, dateUpdate=dateUpdate, LastDate=LastDate, AMgmt = AMgmt, ABatchFurnt = ABatchFurnt, AForming = AForming, AMachinRepa = AMachinRepa, AMoldRepa = AMoldRepa, ALehr = ALehr, ASelCol = ASelCol, AQuaAssu = AQuaAssu, AColdEnd = AColdEnd, ABuiMain = ABuiMain, ALogis=ALogis, AOther = AOther, AAdmin = AAdmin)


        message = True
        
        #except:
        #    e = str(sys.exc_info()[0])
        #    insError = [[user,plantId,dateUpdateInt,e,datetime.now(),'/GetPlantDetails']]
        #    insError = DataFrame(insError,columns=['User','PlantID','DateId','Error','DateRow', 'Comment'])
        #    insError.to_sql('ErrorLog', schema='dw', con=con.engine, if_exists='append', index=False)

        try:
            message = True
            
            DelRows = SQLFunctions.execute_statement_SQL(con.DEL_FACT_EXEP,[dateUpdateInt, plantId])
            insExeption = session.get('insExeption', None)
            print(insExeption)
            insExeption.to_sql('', schema='dbo', con=con.engine, if_exists='append', index=False)

            insLog = [[user,plantId,dateUpdateInt,'Insert FactExceptions',datetime.now()]]
            insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
            insLog.to_sql('', schema='dw', con=con.engine, if_exists='append', index=False)

            DelRows = SQLFunctions.execute_statement_SQL(con.DEL_FACT_WORK,[dateUpdateInt, plantId])
            insFacWork = session.get('insFacWork', None)
            insFacWork = insFacWork[['plantId','dateId','laborAreaRoleId','tempHeadCount','staffHeadCount','dailyShiftHourlyHeadCount','outsorceHeadCount','otherHeadCount','populationDate','dailyHourlyHeadCount','Comments']]
            print(insFacWork)
            insFacWork.to_sql('', schema='dbo', con=con.engine, if_exists='append', index=False)

            insLog = [[user,plantId,dateUpdateInt,'Insert FactWorksheet',datetime.now()]]
            insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
            insLog.to_sql('', schema='dw', con=con.engine, if_exists='append', index=False)

            DelRows = SQLFunctions.execute_statement_SQL(con.DEL_ALLOCA,[dateUpdateInt, plantId])
            insAlloca = session.get('allocation', None)
            insAlloca = insAlloca[['plantId','dateId','laborSectionRoleId','actualManning','expectedManning','populationDate']]
            print(insAlloca)
            insAlloca.to_sql('', schema='dbo', con=con.engine, if_exists='append', index=False)

            insLog = [[user,plantId,dateUpdateInt,'Insert FactAllocation',datetime.now()]]
            insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
            insLog.to_sql('', schema='dw', con=con.engine, if_exists='append', index=False)

            DelRows = SQLFunctions.execute_statement_SQL(con.DEL_MONTHR,[dateUpdateInt, plantId])
            insMontlyR = session.get('insMontlyR', None)
            insMontlyR = insMontlyR[['plantId', 'dateId', 'totalOpFurnaces', 'totalOpProductionLines', 'totalSections', 'totalCavities', 
                'maxDailyTonnesPulled', 'totalColdEndDetectionDevices', 'totalJobChanges', 'currentLabor', 'shiftAbsenteeismRate',
                'shiftOverTimeRate','dailyAbsenteeismRate', 'dailyOvertimeRate', 'purePerformanceManningIndex',
                'populationDate', 'jobChangeCrew', 'shiftWorkers', 'dailyStaffWorkers','dailyHourlyWorkers', 'totalExceptionsB2', 
                'totalExceptionsB1',  'shiftWorkedHoursIndex','shiftWorkingDaysYear', 'dailyWorkedHoursIndex', 'dailyWorkingDaysYear', 
                'jobChangesWeek', 'cavitiesSectionMCE','cavitiesSectionMHE']]
            insMontlyR.to_sql('FactMonthlyReportRD', schema='dbo', con=con.engine, if_exists='append', index=False)

            insLog = [[user,plantId,dateUpdateInt,'Insert FactMonthlyReport',datetime.now()]]
            insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
            insLog.to_sql('', schema='dw', con=con.engine, if_exists='append', index=False)

            DelRows = SQLFunctions.execute_statement_SQL(con.DEL_PLANTA,[dateUpdateInt, plantId])
            insPlantA = session.get('PlantData', None)
            insPlantA.rename(columns={"key": "name"}, inplace = True)
            print(insPlantA)
            insPlantA.to_sql('', schema='dw', con=con.engine, if_exists='append', index=False)

            insLog = [[user,plantId,dateUpdateInt,'Insert PlantData_A',datetime.now()]]
            insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
            insLog.to_sql('', schema='dw', con=con.engine, if_exists='append', index=False)
        except:
            message = False
            e = str(sys.exc_info()[0])
            insError = [[user,plantId,dateUpdateInt,e,datetime.now(),'/InsertTables']]
            insError = DataFrame(insError,columns=['User','PlantID','DateId','Error','DateRow', 'Comment'])
            insError.to_sql('ErrorLog', schema='dw', con=con.engine, if_exists='append', index=False)

        
        session.pop("USERNAME", None)
        session.pop("plantId", None)
        session.pop("dateUpdateInt", None)
        session.pop("dateUpdate", None)
        session.pop("LastDate", None)
        session.pop("sumAppenTot", None)
        session.pop("totfirstBlockExe", None)
        session.pop("sumTotalOut", None)
        session.pop("pseudoValiExce", None)
        session.pop("exepBack", None)
        session.pop("pseudoValiApp", None)
        session.pop("dicPseudo", None)
        session.pop("insFacWork", None)
        session.pop("dicPseudo", None)
        session.pop("TreArea", None)
        
        return render_template('finalView.html', message=message)