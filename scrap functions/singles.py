import requests
from decimal import Decimal
from datetime import datetime
import random

URL = "http://127.0.0.1:8000/bets/"

def get_last_result():
    r = requests.get(url=URL)
    try:
        data = (r.json())[0]
        return data
    except:
        return None
    
    
def post_to_api(result,stake,odds,total_lost):
    now = datetime.now()
    prog=random.randint(0,1)
    try:
        jsonData = {"progression":0,"result": result, "stake": stake,"odds": odds,"total_lost": total_lost,"date_created":now}
        requests.post(URL, data=jsonData)
        return True
    except:
        print('exception')
        return False
            
          
# start progression:
def place_bet(odds):
    
    data=get_last_result()
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
        stake=round((Decimal(initial_target/odds)),2)
        result=input('Enter match result (w/l/d)')
        if(result=='w' or result=='d'):
            total_lost=0
            # restart the progression
            prev_result=''
            return [prev_result,stake,result,total_lost]
        elif(result=='l'):
            total_lost=stake
            prev_result='l'
            return [prev_result,stake,result,total_lost]
            
    
    if(prev_result=='w' or prev_result=='d'):
        result=input('Enter match result (w/l/d)')
        stake=round((Decimal((total_lost+initial_target)/odds)),2)
        if(result=='w' or result=='d'):
            total_lost= 0
            # restart the progression
            prev_result=''
            return [prev_result,stake,result,total_lost]
            
        elif(result=='l'):
            total_lost=stake
            prev_result='l'
            return [prev_result,stake,result,total_lost]
            
              
    if(prev_result=='l'):
        result=input('Enter match result (w/l/d)')
        stake=round((Decimal(((total_lost+initial_target)/2)/odds)),2)
        if(result=='w' or result=='d'):
            total_lost=round((Decimal(abs((Decimal(stake) * Decimal(odds))-Decimal(total_lost)))),2) 
            # restart the progression
            prev_result='w' or prev_result=='d'
            return [prev_result,stake,result,total_lost]
              
        elif(result=='l'):
            total_lost = round(Decimal(total_lost)+ Decimal(stake),2)
            prev_result='l'
            return [prev_result,stake,result,total_lost]
 
              
def main():
    # post_to_api(1,3,1.4,0)
    while True:
        val=place_bet(0.44)
        post_to_api(val[2],val[1],1.44,val[3])
        
   
if __name__=='__main__':
    main()





    
    
