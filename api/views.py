from django.shortcuts import render
from collections import Counter


from rest_framework.views import APIView
from api.models import Bet
from api.serializer import BetSerializer
from rest_framework.response import Response
from rest_framework import status


class BetList(APIView):
    def get(self, request):
        # returns complex Data type
        bets = Bet.objects.all().order_by('-id')
        # convert to python data structre using the serializer
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LatestBet(APIView):
    def get(self, request, pk):
        # returns complex Data type
        bets = Bet.objects.filter(progression=pk).order_by('-id')
        # convert to python data structre using the serializer
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data)


def History(request):
    # returns complex Data type
    bets = Bet.objects.all().order_by('-id')
    return render(request, 'index.html', {'bets': bets})


def Graphs(request):
    bet_one = []
    bet_two = []
    one_losses = Bet.objects.filter(progression=0).filter(result='l').count()
    one_draws = Bet.objects.filter(progression=0).filter(result='d').count()
    one_wins = Bet.objects.filter(progression=0).filter(result='w').count()

    two_losses = Bet.objects.filter(progression=1).filter(result='l').count()
    two_draws = Bet.objects.filter(progression=1).filter(result='d').count()
    two_wins = Bet.objects.filter(progression=1).filter(result='w').count()

    bet_one.extend((one_wins, one_draws, one_losses))
    bet_two.extend((two_wins, two_draws, two_losses))

    win_count_one = get_wins(Bet.objects.filter(progression=0))[0]
    win_count_two = get_wins(Bet.objects.filter(progression=1))[0]

    win_dates_one = []
    win_data_one=[]
    
    win_dates_two = []
    win_data_two=[]
    
    # get date for each confirmed win
    all_dates_one = Bet.objects.filter(progression=0)
    all_dates_two = Bet.objects.filter(progression=1)

    for index, i in enumerate(all_dates_one):
        for j in (get_wins(Bet.objects.filter(progression=0))[1]):
            if (index == j):
                win_dates_one.append(i.date_created.strftime("%Y-%m-%d %H:%M:%S"))
                
    # count similar dates
    c = Counter()
    c.update(win_dates_one) 
    for v in c.values():
        win_data_one.append(v)
        
    for index, i in enumerate(all_dates_two):
        for j in (get_wins(Bet.objects.filter(progression=0))[1]):
            if (index == j):
                win_dates_two.append(i.date_created.strftime("%Y-%m-%d %H:%M:%S"))
                
    # count similar dates
    c = Counter()
    c.update(win_dates_two) 
    for v in c.values():
        win_data_two.append(v)
        
    return render(request, 'graphs.html', 
                  {'one': bet_one, 'two': bet_two, 
                   'win_count_one': win_count_one, 'win_count_two': win_count_two, 
                   'win_dates_one': win_dates_one,'win_data_one':win_data_one,
                   'win_dates_two': win_dates_two,'win_data_two':win_data_two})

def get_wins(results):
    my_list = []
    dates = []
    if(len(results)>0):
        for i in results:
            my_list.append(i.result)

        count = 0
        length = []
        if len(my_list) > 1:
            for i in range(1, len(my_list)):
                if (my_list[i] == 'w' or my_list[i] == 'd'):
                    if my_list[i-1] == 'w' or my_list[i-1] == 'd':
                        count += 1
                length.append(count)
                count = 0
        else:
            return 0

        wins = 0
        for i in range(len(length)):
            if (length[i] == 1):
                dates.append((i+1))
                wins += length[i]

        return ([wins, dates])
    else:
        return ['']

