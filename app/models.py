from django.db import models
from django.conf import settings
# Create your models here.

class ImageUpload(models.Model):
    title = models.CharField(max_length = 100)
    pic = models.ImageField(upload_to='imageupload') #저장 디렉터리 : media/imageupload

    def __str__(self):
        return self.title

class letter(models.Model):
    letters = models.CharField(max_length=10000)

    def __str__(self):
        return self.letters

class Cos(models.Model):
    id = models.IntegerField(primary_key=True)
    brand = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    ingredient = models.TextField(blank=True, null=True)
    prdname = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cos'

# 좋아요 기능을 위한 모델.
# common.User 모델 생성후 정의할 것.
class cos_like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cos = models.ForeignKey(Cos, on_delete=models.CASCADE)

    class Meta:
        db_table='cos_like'