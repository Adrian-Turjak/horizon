# Copyright (c) 2015 Catalyst IT Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf import settings
from django.forms import ValidationError  # noqa
from django import http
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables  # noqa

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import functions as utils
from horizon.utils import validators

from openstack_dashboard import api


class PasswordForm(forms.SelfHandlingForm):
    new_password = forms.RegexField(
        label=_("New password"),
        widget=forms.PasswordInput(render_value=False),
        regex=validators.password_validator(),
        error_messages={
            'invalid': validators.password_validator_msg()
        }
    )
    confirm_password = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput(render_value=False)
    )
    no_autocomplete = True

    def clean(self):
        '''Check to make sure password fields match.'''
        data = super(forms.Form, self).clean()
        if 'new_password' in data:
            if data['new_password'] != data.get('confirm_password', None):
                raise ValidationError(_('Passwords do not match.'))
        return data

    # We have to protect the entire "data" dict because it contains
    # newpassword strings.
    @sensitive_variables('data')
    def handle(self, request, data):
        usable_data = self.cleaned_data
        user_is_editable = api.keystone.keystone_can_edit_user()

        if user_is_editable and usable_data:
            try:
                api.keystone.user_update_own_password(
                    request,
                    usable_data['current_password'],
                    usable_data['new_password']
                )
                response = http.HttpResponseRedirect(settings.LOGOUT_URL)
                msg = _("Password changed. Please log in again to continue.")
                utils.add_logout_reason(request, response, msg)
                return response
            except Exception:
                exceptions.handle(request,
                                  _('Unable to change password.'))
                return False
        else:
            messages.error(request, _('Changing password is not supported.'))
            return False


class ConfirmForm(forms.SelfHandlingForm):

    def handle(self, request, data):
        pass
