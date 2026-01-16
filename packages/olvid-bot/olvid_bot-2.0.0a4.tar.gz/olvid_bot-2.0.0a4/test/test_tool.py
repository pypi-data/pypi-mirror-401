import logging

from olvid import errors
from ClientHolder import ClientHolder

async def test_tool(client_holder: ClientHolder, fast_mode=False):
	logging.info(f"tools: ping")
	for c in client_holder.clients:
		await c.ping()

	# test with admin client
	try:
		await client_holder.admin_client.authentication_test()
	except errors.PermissionDeniedError as e:
		pass
	else:
		assert False, "authentication passed for non admin key"

	await client_holder.admin_client.authentication_admin_test()

	for c in client_holder.clients:
		# test with non admin client
		try:
			await c.authentication_admin_test()
		except errors.PermissionDeniedError as e:
			pass
		else:
			assert False, "authentication passed for non admin key"
		await c.authentication_test()
