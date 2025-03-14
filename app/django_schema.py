from graphene_django import DjangoObjectType
from app.models import Category,Ingredients
from graphene import relay
from django.contrib.auth import get_user_model

User=get_user_model()

class CategoriesSchema(DjangoObjectType):
    class Meta:
        model=Category
        interfaces=(relay.Node,)
        filter_fields={'name':['icontains']}

class IngredientsSchema(DjangoObjectType):
    class Meta:
        model=Ingredients
        interfaces=(relay.Node,)
        filter_fields={"name":['icontains']}

class UserSchema(DjangoObjectType):
    class Meta:
        model=User
        fields="__all__"

    
#     @classmethod
#     def get_queryset(cls, queryset, info):
#         print(queryset)
#         queryset=Ingredients.objects.all()
#         return super().get_queryset(queryset, info)
    