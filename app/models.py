from django.db import models

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name
    
    @property
    def caps_name(self):
       return self.name.upper()


class Ingredients(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='ingredients',related_query_name="category")

    def __str__(self):
        return f"{self.name} {self.category.name}"