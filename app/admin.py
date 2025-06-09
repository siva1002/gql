# from io import BytesIO
# from django.contrib import admin
# from django.shortcuts import render,redirect
# from django.urls import path
# from app.models import Category,Ingredients
# from app.forms import UploadForm
# from django.contrib import messages
# from utils.processors import ProcessExcell

# # Register your models here.

# # admin.site.register(Category)

# @admin.register(Ingredients)
# class IngredientsAdmin(admin.ModelAdmin):
#     model=Ingredients
#     change_list_template = "admin/app/ingredients/change_list.html"
#     list_display=('id','name')
#     list_display_links=("id",)
#     excell_fields={"Month",
#     "Rank",
#     "User Name",
#     "Mobile Number",
#     "No. of Days Played",
#     "No. of Games Started",
#     "Gameplay Coins",
#     "Share Coins",
#     "Referral Coins",
#     "Bonus Coins",
#     "Total Coins",
#     "Gifts"}


#     def upload_ingredients(self,request):
#         context = dict(
#                 self.admin_site.each_context(request),  # includes default admin context like site title, etc.
#                 title="Upload Winners",
#                 form=UploadForm()
#             )
#         if request.method=='POST':
#             try:
#                 file=request.FILES.get('file')
#                 name=file._name.split(".")
#                 if not name[-1] == 'xlsx':
#                     messages.error(request=request,message='Upload valid file')
#                     raise Exception("Not valid File")
#                 excel=ProcessExcell(
#                     file=file,
#                     fields=self.excell_fields
#                     ).validate()
#                 if not excel.valid_columns:
#                     messages.error(request=request,message=f"Columns mismatch found please check")
#                     messages.info(request=request,message=f"{self.excell_fields} file should contain these colums")
#                     raise Exception("Invalid Rows")

#                 if excel.invalid_rows:
#                     messages.error(request=request,message=f"Invalid rows {excel.invalid_rows}")
#                     raise Exception("Invalid Rows")
#                 return redirect("admin:upload")
#             except Exception as e:
#                 print(e)
#                 return render(request=request,template_name='upload.html',context=context)
        
#         if not request.method =='POST':            
#             return render(request=request,template_name='upload.html',context=context)
        

#     def get_urls(self):
#         add_ons=[
#             path('upload',self.upload_ingredients,name='upload')
#         ]
#         return super().get_urls()+add_ons
