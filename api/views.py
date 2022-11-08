from django.shortcuts import render


from rest_framework.views import APIView
from api.models import Bet
from api.serializer import BetSerializer
from rest_framework.response import Response
from rest_framework import status


class BetList(APIView):
    def get(self,request):
        # returns complex Data type
        bets=Bet.objects.all().order_by('-id')
        # convert to python data structre using the serializer
        serializer=BetSerializer(bets,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=BetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class LatestBet(APIView):
    def get(self,request,pk):
        # returns complex Data type
        bets= Bet.objects.filter(progression=pk).order_by('-id')
        # convert to python data structre using the serializer
        serializer=BetSerializer(bets,many=True)
        return Response(serializer.data)

def History(request):
    # returns complex Data type
    bets=Bet.objects.all().order_by('-id')
    return render(request, 'index.html', {'bets': bets})

def Graphs(request):
    bet_one=[]
    bet_two=[]
    one_losses=Bet.objects.filter(progression=0).filter(result='l').count()
    one_draws=Bet.objects.filter(progression=0).filter(result='d').count()
    one_wins=Bet.objects.filter(progression=0).filter(result='w').count()
    
    two_losses=Bet.objects.filter(progression=1).filter(result='l').count()
    two_draws=Bet.objects.filter(progression=1).filter(result='d').count()
    two_wins=Bet.objects.filter(progression=1).filter(result='w').count()
    
    bet_one.extend((one_wins,one_draws,one_losses))
    bet_two.extend((two_wins,two_draws,two_losses))
    
    return render(request, 'graphs.html', {'one': bet_one,'two':bet_two })

  