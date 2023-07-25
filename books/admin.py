from django.contrib import admin

# Register your models here.
from .models import* 



admin.site.register([Book,
BookReview])

@admin.register(PostedBook)
class PostedBookAdmin(admin.ModelAdmin):
    list_display=["book","book_position"]
    list_editable=["book_position"]