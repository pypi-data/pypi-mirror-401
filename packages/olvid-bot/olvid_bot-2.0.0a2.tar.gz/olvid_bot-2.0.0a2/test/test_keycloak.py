import logging

from ClientHolder import ClientHolder, OlvidAdminClient, datatypes

async def test_keycloak(client_holder: ClientHolder):
	# check if there keycloak identities
	keycloak_identities: list[datatypes.Identity] = [i async for i in client_holder.admin_client.admin_identity_list(filter=datatypes.IdentityFilter(keycloak=datatypes.IdentityFilter.Keycloak.KEYCLOAK_IS))]
	if len(keycloak_identities) == 0:
		logging.warning("No keycloak identities, skipping test")
		return

	for keycloak_identity in keycloak_identities:
		keycloak_client = OlvidAdminClient(identity_id=keycloak_identity.id)

		keycloak_user: list[datatypes.KeycloakUser] = []
		async for response in keycloak_client.keycloak_user_list():
			keycloak_user.extend(response[0])
		await keycloak_client.keycloak_get_api_credentials()
