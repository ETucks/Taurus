from django.db import models

# Create your models here.
class Stock(models.Model):
    """
    Model representing a stock
    """
    name = models.CharField(max_length=200, help_text="Enter a stock")
    current_price = models.DecimalField(..., max_digits=5, decimal_places=2)
    day_change = models.DecimalField(..., max_digits=5, decimal_places=2)
    bid = models.CharField(max_length=200)
    ask = models.CharField(max_length=200)
    day_range = models.CharField(max_length=200)
    week_range_52 = models.CharField(max_length=200)
    volume = models.IntegerField()
    avg_volume = models.IntegerField()
    market_cap = models.CharField(max_length=200)
    beta = models.DecimalField(..., max_digits = 4, decimal_places = 2)
    pe_ratio = models.DecimalField(..., max_digits = 4, decimal_places = 2)
    eps = models.DecimalField(..., max_digits = 4, decimal_places = 2)
    earnings_date = models.CharField(max_length=200)
    for_div_yield = models.CharField(max_length=200)
    ex_div_date = models.CharField(max_length=200)
    year_target_est = models.DecimalField(..., max_digits = 4, decimal_places = 2)    

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Crypto(models.Model):
    """
    Model representing a cryptocurrency
    """
    name=models.CharField(max_length=200, help_text="Enter a cryptocurrency")
    current_price = models.DecimalField(..., max_digits=5, decimal_places=2)
    day_change = models.DecimalField(..., max_digits=5, decimal_places=2)
    market_cap = models.CharField(max_length=200)
    circulating_supply=models.CharField(max_length=200)
    max_supply = models.CharField(max_length=200)    
    volume = models.IntegerField()
    volume_24h = models.CharField(max_length=200)
    volume_24h_all = models.CharField(max_length=200)

#class NeuralNets(models.Model):
#    """
#    Model representing neural networks for various stocks and cryptocurrencies
#    """
#    name = models.CharField(max_length=200, help_text="Enter a stock or cryptocurrency")
#    weights = ArrayField()
