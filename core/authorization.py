from django.conf import settings


class AuthorizationClient:
    def __init__(self):
        self.store_id = settings.OPENFGA_STORE_ID
        self.model_id = settings.OPENFGA_MODEL_ID

    def check(self, uid, relation, domain):
        if not self.store_id:
            return True
        return False
