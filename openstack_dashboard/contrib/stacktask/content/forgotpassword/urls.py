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

import os

from django.conf.urls import patterns
from django.conf.urls import url
from horizon import loaders

from openstack_dashboard.contrib.stacktask.content.forgotpassword import views

urlpatterns = patterns(
    '',
    url(r'^/?$', views.ForgotPasswordView.as_view(), name='forgot-index'),
    url(r'^sent/?$', views.password_sent_view, name='forgot-sent'),
)

# NOTE(dale): Hack to register our template directory as searchable
# This is required as we do not register /token/ as a real Horizon panel
# and so horizon.base.Dashboard.register is never called.
token_dir = os.path.dirname(__file__)
template_dir = os.path.join(token_dir, "templates")
if os.path.exists(template_dir):
    loaders.panel_template_dirs['stacktask/forgotpassword'] = template_dir
