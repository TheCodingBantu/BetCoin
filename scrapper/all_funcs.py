
def get_odds():
    return [1.40,1.42]

def place_bet(stake_one,stake_two):
    return False

def get_results():
    pass

#algo
'''
variables:

initial_target=1
new_target=0
total_lost=0

start progression:
place_bet(stake)

if win on the first try,
    total_lost=0
    new_target=0
    start_progression()
  
    
if lose on first try:
    total_lost=stake
    new_target=(total_lost+initial_target)/2
    

if win (any time except first)
    if(prev_result=Win)
        total_lost= profit-total_lost
        new_target=0
        start_progression()
        
    if(prev_result=Loss)
        total_lost=profit-total_lost
        new_target=total_lost+initial_target
       
       
if lose(any time except first):
    total_lost += this_stake
    new_target=(total_lost+initial_target)/2
    
    
'''