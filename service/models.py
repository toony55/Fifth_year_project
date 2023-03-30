from django.db import models
from django.contrib.auth import get_user_model 
from django.utils import timezone
from django.db.models import Sum, Count


User=get_user_model()




class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='certificates/')

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255)
    percent = models.CharField(max_length=255)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    parent = models.ForeignKey('self',null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    description = models.TextField(default='category_example',blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True,default='images/1.png', null=True)
    is_featured = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name



class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='categories',blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_time = models.IntegerField(help_text='Enter delivery time in days')
    revisions = models.IntegerField(default=0, help_text='Enter the number of revisions included in the service')
    is_taken=models.BooleanField(default=False)   
    samples = models.URLField(help_text='Enter a link to samples of previous work',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

   
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.title


class SellService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='Sell_categories',blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_time = models.IntegerField(help_text='Enter delivery time in days')
    revisions = models.IntegerField(default=0, help_text='Enter the number of revisions included in the service')
    is_taken=models.BooleanField(default=False)   
    samples = models.URLField(help_text='Enter a link to samples of previous work',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

   
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sellservices')

    def __str__(self):
        return self.title
    



class Request(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DENIED = 'denied'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DENIED, 'Denied'),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_requests')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_requests')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.service} ({self.status})'
    

class SellRequest(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DENIED = 'denied'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DENIED, 'Denied'),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_request')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_request')
    service = models.ForeignKey(SellService, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.service} ({self.status})'
    
class Rating(models.Model):
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    rating_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    value = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rating_user.username} did rate {self.rated_user.username}'
    

class Block(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.blocker.username} did block {self.blocked.username}'