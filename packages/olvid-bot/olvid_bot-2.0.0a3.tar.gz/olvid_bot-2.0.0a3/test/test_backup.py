import asyncio
import logging
import uuid

from olvid import datatypes, OlvidAdminClient
from ClientHolder import ClientHolder
from utils.tools_group import create_standard_group


async def test_backup(client_holder: ClientHolder, fast_mode: bool):
	test_random_nonce: str = str(uuid.uuid4())
	try:
		if fast_mode:
			logging.warn(f"Skip backup tests in fast mode")
			return

		####
		# feed with data before backup
		####
		# create a group with everyone
		logging.info(f"Creating group")
		await create_standard_group(client_holder, client_holder.clients[0], test_random_nonce, "")

		# create admin client key to backup, with storage
		admin_client_key: datatypes.ClientKey = await client_holder.admin_client.admin_client_key_new(test_random_nonce, 0)
		admin_storage_element: datatypes.StorageElement = datatypes.StorageElement(key=test_random_nonce, value="admin-storage-to-backup")
		await OlvidAdminClient(identity_id=0, client_key=admin_client_key.key).storage_set(admin_storage_element.key, admin_storage_element.value)

		# feed client storage
		for c in client_holder.clients:
			await c.storage_set(test_random_nonce, f"to-backup-{c.identity.id}")
			async for d in c.discussion_list():
				await c.discussion_storage_set(discussion_id=d.id, key=test_random_nonce, value=f"to-backup-{c.identity.id}")

		####
		# create backup
		####
		await client_holder.admin_client.admin_backup_now()

		####
		# then get backup and check it contains enough data
		####
		backup_key: str = await client_holder.admin_client.admin_backup_key_get()
		backup = await client_holder.admin_client.admin_backup_get(backup_key=backup_key)

		# check admin backup
		if backup.admin_backup.admin_client_key_count == 0 or backup.admin_backup.admin_client_key_count == 0:
			logging.warn(f"Skip backup tests: nothing in admin backup")
			return

		# check profile backups
		profile_to_backup: list[datatypes.Backup.ProfileBackup] = []
		for c in client_holder.clients:
			valid_profiles = [profile for profile in backup.profile_backups if profile.profile_display_name == c.identity.display_name]
			if len(valid_profiles) != 1:
				raise Exception(f"cannot find profile for {c.identity.display_name} in backup")
			profile_to_backup.append(valid_profiles[0])
			snapshot: datatypes.Backup.ProfileBackup.Snapshot = sorted(profile_to_backup[0].snapshots, key=lambda s: s.timestamp)[-1]
			if snapshot.client_key_count == 0:
				logging.error(f"{c.identity.display_name}: snapshot does not contain client key")
				return
			if snapshot.contact_count == 0:
				logging.error(f"{c.identity.display_name}: snapshot does not contain contacts")
				return
			if snapshot.storage_elements_count == 0:
				logging.error(f"{c.identity.display_name}: snapshot does not storage elements")
				return
			if snapshot.group_count == 0:
				logging.warn(f"{c.identity.display_name}: snapshot doest not contain groups ({snapshot})")

		####
		# delete data
		####
		# delete test identities
		for c in client_holder.clients:
			await client_holder.admin_client.admin_identity_delete(c.identity.id)
			logging.info(f"Deleted identity: {c.identity.id}")

		# delete admin client key
		await client_holder.admin_client.admin_client_key_delete(client_key=admin_client_key.key)

		# wait for cascade deletion to complete
		logging.info(f"Wait for deletion to be effective")
		await asyncio.sleep(5)

		####
		# restore admin client key and storage
		####
		await client_holder.admin_client.admin_backup_restore_admin_backup(backup_key=backup_key)

		# check admin client key is back
		new_admin_client_key = await client_holder.admin_client.admin_client_key_get(client_key=admin_client_key.key)
		assert admin_client_key == new_admin_client_key, f"{admin_client_key} != {new_admin_client_key}"

		# check admin storage
		new_admin_storage_element_value: str = await OlvidAdminClient(identity_id=0, client_key=admin_client_key.key).storage_get(test_random_nonce)
		assert admin_storage_element.value == new_admin_storage_element_value, f"{admin_storage_element.value} != {new_admin_storage_element_value}"

		####
		# restore profile
		####
		for c in client_holder.clients:
			profile = [profile for profile in backup.profile_backups if profile.profile_display_name == c.identity.display_name][0]
			snapshot: datatypes.Backup.ProfileBackup.Snapshot = sorted(profile.snapshots, key=lambda s: s.timestamp)[-1]

			logging.debug(f"{c.identity.display_name}: snapshot to restore\n{snapshot}")

			response = await client_holder.admin_client.admin_backup_restore_profile_snapshot(backup_key=backup_key, id=snapshot.id, new_device_name=test_random_nonce)

			assert response.restored_identity.display_name.__eq__(profile.profile_display_name)
			assert c.client_key in [ck.key for ck in response.restored_client_keys], f"{c.client_key} not in {response.restored_client_keys}"
			# check contact
			assert len([c async for c in c.contact_list()]) == snapshot.contact_count, "Invalid contact count"
			# check groups
			assert len([c async for c in c.group_list()]) == snapshot.group_count, "Invalid group count"
			assert len([g async for g in c.group_list(filter=datatypes.GroupFilter(name_search=test_random_nonce))]) == 1, "Do not found group"
			# check storage
			assert (await c.storage_get(test_random_nonce)).startswith("to-backup"), "cannot find global storage"
			# check discussion storage
			async for d in c.discussion_list():
				assert (await c.discussion_storage_get(discussion_id=d.id, key=test_random_nonce)).startswith("to-backup"), "cannot find discussion storage"

	# try to clean created elements
	finally:
		# remove admin client key
		try:
			await client_holder.admin_client.admin_client_key_delete(test_random_nonce)
		except:
			pass

		# clean client storage
		for c in client_holder.clients:
			try:
				await c.storage_unset(test_random_nonce)
			except:
				pass
			try:
				async for d in c.discussion_list():
					await c.discussion_storage_unset(discussion_id=d.id, key=test_random_nonce)
			except:
				pass
