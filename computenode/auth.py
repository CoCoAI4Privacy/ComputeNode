from oidcrp import RPHandler

rph = RPHandler(
    "https://localhost:44384/.well-known/openid-configuration", verify_ssl=False)
issuer_id = "https://localhost:44384/"
info = rph.begin(issuer_id)
print(info["url"])
