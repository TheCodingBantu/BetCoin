import requests

from all_funcs import get_results, get_odds, place_bet

URL = "http://127.0.0.1:8000/bets/"

class Bet:

    def __init__(self, stake, odds, target, progression, result, profit, balance):
        self.stake = stake
        self.odds = odds
        self.target = target
        self.progression = progression
        self.result = result
        self.profit = profit
        self.balance = balance

    def __str__(self) -> str:
        return (self.profit)


    def post_to_api(self):
        try:
            jsonData = {"progression": self.progression, "result": self.result, "stake": self.stake,
                        "odds": self.odds, "target": self.target, "profit": self.profit, "balance": self.balance}
            post = requests.post(URL, data=jsonData)
            return (post.text)
        except:
            print('exception')

# declare the objects
prg_1 = Bet('', '', '', '', '', '', '')
prg_2 = Bet('', '', '', '', '', '', '')


def save_results(stake,odds,target,progression,result,profit,balance):
    atrrs = {'stake': stake, 'odds': odds, 'target': target,
             'progression': progression, 'result': result, 'profit': profit, 'balance': balance}
    list(map(lambda item: setattr(prg_1, *item), atrrs.items()))
    response = prg_1.post_to_api()
    print(response)


def calculate_stake(odd,prog):
    stakes=[]
    # get last profit
    if(prog==0):
        profit = int(prg_1.profit)
        target = int(prg_1.target)
        balance = int(prg_1.balance)
        prev_result=prg_1.result
    elif(prog==1):
        profit = prg_2.profit
        target = int(prg_2.target)
        balance = prg_2.balance
        prev_result=prg_2.result
            
    # if the profit is positive, stop the session
    if((profit) >= 0):
        print(profit)
        # start new session
        stake=((1/balance)/(odd-1))
        stakes.append((stake))
        print('Profit gained, Starting new session')
        return stakes
        
        # if prev result was a loss
    if(profit < 0 and prev_result==0):
        stake=((((abs(profit)+target)/2))/(odd-1))
        stakes.append(stake)
        return stakes
    
    if(prev_result==1 and profit < 0):
        stake=(profit+target)/(odd-1)
        stakes.append(stake)
        return stakes

# gets initial data from database and populates the created objects
def get_last_result(progression):
    r = requests.get(url=URL+str(progression))
    try:
        data = (r.json())[0]
        atrrs = {'stake': data['stake'], 'odds': data['odds'], 'target': data['target'], 'progression': progression,
                 'result': data['result'], 'profit': data['profit'], 'balance': data['balance']}
        if (progression == 0):
            list(map(lambda item: setattr(prg_1, *item), atrrs.items()))
        elif (progression == 1):
            list(map(lambda item: setattr(prg_2, *item), atrrs.items()))
    except:
        return None


def main():
    pass
    # save_results(8.75,1.4,3.5,0,1,-5.25,1001.5)
    
    # get_last_result(0)

   
    # # # get odds from the selected teams (all_funcs)
    # odd_one=get_odds()[0]
    # odd_two=get_odds()[1]
    
    # # #calculate stakes and call a method from all_funcs
    # stake_one=calculate_stake(odd_one,0)
    # print(stake_one)
    # # stake_two=calculate_stake(odd_two,1)
    
    # # # results=place_bet(stake_one,stake_two)
    # # # print()
    # # # # save_results()


if __name__ == "__main__":
    main()
