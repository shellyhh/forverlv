# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from django.conf.urls import url
from views import views
urlpatterns = [
    url(r'^page/(?P<app_label>[^/]*)/(?P<model_name>[^/]*)/$', view=views.page_view),
    url(r'^grid/(?P<app_label>[^/]*)/(?P<model_name>[^/]*)/$', view=views.grid_view),
    url(r'^action/(?P<app_label>[^/]*)/(?P<model_name>[^/]*)/(?P<object_id>\d+)/$', view=views.model_view),
    url(r'^action/(?P<app_label>[^/]*)/(?P<model_name>[^/]*)/(?P<action_name>[^/]*)/$', view=views.model_action)
]