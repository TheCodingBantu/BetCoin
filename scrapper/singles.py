import requests
from decimal import Decimal


URL = "http://127.0.0.1:8000/bets/"

def get_last_result():
    r = requests.get(url=URL)
    try:
        data = (r.json())[0]
        return data
    except:
        return None
    
    
def post_to_api(result,stake,odds,total_lost):
        try:
            jsonData = {"result": result, "stake": stake,"odds": odds,"total_lost": total_lost}
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
        result=input('Enter match result (w/l)')
        if(result=='w'):
            total_lost=0
            # restart the progression
            prev_result=''
            return [prev_result,stake,result,total_lost]
        elif(result=='l'):
            total_lost=stake
            prev_result='l'
            return [prev_result,stake,result,total_lost]
            
    
    if(prev_result=='w'):
        result=input('Enter match result (w/l)')
        stake=round((Decimal((total_lost+initial_target)/odds)),2)
        if(result=='w'):
            total_lost= 0
            # restart the progression
            prev_result=''
            return [prev_result,stake,result,total_lost]
            
        elif(result=='l'):
            total_lost=stake
            prev_result='l'
            return [prev_result,stake,result,total_lost]
            
              
    if(prev_result=='l'):
        result=input('Enter match result (w/l)')
        stake=round((Decimal(((total_lost+initial_target)/2)/odds)),2)
        if(result=='w'):
            total_lost=round((Decimal(abs((Decimal(stake) * Decimal(odds))-Decimal(total_lost)))),2) 
            # restart the progression
            prev_result='w'
            return [prev_result,stake,result,total_lost]
              
        elif(result=='l'):
            total_lost = round(Decimal(total_lost)+ Decimal(stake),2)
            prev_result='l'
            return [prev_result,stake,result,total_lost]
 
              
def main():
    # post_to_api(1,3,1.4,0)
    while True:
        val=place_bet(0.8)
        post_to_api(val[2],val[1],1.8,val[3])
        
   
if __name__=='__main__':
    main()





    
    
