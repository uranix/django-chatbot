import requests

from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from core.provider import YaRuProvider


class YaRuAdapter(OAuth2Adapter):
    provider_id = YaRuProvider.id
    authorize_url = 'https://oauth.yandex.ru/authorize'
    access_token_url = 'https://oauth.yandex.ru/token'
    profile_url = 'https://login.yandex.ru/info'

    def complete_login(self, request, app, access_token, **kwargs):
        extra_data = requests.get(self.profile_url, headers={
            'Authorization': 'Bearer {}'.format(access_token.token)
        })
        return self.get_provider().sociallogin_from_response(
            request,
            extra_data.json()
        )

YaRuProvider.oauth2_adapter_class = YaRuAdapter
