from django.contrib import admin
from store.models import Brand,Tag,Size,Category,Product

from store.models import User

# Register your models here.

admin.site.register(Brand)
admin.site.register(Tag)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Product)

admin.site.register(User)
