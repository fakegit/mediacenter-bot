from mediacenter import ALLOWED_USERS
from mediacenter.mediacenterbot import MediaCenterBot
from pyrogram import Filters, Message, Emoji, CallbackQuery

# CONSTANTS
NOT_ALLOWED_MESSAGE = (f'**{Emoji.FIRE} You are not allowed! {Emoji.FIRE}\n'
                       f'{Emoji.FIRE} This incident will be reported! {Emoji.FIRE}**')


@MediaCenterBot.on_message(~Filters.user(ALLOWED_USERS), group=-1)
async def stop_user_from_doing_anything(bot: MediaCenterBot, message: Message):
    """
    Checks if user is allowed to use TorrentBot
    """
    if message.chat and message.chat.type in {"group", "supergroup"}:
        await message.reply(NOT_ALLOWED_MESSAGE)
        message.stop_propagation()
    else:
        await message.reply(NOT_ALLOWED_MESSAGE)
        message.stop_propagation()


@MediaCenterBot.on_callback_query(~Filters.user(ALLOWED_USERS), group=-1)
async def stop_user_from_doing_anything_callback(client, callback: CallbackQuery):
    """
    Checks if user is allowed to use TorrentBot via CallbackQuery
    """
    if callback.message.chat and callback.message.chat.type in {'group', 'supergroup'}:
        await callback.answer('Groups not allowed.')
        await callback.edit_message_text(NOT_ALLOWED_MESSAGE)
        callback.stop_propagation()

    await callback.edit_message_text(NOT_ALLOWED_MESSAGE)
    callback.stop_propagation()