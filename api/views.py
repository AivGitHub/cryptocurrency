from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import WalletSerializer
from cryptocurrency.models import Wallet, Coin
from django.db.utils import IntegrityError


class WalletViews(APIView):

    def post(self, request) -> Response:

        _seed = request.data.get('seed', '')
        _symbol = request.data.get('symbol')
        _parent = request.data.get('parent')

        try:
            coin = Coin.objects.get(symbol=_symbol)
        except Coin.DoesNotExist:
            return Response({"status": "error", "data": f'No Coin \'{_symbol}\' found'},
                            status=status.HTTP_400_BAD_REQUEST)

        request_data = {'coin': coin}

        try:
            if _parent:
                # Seed is not stored in database so firstly getting parent BIP32Key is needed
                root_key = Wallet.get_from_seed(seed=_parent.encode('utf-8'), symbol=_symbol)
                key = Wallet.get_from_seed(parent_seed=_parent.encode('utf-8'), symbol=_symbol)

                parent_wallet = Wallet.objects.get(address=root_key.Address())

                request_data.update({'parent': parent_wallet})
            else:
                key = Wallet.get_from_seed(seed=_seed.encode('utf-8'), symbol=_symbol)
        except ValueError:
            return Response({"status": "error", "data": f'Seed must be at least 128 bits'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Wallet.DoesNotExist:
            return Response({"status": "error", "data": f'No wallet (parent) found for seed \'{_parent}\''},
                            status=status.HTTP_400_BAD_REQUEST)

        address = key.Address()
        public_key_hex = key.PublicKey().hex()
        # Not for saving. Need to show to user generated key
        private_key = key.PrivateKey().hex()

        request_data.update({
            'address': address,
            'public_key_hex': public_key_hex
        })

        try:
            wallet = Wallet.objects.create(**request_data)
            wallet.save()
        except IntegrityError:
            return Response({"status": "error", "data": "Wallet already exists"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "success", "data": request.data}, status=status.HTTP_200_OK)

    def get(self, request, address_id=None) -> Response:

        if address_id:
            wallets = Wallet.objects.filter(pk=address_id)
        else:
            wallets = Wallet.objects.all()

        serializer = WalletSerializer(wallets, many=True)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
