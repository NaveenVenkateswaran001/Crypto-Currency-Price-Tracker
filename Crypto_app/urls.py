from django.urls import path
from Crypto_app import views


urlpatterns = [
    
    path('',views.home,name='home'),
    path('allcoins/',views.coins,name='coins'),
    path('mywallet/',views.myWallet,name='myWallet'),
    path('addcoin/<str:coin_id>/',views.addCoin,name='addCoin'),
    path('deletecoin/<str:coin_id>/',views.deleteCoin,name='deleteCoin'),
]
