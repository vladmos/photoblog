from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import ModelForm

from models import UserProfile

admin.site.unregister(User)

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile

    #def __getattribute__(self, item):
    #    print item
    #    return super(UserProfileForm, self).__getattribute__(item)

    def clean(self):
        print 'TWAT'

    def clean_custom_hostname(self):
        print 'WAT'
        hostname = self.cleaned_data['custom_hostname']
        return hostname or None

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    form = UserProfileForm

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.register(User, UserProfileAdmin)