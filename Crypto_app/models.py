from django.db import models
# Create your models here

class CoinDetails(models.Model):
     coin_id = models.CharField(max_length = 17 , null = False)
     symbol = models.CharField(max_length =  10, null = False)
     image_path = models.CharField(max_length=255)
     name = models.CharField(max_length = 19 , null = False)
     current_price = models.DecimalField(max_digits=15, decimal_places =0, null=False ,default=1000)
     price_change_1h = models.DecimalField(max_digits = 5, decimal_places = 2, null = False, default=0)
     price_change_24h = models.DecimalField(max_digits = 5 ,decimal_places = 2, default = 0)
     total_volume = models.DecimalField(max_digits=15, decimal_places =0,  null = False,default=1000)
     
class MyWallet(models.Model):
     coin_id = models.CharField(max_length = 17 , null = True)
     symbol = models.CharField(max_length =  10, null = True)
     image_path = models.CharField(max_length=255)
     name = models.CharField(max_length = 19 , null = True)
     user_id = models.IntegerField(default=0)