from django.contrib import admin

from .models import Category
from .models import Comment
from .models import Post
from .models import User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
