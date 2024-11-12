from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Stuff(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=20)
    price=models.IntegerField()
    detail=models.TextField(max_length=300)
    quantity=models.IntegerField(default=0)
    image=models.ImageField(upload_to="",blank=True,verbose_name='stuff_img')
    pub_date = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=10)  # 재고 필드 추가
    

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    stuffs=models.ForeignKey(Stuff,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username +' '+ self.stuffs.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)  # 주문 시간 자동 설정
    subtotal = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' ' + self.stuff.name+' '+str(self.order_date)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stuff = models.ForeignKey('Stuff', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"
