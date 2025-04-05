from django.urls import path

from .views import AccountView, DepositView, TransactionView, TransferView

urlpatterns = [
    path('', AccountView.as_view(), name='account_detail'),
    path('transfer/', TransferView.as_view(), name='create_transfer'),
    path("deposit/", DepositView.as_view())
]
