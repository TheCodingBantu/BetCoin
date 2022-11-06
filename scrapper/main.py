# import requests
# URL = "http://127.0.0.1:8000/bets/"



# def get_last_result():
#     r = requests.get(url=URL)
#     try:
#         data = (r.json())[0]
#         return data
#     except:
#         return None
    
from decimal import Decimal
val='15.05'
print(Decimal(val)) 
