import requests
from oic import rndstr
from oic.oic import Client
from oic.oic.message import AuthorizationResponse
from oic.utils.http_util import Redirect
from oic.utils.authn.client import CLIENT_AUTHN_METHOD


class AuthenticationHandler:
    def __init__(self):
        response = requests.get(
            "https://localhost:44384/_configuration/Coordinator", verify=False)
        self.config = response.json()
        print("Config:", self.config)
        self.client = Client(
            client_authn_method=CLIENT_AUTHN_METHOD, verify_ssl=False)
        self.state = rndstr()
        self.nonce = rndstr()
        self.provider_info = self.client.provider_config(
            "https://localhost:44384")

    def authenticate(self):
        args = {
            "client_id": self.config["client_id"],
            "response_type": self.config["response_type"],
            "scope": [self.config["scope"]],
            "nonce": self.nonce,
            "redirect_uri": self.config["redirect_uri"],
            "state": self.state
        }
        auth_req = self.client.construct_AuthorizationRequest(
            request_args=args)
        print("Auth request:", auth_req)
        login_url = auth_req.request(self.client.authorization_endpoint)
        print("Login url:", login_url)

        self.redirect = Redirect(login_url)
        aresp = self.client.parse_response(
            AuthorizationResponse, sformat="urlencoded")
        print(aresp["code"])
        print(aresp["state"])
        print(self.state)


if __name__ == "__main__":
    auth = AuthenticationHandler()
    auth.authenticate()
