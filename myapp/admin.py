from django.contrib import admin

# Register your models here.
from .models import User, Tag, Posts, UserDetails

admin.site.register(User)
admin.site.register(UserDetails)
admin.site.register(Posts)
admin.site.register(Tag)

