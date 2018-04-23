from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.admin import helpers

from library.models import *
from login.models import CustomUser
from login.forms import CustomUserCreationForm, CustomUserChangeForm


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
            'fields': ('user_permissions', 'groups', 'subtype')
        }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number',
                       'address', 'groups', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


    def get_or_create_group(self, name):
        if Group.objects.filter(name=name).count() != 0:
            return Group.objects.get(name=name)
        group = Group.objects.create(name=name)
        return group

    def _changeform_view(self, request, object_id, form_url, extra_context):

        ret = super()._changeform_view(self, request, object_id, form_url, extra_context)

        model = self.model
        opts = model._meta

        if request.method == 'POST' and '_saveasnew' in request.POST:
            object_id = None

        obj = self.get_object(request, unquote(object_id), to_field)

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)


        print(obj.groups.all())

        obj.groups.clear()
        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                if form.cleaned_data['subtype'] == 'Librarians':
                    obj.groups.add(self.get_or_create_group('Librarians'))
                elif form.cleaned_data['subtype'] == 'Students':
                    obj.groups.add(self.get_or_create_group('Students'))
                elif form.cleaned_data['subtype'] == 'Visiting Professors':
                    obj.groups.add(self.get_or_create_group('Visiting Professors'))
                else: # if self.cleaned_data['subtype'] equal 'Instructors' or 'TAs' or 'Professors'
                    obj.groups.add(self.get_or_create_group('Faculty'))


        print(obj.groups.all())
        obj.save()

        print(obj.groups.all())

        print('\n\n\n\n\nAFSDGSHDMFJDNSBEAWFGt\n\n\n\n\n')
        print(form.cleaned_data)

        return ret
