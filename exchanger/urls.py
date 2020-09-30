from django.conf.urls import url
from . import views


urlpatterns=[
    url('^exchange/$', views.ExchangeViewSet, name='list'),
    url('^retrieve/$', views.RetrieveFormView, name='retrieve'),
]