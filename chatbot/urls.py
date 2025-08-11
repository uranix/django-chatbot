from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.urls import path
from core.views import home, login
from core.chat import chat_api
from core.provider import YaRuProvider
from allauth.socialaccount.providers.google.provider import GoogleProvider


urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('api/chat', chat_api)
]

urlpatterns += default_urlpatterns(YaRuProvider)
urlpatterns += default_urlpatterns(GoogleProvider)
