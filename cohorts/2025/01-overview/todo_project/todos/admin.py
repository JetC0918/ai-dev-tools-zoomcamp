from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'is_resolved')
    list_filter = ('is_resolved', 'due_date')
    search_fields = ('title', 'description')
    ordering = ('due_date',)

admin.site.register(Todo, TodoAdmin)