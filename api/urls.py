from django.urls import path

from api.views import WalletViews

urlpatterns = [
    path('wallet/', WalletViews.as_view()),
    path('wallet/<int:address_id>', WalletViews.as_view()),
]
