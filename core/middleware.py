from core.authorization import AuthorizationClient


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._client = AuthorizationClient()

    def __call__(self, request):
        request.check_perm = self._client.check
        return self.get_response(request)
