from django.conf import settings
from openfga_sdk.client import ClientConfiguration, ClientCheckRequest
from openfga_sdk.sync import OpenFgaClient


class AuthorizationClient:
    def __init__(self):
        store_id = settings.OPENFGA_STORE_ID
        model_id = settings.OPENFGA_MODEL_ID

        if not store_id:
            self.client = None
            return

        configuration = ClientConfiguration(
            api_url="http://openfga:8080",
            store_id=store_id,
            authorization_model_id=model_id,
        )

        self.client = OpenFgaClient(configuration)

    def check(self, uid, relation, domain):
        if not self.client:
            return True

        body = ClientCheckRequest(
            user=f"user:{uid}",
            relation=relation,
            object=f"domain:{domain}",
        )

        response = self.client.check(body)

        return response.allowed  # type: ignore
