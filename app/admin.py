from django.contrib import admin
from .models import profile,bio,post,follow
# Register your models here.
admin.site.register(profile)
admin.site.register(bio)
admin.site.register(post)
admin.site.register(follow) 

