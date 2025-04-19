from graphene import Mutation
import graphene
from app.input_schema import UserInput
from app.gql_schema import UserSchema
from django.contrib.auth import get_user_model,authenticate,login
from django.core.cache import cache
from app.forms import UserForm
from graphene_django.forms.mutation import DjangoModelFormMutation,ErrorType
User=get_user_model()
from graphql import GraphQLError
class UserCreate(DjangoModelFormMutation):
    errors=graphene.List(ErrorType,required=False)
    message=graphene.String()
    class Meta:
        form_class=UserForm
    
    @classmethod
    def perform_mutate(cls,form,root,*args,**kwargs):
        user=form.save()
        print(user)
        return UserCreate(message="USER CREATED",errors=[])

class UserUpdate(DjangoModelFormMutation):
    message=graphene.String(default_value='Updated')
    class Meta:
        form_class=UserForm
    
    @classmethod
    def perform_mutate(cls,form,root,*args,**kwargs):
        user_details=form.cleaned_data
        print(user_details)
        return UserUpdate()


class LoginUser(Mutation):
    class Arguments:
        email=graphene.String(required=True)
        password=graphene.String(required=True)
    
    user=graphene.Field(UserSchema)
    message=graphene.Field(graphene.String)


    def mutate(root,info,email,password,*args,**kwargs):
        block_user=cache.get(f"blocked_{email}")
        key=f"spam_{email}"
        if block_user:
            return UserCreate(message="User blocked")
        user=authenticate(
            info.context,
            username=email,
            password=password
            )
        if user:
            login(request=info.context,
                  user=user)
            cache.delete(key)
            return LoginUser(message="Logged in Successfully",user=user)
        suser=cache.get(key)
        if not suser:
            cache.set(key,1,timeout=60)
            return LoginUser(message=f"Attempts remaining 4")
        if suser < 4:
            cache.incr(f"spam_{email}")
            return LoginUser(message=f"Attempts remaining {5-cache.get(key)}")
        cache.set(f"blocked_{email}",1,timeout=300)
        return LoginUser(message="User Blocked")

class Mutation(graphene.ObjectType):
    create_user=UserCreate.Field()
    login=LoginUser.Field()
    user_update=UserUpdate.Field()

