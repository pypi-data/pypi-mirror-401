import asyncio
import datetime
import logging
import uuid
from asyncio import InvalidStateError

from ClientHolder import ClientHolder, ClientWrapper
from olvid import datatypes, OlvidClient, listeners
from utils.tools_message import send_message_wait_and_check_content
from utils.tools_group import create_standard_group


async def test_message_retention_duration(client_1: ClientWrapper, client_2: ClientWrapper):
	original_settings: datatypes.IdentitySettings = await client_1.settings_identity_get()
	try:
		# populate discussions with "old messages" (messages to delete)
		tasks = []
		random_body: str = str(uuid.uuid4())[:4]
		for i in range(1, 10):
			tasks.append(send_message_wait_and_check_content(client_1, client_2, f"settings - {i} - {random_body}"))
		for task in tasks:
			await task

		# determine limit timestamp
		limit_timestamp: int = [m async for m in client_1.message_list()][-1].timestamp

		# wait before next population
		logging.info(f"sleep before sending messages")
		await asyncio.sleep(5)

		# populate discussions with "new messages" (messages to keep)
		tasks = []
		random_body: str = str(uuid.uuid4())[:4]
		for i in range(1, 10):
			tasks.append(send_message_wait_and_check_content(client_1, client_2, f"settings - {i} - {random_body}"))
		for task in tasks:
			await task

		# determine messages to delete and messages to keep
		all_messages: list[datatypes.Message] = [m async for m in client_1.message_list()]
		messages_to_delete: list[datatypes.Message] = [m for m in all_messages if m.timestamp <= limit_timestamp]
		messages_to_keep: list[datatypes.Message] = [m for m in all_messages if m.timestamp > limit_timestamp]

		# create listener for message deleting
		# create one bot for each message
		bots: list[OlvidClient] = [client_1.create_notification_bot(listener=listeners.MessageDeletedListener(handler=lambda m: m, count=1, message_ids=[m.id])) for m in messages_to_delete]
		# create a bot for all messages to let watchdog know we listen
		bots.append(client_1.create_notification_bot(listener=listeners.MessageDeletedListener(handler=lambda m: m, count=len(messages_to_delete))))

		# change settings
		new_settings: datatypes.IdentitySettings = original_settings._clone()
		new_settings.message_retention.existence_duration = round(datetime.datetime.now().timestamp() - (limit_timestamp/1000)) - 1
		await client_1.settings_identity_set(identity_settings=new_settings)

		# wait for message deletion
		for bot in bots:
			await bot.wait_for_listeners_end()

		# check we deleted messages correctly
		kept_messages: list[datatypes.Message] = [m async for m in client_1.message_list()]
		if len(kept_messages) != len(messages_to_keep):
			raise ValueError("Deleted too many messages")
		for i in range(len(kept_messages)):
			if not kept_messages[i].id.__eq__(messages_to_keep[i].id):
				raise ValueError("Wrong messages kept")
	finally:
		# restore settings
		await client_1.settings_identity_set(identity_settings=original_settings)


async def test_message_retention_discussion_count(client_1: ClientWrapper, client_2: ClientWrapper):
	original_settings: datatypes.IdentitySettings = await client_1.settings_identity_get()
	try:
		# populate discussions
		tasks = []
		random_body: str = str(uuid.uuid4())[:4]
		for i in range(1, 10):
			tasks.append(send_message_wait_and_check_content(client_1, client_2, f"settings - {i} - {random_body}"))
		for task in tasks:
			await task

		# get current messages
		all_messages: list[datatypes.Message] = [m async for m in client_1.message_list()]
		messages_by_discussion: dict[int, list[datatypes.Message]] = {}
		for m in all_messages:
			if not messages_by_discussion.get(m.discussion_id):
				messages_by_discussion[m.discussion_id] = []
			messages_by_discussion[m.discussion_id].append(m)

		# determine messages to delete and messages to keep
		messages_to_delete: list[datatypes.Message] = []
		messages_to_keep: list[datatypes.Message] = []
		for did in messages_by_discussion.keys():
			if len(messages_by_discussion[did]) > 8:
				messages_to_delete.extend(messages_by_discussion[did][:-8])
				messages_to_keep.extend(messages_by_discussion[did][-8:])
			else:
				messages_to_keep.extend(messages_by_discussion[did])

		# create listener for message deleting
		# create one bot for each message
		bots: list[OlvidClient] = [client_1.create_notification_bot(listener=listeners.MessageDeletedListener(handler=lambda m: m, count=1, message_ids=[m.id])) for m in messages_to_delete]
		# create a bot for all messages to let watchdog know we listen
		bots.append(client_1.create_notification_bot(listener=listeners.MessageDeletedListener(handler=lambda m: m, count=len(messages_to_delete))))

		# change settings
		new_settings: datatypes.IdentitySettings = original_settings._clone()
		new_settings.message_retention.discussion_count = 8
		await client_1.settings_identity_set(identity_settings=new_settings)

		# wait for message deletion
		for bot in bots:
			await bot.wait_for_listeners_end()

		# check we do not deleted messages in other discussions
		all_messages_refreshed: list[datatypes.Message] = [m async for m in client_1.message_list()]
		if len(all_messages) != len(all_messages_refreshed) + len(messages_to_delete):
			raise ValueError("Deleted messages in other discussions")
	finally:
		# restore settings
		await client_1.settings_identity_set(identity_settings=original_settings)


async def test_message_retention_global_count(client_1: ClientWrapper, client_2: ClientWrapper):
	original_settings: datatypes.IdentitySettings = await client_1.settings_identity_get()
	try:
		# populate discussions
		tasks = []
		random_body: str = str(uuid.uuid4())[:4]
		for i in range(1, 10):
			tasks.append(send_message_wait_and_check_content(client_1, client_2, f"settings - {i} - {random_body}"))
		for task in tasks:
			await task

		# get current messages
		all_messages: list[datatypes.Message] = [m async for m in client_1.message_list()]
		if len(all_messages) < 10:
			raise InvalidStateError("Do not found enough messages")

		# determine messages to delete and messages to keep
		messages_to_delete: list[datatypes.Message] = all_messages[:-9]
		messages_to_keep: list[datatypes.Message] = all_messages[-9:]

		# create listener for message deleting
		# create one bot for each message
		bots: list[OlvidClient] = [client_1.create_notification_bot(listener=listeners.MessageDeletedListener(handler=lambda m: m, count=1, message_ids=[m.id])) for m in messages_to_delete]
		# create a bot for all messages to let watchdog know we listen
		bots.append(client_1.create_notification_bot(listener=listeners.MessageDeletedListener(handler=lambda m: m, count=len(messages_to_delete))))

		# change settings
		new_settings: datatypes.IdentitySettings = original_settings._clone()
		new_settings.message_retention.global_count = 9
		await client_1.settings_identity_set(identity_settings=new_settings)

		# wait for message deletion
		for bot in bots:
			await bot.wait_for_listeners_end()

		# check we do not deleted more messages than expected in discussion
		kept_messages: list[datatypes.Message] = [m async for m in client_1.message_list()]
		if len(kept_messages) != len(messages_to_keep):
			raise ValueError("Deleted too many messages")
		for i in range(len(kept_messages)):
			if not kept_messages[i].id.__eq__(messages_to_keep[i].id):
				raise ValueError("Wrong messages kept")
	finally:
		# restore settings
		await client_1.settings_identity_set(identity_settings=original_settings)


async def test_message_retention_locked(client_holder: ClientHolder, client_1: ClientWrapper):
	original_identity_settings: datatypes.IdentitySettings = await client_1.settings_identity_get()
	try:
		# create a group and post messages
		group_1: datatypes.Group = await create_standard_group(client_holder=client_holder, admin_client=client_1, group_name="Locked Group", group_description="")
		group_discussion_1: datatypes.Discussion = await client_1.discussion_get_by_group(group_id=group_1.id)
		bots: list[OlvidClient] = [
			client_1.create_notification_bot(listener=listeners.MessageSentListener(handler=lambda i: i, count=5)),
			client_1.create_notification_bot(listener=listeners.MessageUploadedListener(handler=lambda i: i, count=5)),
			client_1.create_notification_bot(listener=listeners.MessageDeliveredListener(handler=lambda i: i, count=5)),
			client_1.create_notification_bot(listener=listeners.MessageReadListener(handler=lambda i: i, count=5)),
		]
		for c in client_holder.clients[1:]:
			bots.append(c.create_notification_bot(listener=listeners.MessageReceivedListener(handler=lambda i: i, count=5)))
		for i in range(5):
			await group_discussion_1.post_message(client_1, f"locked message - {i}")
		for bot in bots:
			await bot.wait_for_listeners_end()

		# get messages
		locked_discussion_ids: list[int] = [d.id async for d in client_1.discussion_locked_list()]
		all_messages: list[datatypes.Message] = [m async for m in client_1.message_list()]
		messages_to_keep: list[datatypes.Message] = [m for m in all_messages if m.discussion_id not in locked_discussion_ids]

		# prepare listeners for group disband
		bots: list[OlvidClient] = [
			client_1.create_notification_bot(listener=listeners.GroupDeletedListener(handler=lambda i: i, count=1)),
			client_1.create_notification_bot(listener=listeners.DiscussionLockedListener(handler=lambda i: i, count=1)),
		]
		for c in client_holder.clients[1:]:
			bots.append(c.create_notification_bot(listener=listeners.GroupDeletedListener(handler=lambda i: i, count=1)))
			bots.append(c.create_notification_bot(listener=listeners.DiscussionLockedListener(handler=lambda i: i, count=1)))

		# disband group
		await group_1.disband(client_1)
		for bot in bots:
			await bot.wait_for_listeners_end()

		# change settings
		new_settings: datatypes.IdentitySettings = original_identity_settings._clone()
		new_settings.message_retention.clean_locked_discussions = True
		await client_1.settings_identity_set(identity_settings=new_settings)

		# check we do not deleted more messages than expected in discussion
		kept_messages: list[datatypes.Message] = [m async for m in client_1.message_list()]
		if len(kept_messages) != len(messages_to_keep):
			raise ValueError("Deleted too many messages")
		for i in range(len(kept_messages)):
			if not kept_messages[i].id.__eq__(messages_to_keep[i].id):
				raise ValueError("Wrong messages kept")
	finally:
		await client_1.settings_identity_set(identity_settings=original_identity_settings)


async def test_invitation_auto_accept_one_to_one(client_1: ClientWrapper, client_2: ClientWrapper):
	original_identity_settings: datatypes.IdentitySettings = await client_2.settings_identity_get()
	try:
		######
		# Auto accept pending invitations (when you change settings browse pending invitations and accept them if necessary)
		######
		contact_1_2 = await client_1.get_contact_associated_to_another_client(client_2)

		# downgrade one to one contact and re-invite him
		if contact_1_2.has_one_to_one_discussion:
			bots: list[OlvidClient] = [
				client_1.create_notification_bot(listener=listeners.DiscussionLockedListener(handler=lambda i: i, count=1)),
				client_2.create_notification_bot(listener=listeners.DiscussionLockedListener(handler=lambda i: i, count=1)),
			]
			await client_1.contact_downgrade_one_to_one_discussion(contact_id=contact_1_2.id)
			for bot in bots:
				await bot.wait_for_listeners_end()

		# add global listeners to let watchdog think we are listening
		bots: list[OlvidClient] = [
			client_1.create_notification_bot(listener=listeners.InvitationSentListener(handler=lambda i: i, count=1)),
			client_1.create_notification_bot(listener=listeners.InvitationDeletedListener(handler=lambda i: i, count=1)),
			client_1.create_notification_bot(listener=listeners.DiscussionNewListener(handler=lambda i: i, count=1)),
			client_2.create_notification_bot(listener=listeners.InvitationReceivedListener(handler=lambda i: i, count=1)),
			client_2.create_notification_bot(listener=listeners.InvitationDeletedListener(handler=lambda i: i, count=1)),
			client_2.create_notification_bot(listener=listeners.DiscussionNewListener(handler=lambda i: i, count=1)),
		]

		await client_1.contact_invite_to_one_to_one_discussion(contact_id=contact_1_2.id)
		# change settings and check pending invitation was accepted
		identity_settings: datatypes.IdentitySettings = original_identity_settings._clone()
		identity_settings.invitation.auto_accept_one_to_one = True
		await client_2.settings_identity_set(identity_settings=identity_settings)

		for bot in bots:
			await bot.wait_for_listeners_end()

		assert (await client_1.contact_get(contact_id=contact_1_2.id)).has_one_to_one_discussion, "one to one not restored (1)"

		######
		# Auto accept new invitations (when you change settings browse pending invitations and accept them if necessary)
		######
		# downgrade one to one
		bots: list[OlvidClient] = [
			client_1.create_notification_bot(listener=listeners.DiscussionLockedListener(handler=lambda i: i, count=1)),
			client_2.create_notification_bot(listener=listeners.DiscussionLockedListener(handler=lambda i: i, count=1)),
		]
		await client_1.contact_downgrade_one_to_one_discussion(contact_id=contact_1_2.id)
		for bot in bots:
			await bot.wait_for_listeners_end()

		# add global listeners to let watchdog think we are listening
		bots: list[OlvidClient] = [
			client_1.create_notification_bot(listener=listeners.InvitationSentListener(handler=lambda i: i, count=1)),
			client_1.create_notification_bot(listener=listeners.InvitationDeletedListener(handler=lambda i: i, count=1)),
			client_1.create_notification_bot(listener=listeners.DiscussionNewListener(handler=lambda i: i, count=1)),
			client_2.create_notification_bot(listener=listeners.InvitationReceivedListener(handler=lambda i: i, count=1)),
			client_2.create_notification_bot(listener=listeners.InvitationDeletedListener(handler=lambda i: i, count=1)),
			client_2.create_notification_bot(listener=listeners.DiscussionNewListener(handler=lambda i: i, count=1)),
		]

		await client_1.contact_invite_to_one_to_one_discussion(contact_id=contact_1_2.id)
		# change settings and check pending invitation was accepted
		identity_settings: datatypes.IdentitySettings = original_identity_settings._clone()
		identity_settings.invitation.auto_accept_one_to_one = True
		await client_2.settings_identity_set(identity_settings=identity_settings)

		for bot in bots:
			await bot.wait_for_listeners_end()

		assert (await client_1.contact_get(contact_id=contact_1_2.id)).has_one_to_one_discussion, "one to one not restored (2)"
	finally:
		await client_2.settings_identity_set(identity_settings=original_identity_settings)

async def test_cron_tasks(client_holder: ClientHolder, client_1: ClientWrapper):
	original_identity_settings: datatypes.IdentitySettings = await client_1.settings_identity_get()
	# a bot to ignore message deleted notifications
	messages_deleted_bot = client_1.create_notification_bot(listener=listeners.MessageDeletedListener(handler=lambda m: m))
	try:
		# prepare and set settings
		identity_settings = original_identity_settings._clone()
		identity_settings.message_retention.global_count = 9
		identity_settings.message_retention.discussion_count = 4
		await client_1.settings_identity_set(identity_settings=identity_settings)

		# wait for initial routine end daemon side
		await asyncio.sleep(1)

		# now populate with messages
		random_body: str = str(uuid.uuid4())[:4]
		for other_client in client_holder.clients[1:]:
			discussion: datatypes.Discussion = await client_1.get_discussion_associated_to_another_client(other_client)
			bots: list[OlvidClient] = [
				client_1.create_notification_bot(listener=listeners.MessageSentListener(handler=lambda i: i, count=5)),
				client_1.create_notification_bot(listener=listeners.MessageUploadedListener(handler=lambda i: i, count=5)),
				client_1.create_notification_bot(listener=listeners.MessageDeliveredListener(handler=lambda i: i, count=5)),
				client_1.create_notification_bot(listener=listeners.MessageReadListener(handler=lambda i: i, count=5)),
				other_client.create_notification_bot(listener=listeners.MessageReceivedListener(handler=lambda i: i, count=5)),
			]
			for i in range(5):
				await discussion.post_message(client_1, f"{i} - {discussion.id} - {random_body}")
			for bot in bots:
				await bot.wait_for_listeners_end()

		# determine a minimum number of messages to delete
		messages_to_delete_count: int = len([m async for m in client_1.message_list()]) - identity_settings.message_retention.global_count
		bots = [client_1.create_notification_bot(listener=listeners.MessageDeletedListener(handler=lambda m: m, count=messages_to_delete_count))]

		logging.info(f"Wait for next cron execution, expected around: {datetime.datetime.now() + datetime.timedelta(minutes=5)}")
		for bot in bots:
			await bot.wait_for_listeners_end()

		# check message cleaning respect expectations
		assert len([m async for m in client_1.message_list()]) <= identity_settings.message_retention.global_count, "global count incorrect"
		async for d in client_1.discussion_list():
			assert len([m async for m in client_1.message_list(filter=datatypes.MessageFilter(discussion_id=d.id))]) <= identity_settings.message_retention.discussion_count, f"discussion count incorrect: {d.id}"
	finally:
		await messages_deleted_bot.stop()
		await client_1.settings_identity_set(identity_settings=original_identity_settings)

async def test_settings(client_holder: ClientHolder, fast_mode: bool):
	c1, c2 = client_holder.get_one_client_pair()

	# reset settings
	for c in client_holder.clients:
		await c.settings_identity_set(identity_settings=datatypes.IdentitySettings())

	#####
	# Message retention
	#####
	if not fast_mode:
		logging.info(f"{c1.identity.id} <-> {c2.identity.id}: settings: message retention: duration")
		logging.info("(this test implies race conditions and might fail with bad network conditions)")
		await test_message_retention_duration(c1, c2)
	logging.info(f"{c1.identity.id} <-> {c2.identity.id}: settings: message retention: discussion count")
	await test_message_retention_discussion_count(c1, c2)
	logging.info(f"{c1.identity.id} <-> {c2.identity.id}: settings: message retention: global count")
	await test_message_retention_global_count(c1, c2)
	logging.info(f"{c1.identity.id} <-> {c2.identity.id}: settings: message retention: locked discussions")
	await test_message_retention_locked(client_holder, c1)
	if not fast_mode:
		logging.info(f"{c1.identity.id} <-> {c2.identity.id}: settings: message retention: cron tasks")
		await test_cron_tasks(client_holder, c1)

	#####
	# Invitation auto accept
	#####
	logging.info(f"{c1.identity.id} <-> {c2.identity.id}: settings: invitation auto accept: one to one")
	await test_invitation_auto_accept_one_to_one(c1, c2)

	#####
	# Keycloak auto invite
	#####
	# TODO
