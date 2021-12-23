from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import WalletSerializer
from cryptocurrency.models import Wallet, Coin


class WalletViews(APIView):

    def post(self, request) -> Response:

        _seed = request.data.get('seed', '')
        _symbol = request.data.get('symbol')

        try:
            coin = Coin.objects.get(symbol=_symbol)
        except Coin.DoesNotExist:
            return Response({"status": "error", "data": f'No Coin \'{_symbol}\' found'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            key = Wallet.get_address_from_seed(seed=_seed.encode('utf-8'))
        except ValueError:
            return Response({"status": "error", "data": f'Seed must be at least 128 bits'},
                            status=status.HTTP_400_BAD_REQUEST)

        address = key.Address()
        public_key_hex = key.PublicKey().hex()
        # Not for saving. Need to Show to user generated key
        private_key = key.PrivateKey().hex()

        request_data = [{
            'address': address,
            'public_key_hex': public_key_hex,
            'coin': 1,
            'coin_id': 1
        }]

        serializer = WalletSerializer(data=request_data, many=True, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.data}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None) -> Response:

        if id:
            wallets = Wallet.objects.filter(pk=id)
        else:
            wallets = Wallet.objects.all()

        serializer = WalletSerializer(wallets, many=True)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
