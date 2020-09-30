from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import generics, permissions

from .forms import BalanceUploadForm
from .models import Balance, Transaction
from .models import User
from .serializers import (
    UserSerializer, BalanceSerializer, TransactionSerializer)


@login_required(login_url='/accounts/login/')
def index(request):
    title = 'Transaction'

    return render(request, 'index.html', {"title": title})


@login_required(login_url='/accounts/login/')
def upload_balance(request):
    current_user = request.user
    title = 'Upload Profile'
    try:
        requested_balance = Balance.objects.filter(
            user_id=current_user.id
        ).select_related('user').first()
        if request.method == 'POST':
            form = BalanceUploadForm(request.POST, request.FILES)

            if form.is_valid():
                requested_balance.user.email = form.cleaned_data['email']  # username
                requested_balance.save_profile()
                return redirect(get_balance)
        else:
            form = BalanceUploadForm()
    except:
        if request.method == 'POST':
            form = BalanceUploadForm(request.POST, request.FILES)

            if form.is_valid():
                new_balance = Balance(
                    total_amount=form.cleaned_data['total_amount'],
                    user=request.user,
                    currency=form.cleaned_data['currency'])
                new_balance.save_balance()
                return redirect(get_balance)
        else:
            form = BalanceUploadForm()

    return render(request, 'upload_balance.html',
                  {"title": title, "current_user": current_user, "form": form})


@login_required(login_url='/accounts/login/')
def get_balance(request):
    # current_user = request.user
    pass


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BalanceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BalanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Balance.objects.filter(user=self.request.user)


class MovementList(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovementDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
