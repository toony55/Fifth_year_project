from django.db import models
from django.contrib.auth import get_user_model 

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
    name = models.CharField(max_length=50)
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
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.title