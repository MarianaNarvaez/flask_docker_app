import sys

from numpy.core.fromnumeric import var
#sys.path.insert(1, '/var/www/app/OIInsightsFramework')
sys.path.insert(1, './OIInsightsFramework')
#sys.path.insert(1, '')
from ExceptionR import ExceptionR, Except
from Appendix import Appendix, Append
from Validation import Validation, Vali
from flask import Flask, render_template, url_for, request, redirect, session, current_app
#from flask.ext.session import Session
from flask_session import Session
import Config as con
import os
from pandas import DataFrame
import numpy as np
import pandas as pd
from datetime import datetime 
import calendar
from LdapAuthentication import LdapAuthentication
from SQLFunctions import SQLFunctions
import logging
from gevent.pywsgi import WSGIServer
#import requests 


app = Flask(__name__)
app.register_blueprint(Validation)
app.register_blueprint(Appendix)
app.register_blueprint(ExceptionR)

#Logging capabilities
logging.basicConfig(level=logging.DEBUG)

SQLFunctions = SQLFunctions(con.CONN) 
message = True

#Show initial page
@app.route('/', methods=['GET', 'POST'])
def Login():
    typeLogin = 1
    return render_template('login.html', typeLogin=typeLogin)

#Validate loggin
@app.route('/headerLoggin', methods=['GET', 'POST'])
def headerLoggin():

    domain = request.form.get('domain')
    user = request.form.get('user')
    session["USERNAME"] = user
    password = request.form.get('password')
    #Assign active directory group according to Region
    if domain == '':
        group = ''
    elif domain == '':
        group = ''
    elif domain == '':
        group = ''
    elif domain == '':
        group = ''
    elif domain == '':
        group = ''

    ##Validate login according to user, password and region 
    LdapAuth = LdapAuthentication(domain, user, password, group)
    #authenticate: Valid user in Owens 
    #authorized: The user has access to the group
    authenticate, authorized = LdapAuth.ldap_group_auth()
    #Get plants which user has access
    plantsListDF = SQLFunctions.execute_query_SQL(con.LIST_OF_PLANTS,[user])
    #Dataset with only plant names
    plantsList = plantsListDF['PlantName']
    #Store variables in session
    session["plantsList"] = plantsList
    session["plantsListDF"] = plantsListDF

    #If dataset is empty the user doesn't has acess to any plant
    if len(plantsListDF) <= 0:
        accessPlants = False
    else: 
        accessPlants = True

    showPlant = False
    showDate = False

    #If the user is authenticated, authorized and has access to plants then show the page to choose a plant
    if authenticate and authorized and accessPlants:
        user = user.lower().strip()
        insLog = [[user,np.nan,np.nan,'Login',datetime.now()]]
        insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
        #insert data in log
        insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)
        return render_template('header.html', plantsList=plantsList, showPlant=showPlant, showDate=showDate)
    elif not authenticate and authorized == None:
        typeLogin = 2
        return render_template('login.html', typeLogin=typeLogin)
    elif authenticate and not authorized:
        typeLogin = 3
        return render_template('login.html', typeLogin=typeLogin)
    elif authenticate and authorized and accessPlants == False:
        typeLogin = 4
        return render_template('login.html', typeLogin=typeLogin)

#Choose Plant, date and show Plant Data page
@app.route('/plantData', methods=['GET', 'POST'])
def plantData():
        
    showPlant = False
    showDate = False

    plantsList = session.get('plantsList', None)
    plantsListDF = session.get('plantsListDF', None)

    user = session.get('USERNAME', None) 

    if request.form['action'] == 'Search':  
        plantName = request.form.get('plantsList')
    else:
        plantName = request.form.get('plantName')

    #Get plantId of plant chose
    plantId = int(plantsListDF.loc[plantsListDF['PlantName'] == plantName, 'plantId'])

    #If Go back:
    if request.form['action'] == 'Back':
        insLog = [[user,plantId,np.nan,'Back to Plant',datetime.now()]]
        insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
        insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)
        #Insert log 
        return render_template('header.html', plantsList=plantsList, showPlant=showPlant, showDate=showDate)

    showPlant = True
    showDate = True   

    #select last date of data storage for that plant
    LastDate = SQLFunctions.execute_query_SQL(con.LAST_DATE_PLANT, [plantId])
    #Convert last date into string
    LastDateStr = str(LastDate['LasDate'].values[0])
    #Get year
    lastYear = int(LastDateStr[0:4])
    #Convert last date selected into date format
    LastDateCast = datetime(year=lastYear, month=int(LastDateStr[4:6]), day=int(LastDateStr[6:8])).date()
    #Convert date into format "Jul 2021"
    LastDate = calendar.month_abbr[int(LastDateStr[4:6])] +" "+ LastDateStr[0:4]

    MonthToFill = int(LastDateStr[4:6])
    #Calculate month to fill:
    #Month to fill is a month next that the last month loaded
    #If monthToFill = currentMonth then monthToFill = monthToFill because due to business rule, a month is available just if it month is already finished
    #if the year changed set January like the month to fill
    if (MonthToFill < (datetime.now().month)-1 or (datetime.now().year) > lastYear):
        MonthToFill = MonthToFill + 1

    if MonthToFill <= 12 : 
        yearToFill = lastYear
    else:
        yearToFill = datetime.now().year
        MonthToFill = 1

    newLastDate = datetime( 
        year=int(yearToFill), month=MonthToFill, day=1).date()
    newLastDateInt = int(
        str(newLastDate)[0:4]+str(newLastDate)[5:7]+str(newLastDate)[8:10])
    newDate = {'dateId': [newLastDateInt], 'dateIdCast': [newLastDate], 'newFormListDate':calendar.month_abbr[MonthToFill] +" "+ str(int(yearToFill))}
    newDateDf = pd.DataFrame(newDate, columns=['dateId', 'dateIdCast', 'newFormListDate'])

    #list of dates
    listDatPlant = SQLFunctions.execute_query_SQL(con.LIST_DATES_PLANT, [int(plantId), int(plantId), int(plantId)])
    listDatPlant['dateIdCast'] = listDatPlant['dateId'].astype(str).astype(int)
    listDatPlant['dateIdCast'] = pd.to_datetime(listDatPlant['dateIdCast'], format='%Y%m%d').dt.date
    listDatPlantShow = listDatPlant
    listDatPlantShow['newFormListDate'] = ''

    #Cast dates into format "Jul 2021"
    for index, row in listDatPlant.iterrows():
        listDatPlantShow.at[index,'newFormListDate'] = calendar.month_abbr[int(row['dateIdCast'].month)] +" "+ str(int(row['dateIdCast'].year)) 

    if newLastDate > LastDateCast:
        listDatPlantShow = pd.concat([newDateDf, listDatPlantShow]).sort_values(by='dateId', ascending=False)

    if request.form['action'] == 'Search':
        insLog = [[user,plantId,np.nan,'Search Plant',datetime.now()]]
        insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
        #Insert action into log
        insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)
        return render_template('header.html', plantName=plantName, listDates=listDatPlantShow['newFormListDate'], LastDate=LastDate, showPlant=showPlant,showDate=showDate)

    #Get date selected
    dateUpdate = request.form.get('listDates')
    month = datetime.strptime(str(dateUpdate)[0:3], "%b")
    dateUpteBack = datetime(int(str(dateUpdate)[4:8]), month.month, 1, 0, 0)
    dateUpdateInt = int(dateUpteBack.strftime('%Y%m%d'))

    labelsA = con.LABELSA
    labelsB = con.LABELSB

    #Get information regarding to plant data 
    selPlantData = SQLFunctions.execute_query_SQL(con.SEL_MONTHLYR , [dateUpdateInt,plantId])
    blockAPlanD =  SQLFunctions.execute_query_SQL(con.SEL_PLANTDATA , [dateUpdateInt,plantId])

    #if the information for that month doesn't exist then it brings the data of the previous month
    if len(blockAPlanD) <= 0 or len(selPlantData) <= 0 :
        if MonthToFill == 1:
            MonthPreLoad = 12
            yearPreLoad = yearToFill-1
        else:
            MonthPreLoad = MonthToFill-1
            yearPreLoad = yearToFill
        DatePreLoad = datetime(year=int(yearPreLoad), month=MonthPreLoad, day=1).date()
        IntPreLoad = int(str(DatePreLoad)[0:4]+str(DatePreLoad)[5:7]+str(DatePreLoad)[8:10])
        selPlantData = SQLFunctions.execute_query_SQL(con.SEL_MONTHLYR , [IntPreLoad,plantId])
        blockAPlanD =  SQLFunctions.execute_query_SQL(con.SEL_PLANTDATA , [IntPreLoad,plantId])  

    #Set stored values in the dictionaries
    for key, value in labelsA.items(): 
        val = blockAPlanD.loc[blockAPlanD['Name']==key, 'Value'].values[0]
        value[2] = val
    
    for key, value in labelsB.items():  
        column = value [2]
        try:
            if key == 'shiftAbsent' or key == 'shiftOver' or key == 'daiAbsent' or key == 'daiOver':
                value[3] = round((float(selPlantData[column].values[0])*100),2)
            else:
                value[3] =  float(selPlantData[column].values[0])
        except:
            value[3] = ''

    insLog = [[user,plantId,dateUpdateInt,'Search Date',datetime.now()]]
    insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
    insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)

    session['labelsA'] = labelsA 
    session['labelsB'] = labelsB
    session['listDatPlantShow'] = listDatPlantShow
    session['plantId'] = plantId
    session['dateUpdateInt'] = dateUpdateInt
    session['MonthToFill'] = month.month
    session['yearToFill'] = yearToFill
    session['LastDateStr'] = LastDateStr
    session['plantName'] = plantName
    session['dateUpdate'] = dateUpdate
    session['LastDate'] = LastDate
    session['finApp'] = False

    if not session.get("dicPseudo") is None:
        session.pop('dicPseudo')
    if not session.get("exepBack") is None:
        session.pop('exepBack')

    #except:
    #    e = str(sys.exc_info()[0])
    #    if 'dateUpdateInt' in locals():
    #        pass
    #    else:
    #        dateUpdateInt = np.nan
    #    insError = [[user,plantId,dateUpdateInt,e,datetime.now(),'/plantData']]
    #    insError = DataFrame(insError,columns=['User','PlantID','DateId','Error','DateRow', 'Comment'])
    #    insError.to_sql('ErrorLog', schema='dw', con=con.engine, if_exists='append', index=False)


    return render_template('plantData.html', plantName=plantName, dateUpdate=dateUpdate, LastDate=LastDate, labelsA=labelsA, labelsB=labelsB)

@app.route('/getPlantData', methods=['GET', 'POST'])
def getPlantData():

    
    labelsA = session.get('labelsA', None)
    labelsB = session.get('labelsB', None)
    listDatPlantShow = session.get('listDatPlantShow', None)
    plantId = session.get('plantId', None)
    dateUpdateInt = session.get('dateUpdateInt', None)

    #try:
    if request.form['action'] == 'Back':
        showPlant = True
        showDate = True
        plantName = session.get('plantName', None)
        LastDate = session.get('LastDate', None)
        return render_template('header.html', plantName=plantName, listDates=listDatPlantShow['newFormListDate'], LastDate=LastDate, showPlant=showPlant,showDate=showDate)

    dflabelsA = pd.DataFrame(columns = ["key", "label","name","value"])
    dflabelsB = pd.DataFrame(columns = ["key", "label","name","value"])

    #Get the new data for plant data A and B section
    for key, value in labelsA.items():
        val = request.form.get(value[1])
        value[2] = val
        if val == '':
            val = 0
        arg = [key, value[0], value[1], val]
        SerlabelsA = pd.Series(arg, index=dflabelsA.columns)
        dflabelsA = dflabelsA.append(SerlabelsA, ignore_index=True)
        
    for key, value in labelsB.items():
        val = request.form.get(value[1])
        value[3] = val
        if val == '':
            val = 0
        if key == 'shiftAbsent' or key == 'shiftOver' or key == 'daiAbsent' or key == 'daiOver':
            try:
                val = float(val)/100
            except:
                val = 0
        arg = [key, value[0], value[1], val]
        SerlabelsB = pd.Series(arg, index=dflabelsB.columns)
        dflabelsB = dflabelsB.append(SerlabelsB, ignore_index=True)

    #Store data Plant Data in session variables 
    session['labelsA'] = labelsA 
    session['labelsB'] = labelsB 

    plantData = pd.concat([dflabelsA, dflabelsB]).reset_index(drop=True)

    plantData['value'] = plantData['value'].replace('', np.nan, inplace=False).fillna(0).astype(float)
    plantData['plantId'] = plantId
    plantData['dateId'] = dateUpdateInt
    plantData['populationDate'] = datetime.now()
    

    PlantData = plantData[['label','value','key','plantId','dateId','populationDate']]
    session['PlantData'] = PlantData

    user = session.get('USERNAME', None)
    insLog = [[user,plantId,dateUpdateInt,'Go Exception',datetime.now()]]
    insLog = DataFrame(insLog,columns=['User','PlantId','DateSelected','Action','DateRow'])
    insLog.to_sql('Log', schema='dw', con=con.engine, if_exists='append', index=False)

    #except:
    #    e = str(sys.exc_info()[0])
    #    insError = [[user,plantId,dateUpdateInt,e,datetime.now(),'/getPlantData']]
    #    insError = DataFrame(insError,columns=['User','PlantID','DateId','Error','DateRow', 'Comment'])
    #    insError.to_sql('ErrorLog', schema='dw', con=con.engine, if_exists='append', index=False)

    return redirect(url_for('ExceptionR.ExceptionRep'))


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    ##app.config['SESSION_TYPE'] = 'filesystem'
    #sess = session()
    #sess.init_app(app)
    #app.run(host="0.0.0.0", debug=True, port=8080)
    SESSION_TYPE = 'filesystem'
    app.config.from_object(__name__)

    sess = Session()
    sess.init_app(app)

    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()
        
