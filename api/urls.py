
from django.contrib import admin
from django.urls import path
from api.views import BetList,LatestBet,History,Graphs
from django.views.generic.base import TemplateView

urlpatterns = [
    path('bets/',BetList.as_view() ),
    path('',History,name='history' ),
    path('about/',TemplateView.as_view(template_name='about.html'),name='about'),
    path('graphs/',Graphs ,name='graphs'),
    path('<int:pk>',LatestBet.as_view() ),
]

