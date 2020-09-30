from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns=[
    url('^$', views.index, name='index'),
    url(r'^upload/balance', views.upload_balance, name='upload_balance'),
    url(r'^$', views.get_balance, name='balance'),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('balance/<int:pk>/', views.BalanceDetail.as_view()),
    path('movements/', views.MovementList.as_view()),
    path('movements/<int:pk>/', views.MovementDetail.as_view()),
]

