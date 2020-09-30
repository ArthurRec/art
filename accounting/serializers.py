from rest_framework import serializers
from .models import Balance, Transaction, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class BalanceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Balance
        fields = ('id', 'total_amount', 'currency',)


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='user.id')
    addressee = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Transaction
        fields = ('id', 'description', 'amount', 'date', 'sender', 'addressee')

    def create(self, validated_data):
        transaction = Transaction(
            description=validated_data['description'],
            amount=validated_data['amount'],
            date=validated_data['sender'],
            user=validated_data['addressee']
        )
        transaction.save()

        return transaction
