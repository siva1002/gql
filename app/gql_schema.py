import graphene
from app.django_schema import CategoriesSchema,UserSchema
from graphene_django.filter import DjangoFilterConnectionField
from app.models import Category
from app.mutation import Mutation
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

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

    def resolve_greet(self,info,*args,**kwargs):
        return "Hello 6"

class CategoryQuery(graphene.ObjectType):
    category=graphene.Node.Field(CategoriesSchema)
    all_categories=graphene.List(CategoriesSchema)

    def resolve_all_categories(root,info,*args,**kwargs):
        return Category.objects.all()

class UsersQuery(graphene.ObjectType):
    all_user=graphene.Field(UserPagination,page=graphene.Int())

    def resolve_all_user(root,info,page=1,*args,**kwargs):
        print(root,"root")
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

