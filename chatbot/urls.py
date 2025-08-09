from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.urls import path, include
from core.views import home
from core.provider import YaRuProvider


urlpatterns = [
    path('', home, name='home'),
] + default_urlpatterns(YaRuProvider)
