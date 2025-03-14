import graphene
from graphene import InputObjectType

class UserInput(InputObjectType):
    username=graphene.String()
    email=graphene.String(required=True)
    password=graphene.String(required=True)



