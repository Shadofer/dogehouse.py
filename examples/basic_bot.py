import os

from dogehouse import DogeClient
from dogehouse.events import (
    HandRaisedEvent, ReadyEvent, RoomJoinEvent,
    MessageEvent, UserJoinEvent, UserLeaveEvent,
    CommandEvent,
)

token = os.getenv("TOKEN", '')
refresh_token = os.getenv("REFRESH_TOKEN", '')

doge = DogeClient(token, refresh_token)


@doge.on_ready
async def make_my_room(event: ReadyEvent) -> None:
    print(f"Successfully connected as @{event.user.username}!")
    await doge.create_room('Hello dogehouse.py!')


@doge.on_room_join
async def joined_room(event: RoomJoinEvent) -> None:
    print("Joined room", event.room.name)


@doge.on_user_join
async def greet_user(event: UserJoinEvent) -> None:
    await doge.send_message(f"Hello @{event.user.username}")
    await doge.send_message(f"Hi, I sent you a whisper!", whisper_to=[event.user])


@doge.on_user_leave
async def user_left(event: UserLeaveEvent) -> None:
    await doge.send_message(f"Bye @{event.user.username}")


@doge.on_message
async def echo_message(event: MessageEvent) -> None:
    msg = event.message
    print(f'@{msg.author.username} sent {msg.content}')


@doge.on_hand_raise
async def accept_speaker_request(event: HandRaisedEvent) -> None:
    await doge.add_speaker(event.user_id)
    await doge.send_message(f'Gave speaker permissions to: {event.user_id}')


@doge.command
async def echo(event: CommandEvent) -> None:
    msg = event.message
    await doge.send_message(f'@{msg.author.username} said {msg.content}')

doge.run()
