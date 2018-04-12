from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

# required for django 2.0
app_name = "users"

urlpatterns = [
    path('', views.UserAccountView.as_view(), name='account'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('account/', views.UserAccountView.as_view(), name='account'),
]


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
