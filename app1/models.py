from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class SubCategories(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_name= models.CharField(max_length=100)
    desc = models.TextField(max_length=255)
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE) 
    subcategories = models.ForeignKey(SubCategories,on_delete=models.CASCADE) 
    price = models.IntegerField()
    image = models.ImageField(upload_to="product_images")
    objects = models.Manager()

    def __str__(self):
        return self.product_name
    

class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class Wishlist(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Address(models.Model):
    address = models.TextField()
    pincode = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Orders(models.Model):
    order_id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=0)
    order_date = models.DateField()
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    payment_status= models.BooleanField(default=False)

