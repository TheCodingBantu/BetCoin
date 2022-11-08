
from django.contrib import admin
from django.urls import path
from api.views import BetList,LatestBet,History,Graphs

urlpatterns = [
    # path('',BetList.as_view() ),
    path('',History,name='history' ),
    path('graphs/',Graphs ,name='graphs'),
    path('<int:pk>',LatestBet.as_view() ),
]

