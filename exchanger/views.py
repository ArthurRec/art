import datetime
import json

from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from exchanger.forms import RetrieveForm
from exchanger.models import Exchange
from exchanger.serializers import ExchangeSerializer


class ExchangeViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny, )

    def list(self, request):
        date = request.query_params.get('date') or datetime.date.today()
        queryset = Exchange.objects.filter(date=date)
        serializer = ExchangeSerializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveFormView(View):
    template_name = "exchanger/retrieve.html"
    form_class = RetrieveForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        data = "No data available"
        if form.is_valid():
            queryset = Exchange.objects.filter(date=form.cleaned_data['date'])
            serializer = ExchangeSerializer(queryset, many=True)
            data = json.dumps(serializer.data, indent=4)

        return render(
            request, self.template_name, {'form': form, 'data': data})
