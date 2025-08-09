from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

class YaRuProvider(OAuth2Provider):
    id = 'yaru'
    name = 'Yandex'

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        print(data)
        return {
            'email': data.get('default_email'),
            'login': data.get('login'),
        }

provider_classes = [YaRuProvider]
