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

  