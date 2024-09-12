from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from Crypto_app.models import CoinDetails,MyWallet
from django.contrib.auth.models import User
import requests
from django.core.mail import send_mail
# Create your views here.

coins_id=['bitcoin','ethereum','tether','binancecoin','solana','usd-coin','ripple','staked-ether','dogecoin','the-open-network']
def call_api(request):
     
     url="https://api.coingecko.com/api/v3/coins/markets"
     params={
          'ids':','.join(coins_id),
          'vs_currency':'inr',
          'per_page':10,
          'page':1,
          'price_change_percentage':'1h',
          'sparkline':False,
          'image':False          
     }
     try:
          response = requests.get(url,params=params)
          return(response.json())
     except requests.exceptions.ConnectionError:
          return HttpResponse('Connection Error Occured')
     except:
          return HttpResponse('Something Went Wrong')     

@login_required(login_url='loginForm')
@csrf_protect
def home(request):
     return render(request,'home.html')

def sendMail(coin,user_id,latest_price):
     user = User.objects.get(id = user_id)
     if latest_price < 0:
          latest_price = (latest_price) * (-1)

     send_mail(
          subject = f'Price Drop Alert for {coin.name}',
          message = f"Dear {user.username.capitalize()},\n\nWe hope this message finds you well!\n\nWe have a great news for you! The price of {coin.name} has just Dropped. This could be the perfect opportunity to buy!\n\nDetails:\n\n   Coin: {coin.name}\n   Price Drop by: {(latest_price)}%\n\nThank you for being a valued member of our community!\n\nBest Wishes,\nThe Crypto Radar Team",           
          from_email='Crypto Radar <n8103836@gmail.com>',
          recipient_list=[user.email],
          fail_silently=False
     )
     
def checkPrice(current_coins_prices,user_id):
     my_coin = MyWallet.objects.filter(user_id = user_id)
     if my_coin:
          for coin in my_coin:
               for symbol,value in current_coins_prices.items():
                    if coin.symbol == symbol:
                         latest_price = CoinDetails.objects.filter(symbol=coin.symbol).values_list('price_change_1h',flat=True).first()
                         if latest_price < current_coins_prices[symbol]:
                              sendMail(coin,user_id,latest_price)
                              break
                         else:
                              continue
     else:
          pass               

def updateCoins(data,user_id):
     no_of_coins = CoinDetails.objects.all().count()
     if no_of_coins == 0:
          for coin in data:
               CoinDetails.objects.create(
                    coin_id = coin['id'],
                    symbol = coin['symbol'],
                    name = coin['name'],
                    current_price = coin['current_price'],
                    price_change_24h = coin['price_change_24h'],
                    total_volume = coin['total_volume'] 
               )
     else:
          running=True
          while(running):
               
               current_coins_prices={
                    'btc':CoinDetails.objects.filter(symbol='btc').values_list('price_change_1h',flat=True).first(),
                    'eth':CoinDetails.objects.filter(symbol='eth').values_list('price_change_1h',flat=True).first(),
                    'usdt':CoinDetails.objects.filter(symbol='usdt').values_list('price_change_1h',flat=True).first(),
                    'bnb':CoinDetails.objects.filter(symbol='bnb').values_list('price_change_1h',flat=True).first(),
                    'sol':CoinDetails.objects.filter(symbol='sol').values_list('price_change_1h',flat=True).first(),
                    'usdc':CoinDetails.objects.filter(symbol='usdc').values_list('price_change_1h',flat=True).first(),
                    'xrp':CoinDetails.objects.filter(symbol='xrp').values_list('price_change_1h',flat=True).first(),
                    'steth':CoinDetails.objects.filter(symbol='steth').values_list('price_change_1h',flat=True).first(),
                    'doge':CoinDetails.objects.filter(symbol='doge').values_list('price_change_1h',flat=True).first(),
                    'ton':CoinDetails.objects.filter(symbol='ton').values_list('price_change_1h',flat=True).first()
               }
     
               for i,latest_data in enumerate(data):
                    CoinDetails.objects.filter(coin_id = coins_id[i]).update(
                         current_price = latest_data['current_price'],
                         total_volume = latest_data['total_volume'],
                         price_change_24h = latest_data['price_change_percentage_24h'],
                         price_change_1h = latest_data['price_change_percentage_1h_in_currency']
                    )
                    
               checkPrice(current_coins_prices,user_id)     
               running=False

                             
@login_required(login_url='loginForm')
@csrf_protect
def coins(request):
     user_id = request.user.id         
     if request.method =='POST':     
          data = call_api(request)
          updateCoins(data,user_id)
          updated_data = CoinDetails.objects.filter().all().order_by('id')     
          return render(request,'coins.html',{'data':updated_data})
     else:
          updated_data = CoinDetails.objects.filter().all().order_by('id')     
          return render(request,'coins.html',{'data':updated_data})
     
@login_required(login_url='loginForm')
@csrf_protect
def myWallet(request):
     my_coins = MyWallet.objects.filter(user_id = request.user.id)
     return render(request,'my_coin.html',{'mycoin':my_coins})


@login_required(login_url='loginForm')
@csrf_protect
def addCoin(request,coin_id):
     coin = CoinDetails.objects.get(coin_id = coin_id)
     coinExists = MyWallet.objects.filter(user_id = request.user.id, coin_id = coin_id).exists()
     if not coinExists:
          MyWallet.objects.create(
               coin_id = coin.coin_id,
               symbol = coin.symbol,
               image_path = coin.image_path,
               name = coin.name,
               user_id = request.user.id    
               )
          myCoin = MyWallet.objects.filter(user_id = request.user.id)
          return render(request,'my_coin.html',{'mycoin':myCoin})
     else:
          myCoin = MyWallet.objects.filter(user_id = request.user.id)
          return render(request,'my_coin.html',{'mycoin':myCoin})
          

          
@login_required(login_url='loginForm')
@csrf_protect
def deleteCoin(request,coin_id):
     MyWallet.objects.filter(user_id = request.user.id, coin_id = coin_id).delete()
     return redirect('myWallet')
     