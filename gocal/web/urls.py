from django.conf.urls import url

import gocal.web.views


urlpatterns = [
    url(r'^$', gocal.web.views.calculate, name='calculate_expression'),
]
