from django.contrib import admin

# Register your models here.
from .models import bid, Listing, Comment, Category, Wear

admin.site.register(bid)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Wear)

