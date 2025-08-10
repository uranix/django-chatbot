from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.adapter import YaRuAdapter
from functools import wraps


def require_perm(relation, domain):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            account = request.user.socialaccount_set.all()[0]
            uid = f'{account.uid}/{account.provider}'
            if not request.check_perm(uid, relation, domain):
                return render(request, '403.html', status=403, context={
                    'uid': uid,
                    'relation': relation,
                    'domain': domain
                })
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@login_required
@require_perm(relation="member", domain="chatbot")
def home(request):
    uids = [f'{account.uid}/{account.provider}' for account in request.user.socialaccount_set.all()]
    return render(request, 'home.html', context={
        'uid': ', '.join(uids),
    })


def login(request):
    return render(request, 'login.html')


oauth2_login = OAuth2LoginView.adapter_view(YaRuAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(YaRuAdapter)
