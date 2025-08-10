import requests
from django.http import HttpResponseForbidden
from functools import lru_cache


class AuthZMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.service_url = "http://auth-service:8000"  # From env in production

    @lru_cache(maxsize=1024)  # Simple permission caching
    def _check_permission(self, user_id: str, action: str, resource: str) -> bool:
        """Inline permission check with cache"""
        try:
            response = requests.post(
                f"{self.service_url}/check",
                json={
                    "user": f"user:{user_id}",
                    "action": action,
                    "resource": resource
                },
                timeout=1.0  # Fail fast
            )
            return response.json().get("allowed", False)
        except requests.RequestException:
            return False  # Fail closed

    def __call__(self, request):
        request.check_permission = lambda a, r: self._check_permission(
            user_id=str(request.user.id),  # Works with AnonymousUser
            action=a,
            resource=r
        )
        return self.get_response(request)
