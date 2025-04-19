import graphene,enum
from app.django_schema import CategoriesSchema,UserSchema
from graphene_django.filter import DjangoFilterConnectionField
from app.models import Category
from app.mutation import Mutation
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model


class Options(enum.Enum):
    OPTION_1='Option 1'
    OPTION_2='Option 2'

    @classmethod
    def options(cls):
        return (i.value for i in cls)

User=get_user_model()
class UserPagination(graphene.ObjectType):
    total_pages=graphene.Int()
    has_next=graphene.Boolean()
    has_prev=graphene.Boolean()
    users=graphene.List(UserSchema)

    def resolve_total_pages(self,*args,**kwargs):
        print(self,args)

class GraphSchema(graphene.ObjectType):
    greet=graphene.String()
    validate_token=graphene.Field(graphene.String,token=graphene.String())

    def resolve_greet(self,info,*args,**kwargs):
        token=default_token_generator.make_token(info.context.user)
        print(token)
        return "Hello"
    def resolve_validate_token(self,info,token,*args,**kwds):
        token=default_token_generator.check_token(info.context.user,token)
        print(token)
        return 'Hello'

class CategoryQuery(graphene.ObjectType):
    category=graphene.Node.Field(CategoriesSchema)
    all_categories=graphene.List(CategoriesSchema)

    def resolve_all_categories(root,info,*args,**kwargs):
        return Category.objects.all()

class UsersQuery(graphene.ObjectType):
    all_user=graphene.Field(UserPagination,page=graphene.Int())

    def resolve_all_user(root,info,page=1,*args,**kwargs):
        users=User.objects.all()
        userspage=Paginator(users,per_page=1)
        paginator=userspage.page(number=int(page))
        return {
            "users":paginator.object_list,
            "total_pages":userspage.num_pages,
            "has_next":paginator.has_next(),
            "has_prev":paginator.has_previous()
        }

class RootSchema(GraphSchema,CategoryQuery,UsersQuery):
    pass

gql_schema=graphene.Schema(query=RootSchema,mutation=Mutation,auto_camelcase=False)

