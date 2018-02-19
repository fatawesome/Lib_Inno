from django.contrib import admin

from library.models import *
from library.models.user import User


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


class RecordInline(admin.TabularInline):
    model = Record


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_price', 'display_authors', 'display_tags')
    inlines = [RecordInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('document', 'status', 'user', 'due_to', 'id')
    list_filter = ('status', 'due_to')

    fieldsets = (
        (None, {
            'fields': ('document', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'user', 'due_to')
        })
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
