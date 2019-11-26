from mediacenter.mediacenterbot import MediaCenterBot
from pyrogram import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from mediacenter.utils.custom_filters import CustomFilters
from mediacenter.utils.Qbittorrent import TorrentClient as QBT


@MediaCenterBot.on_message(CustomFilters.command("controls"))
async def controls(bot: MediaCenterBot, message: Message):
    await message.reply(
        "Here are some master controls..",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"Resume All", f"resume_all"),
                InlineKeyboardButton(f"Pause All", f"pause_all"),
            ],
        ])
    )


@MediaCenterBot.on_callback_query(CustomFilters.callback_query('pause_all', payload=False))
async def pause_all(client, callback: CallbackQuery):
    try:
        print("hits")
        QBT().pause_all()
        await callback.answer("Pausing all torrents.")
    except:
        await callback.answer("An error occurred..")
        await callback.edit_message_text("An error occurred. Please retry later..")


@MediaCenterBot.on_callback_query(CustomFilters.callback_query('resume_all', payload=False))
async def resume_all(client, callback: CallbackQuery):
    try:
        QBT().resume_all()
        await callback.answer("Resuming all torrents.")
    except:
        await callback.answer("An error occurred..")
        await callback.edit_message_text("An error occurred. Please retry later..")