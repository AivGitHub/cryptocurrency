from abc import ABC

from rest_framework import serializers

from cryptocurrency.models import Wallet, Coin


class CoinSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=256)
    symbol = serializers.CharField(max_length=8)

    class Meta:
        model = Coin
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    address = serializers.CharField(max_length=36)
    public_key_hex = serializers.CharField(max_length=256)
    coin = CoinSerializer(many=False, read_only=True)
    child = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Wallet
        fields = '__all__'
