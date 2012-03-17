from django import forms
from django.forms.forms import BoundField, BaseForm
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm

from frontend.models import Article
from personal.models import UserProfile

class BootstrapForm(BaseForm):
    def as_bootstrap(self):
        rows = []
        for field_name, field in self.fields.iteritems():
            bound_field = BoundField(self, field, field_name)

            rows.append(u'''
<div class="control-group %(errors_class)s">
    <label class="control-label" for="id_%(field_name)s">%(field_label)s</label>
    <div class="controls">
        %(widget)s
        %(errors_list)s
        %(help_text)s
    </div>
</div>
''' % {
                'errors_class': u'error' if bound_field.errors else u'',
                'field_name': field_name,
                'field_label': field.label,
                'widget': unicode(bound_field),
                'errors_list': u'<span class="help-inline">%s</span>' % u', '.join(bound_field.errors) if bound_field.errors else u'',
                'help_text': u'<span class="help-inline">%s</span>' % escape(field.help_text) if field.help_text else u''
            })

        return mark_safe(u'<fieldset>%s</fieldset>' % u''.join(rows))


class ArticleForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = Article
        fields = ['name', 'slug', 'raw_text', 'created']


class UserForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = UserProfile
        fields = ['personal_url', 'custom_hostname']

class CustomPasswordChangeForm(PasswordChangeForm, BootstrapForm):
    pass


class CustomAuthenticationForm(AuthenticationForm, BootstrapForm):
    pass