from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry, DELETION
from library.models import *
from login.models import CustomUser
from login.forms import CustomUserCreationForm, CustomUserChangeForm

from django.utils.html import escape
from django.urls import reverse


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


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
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


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'address', 'subtype')
    list_filter = ('email',)
    fieldsets = (
        (None, {
            'fields': ('email',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'phone_number', 'address')
        }),
        ('Permissions', {
            'fields': ('groups', 'subtype')
        }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number',
                       'address', 'groups', 'subtype', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        # Return nothing to make sure user can't update any data
        pass

    readonly_fields = ('object_id', 'action_time', 'user',
                       'content_type', 'object_repr', 'change_message', 'action_flag')
    list_filter = ['action_time', 'user', 'content_type']
    ordering = ('-action_time', )

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change'
                        % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'
