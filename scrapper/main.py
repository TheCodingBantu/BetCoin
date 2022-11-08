import requests

URL = "http://127.0.0.1:8000/bets/"

def post_to_api(progression,result,stake,odds,total_lost):
        try:
            jsonData = {"progression":progression,"result": result, "stake": stake,"odds": odds,"total_lost": total_lost}
            requests.post(URL, data=jsonData)
            return True
        except:
            print('exception')
            return False
post_to_api(0,'w',1,1.4,0)