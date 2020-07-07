from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['user__username', 'user__email']
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)