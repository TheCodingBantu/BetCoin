import requests
from datetime import datetime
import random
from decimal import Decimal

URL = "http://127.0.0.1:8000/bets/"


def get_last_result(progression):
    LATEST_URL = "http://127.0.0.1:8000/"+progression 
    r = requests.get(url=LATEST_URL)
    try:
        data = (r.json())[0]
        return data
    except:
        return None
  
def post_to_api(progression,odds,stake,result,total_lost,balance):
    now = datetime.now()
    try:
        jsonData = {"progression":progression,"result": result, "stake": stake,"odds": odds,"total_lost": total_lost,"balance":balance,"date_created":now}
        requests.post(URL, data=jsonData)
        print('saved successfully')
        return True
    except:
        print('exception')
        return False
             
def stake_calc(odds,progression):
    data=get_last_result(progression)
    if data is None:
        initial_target=1
        total_lost=0
        prev_result=''
    else:
        initial_target=1
        prev_result=(data['result'])
        total_lost=(data['total_lost'])
     
    if(prev_result==''):
        # if we are starting a new progression
        stake=round((Decimal(initial_target/Decimal(odds))),2)
        if(stake < 1):
            stake=1
        return stake

    if(prev_result=='w' or prev_result=='d'):
        stake=round((Decimal(total_lost+initial_target)/odds),2)
        if(stake < 1):
            stake=1
        return stake
   
    if(prev_result=='l'):
        stake=round((Decimal((total_lost+initial_target)/2)/odds),2)
        if(stake < 1):
            stake=1
        return stake

def save_result(progression,odds,stake,result,balance):
    data=get_last_result(progression)
    if data is None:
        initial_target=1
        total_lost=0
        prev_result=''
    else:
        initial_target=1
        prev_result=(data['result'])
        total_lost=(data['total_lost'])
     
    if(prev_result==''):
        
        if(result=='w' or result=='d'):
            total_lost=0
            # restart the progression
            post_to_api(progression,odds,stake,result,total_lost,balance)
        elif(result=='l'):
            total_lost=stake
            post_to_api(progression,odds,stake,result,total_lost,balance)
   
    if(prev_result=='w' or prev_result=='d'):
       
        if(result=='w' or result=='d'):
            total_lost= 0
            # restart the progression
            post_to_api(progression,odds,stake,result,total_lost,balance)
           
        elif(result=='l'):
            total_lost=stake
            post_to_api(progression,odds,stake,result,total_lost,balance)
                    
              
    if(prev_result=='l'):
        
        if(result=='w' or result=='d'):
            total_lost=round((Decimal(abs((Decimal(stake) * Decimal(Decimal(odds)-Decimal(1)))-Decimal(total_lost)))),2) 
            # restart the progression
            post_to_api(progression,odds,stake,result,total_lost,balance)
            
              
        elif(result=='l'):
            total_lost = round(Decimal(total_lost)+ Decimal(stake),2)
            post_to_api(progression,odds,stake,result,total_lost,balance)
  