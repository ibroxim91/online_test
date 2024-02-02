from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    duration = models.DurationField(blank=True)
    quiz_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Question(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images", blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        if self.id is None:
            self.category.quiz_count += 1
            self.category.save()
    
    def delete(self,*args,**kwargs):
        obj = super().delete(*args, **kwargs)
        self.category.quiz_count -= 1
        self.category.save()



class Variant(models.Model):
    question = models.ForeignKey(Question,  on_delete=models.CASCADE ,related_name='variants')
    title = models.CharField(max_length=255)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Result(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    score = models.PositiveIntegerField(default=0)
    success = models.PositiveIntegerField(default=0)
    fail = models.PositiveIntegerField(default=0)
    end = models.BooleanField(default=False)
 
    def __str__(self):
        return self.user.first_name
    
    def user_info(self):
        return f"{self.user.username} {self.user.last_name}"

class History(models.Model):
    result = models.ForeignKey(Result,  on_delete=models.CASCADE ,related_name='history')
    question = models.ForeignKey(Question,  on_delete=models.CASCADE)
    user_variant = models.ForeignKey(Variant, null=True ,  on_delete=models.CASCADE)
    is_marked = models.BooleanField(default=False)
    number = models.PositiveIntegerField("Tartibi")

    def __str__(self):
        return f"{self.result.user.first_name} javoblar tarixi"




