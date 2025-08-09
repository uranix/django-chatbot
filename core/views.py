from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.adapter import YaRuAdapter


@login_required
def home(request):
    uid = request.user.socialaccount_set.all()[0].uid
    return render(request, 'home.html', context={
        'uid': uid,
    })


oauth2_login = OAuth2LoginView.adapter_view(YaRuAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(YaRuAdapter)
