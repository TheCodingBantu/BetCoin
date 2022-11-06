
from django.contrib import admin
from django.urls import path
from api.views import BetList,LatestBet,History

urlpatterns = [
    path('',BetList.as_view() ),
    path('history/',History ),
    path('<int:pk>',LatestBet.as_view() ),
]

