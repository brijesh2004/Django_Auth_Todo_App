from django.contrib import admin
from .models import TodoModel

# Register your models here.

@admin.register(TodoModel)
class TodoModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at', 'is_completed', 'user')
    search_fields = ('title', 'description')
    list_filter = ('is_completed', 'created_at')
