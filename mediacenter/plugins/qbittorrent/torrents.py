from time import sleep

import pyrogram.errors as pyro_errors
from pyrogram import emoji
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from mediacenter.api_interfaces.qBittorrent.Qbittorrent import TorrentClient as QBT
from mediacenter import MediaCenterBot
from mediacenter.plugins.admin.help import add_command_help
from mediacenter.utils.converters import human_bytes, human_unix_time, time_delta
from mediacenter.utils import custom_filters


def make_torrent_buttons(torrent_hash):
    buttons = [
        [
            InlineKeyboardButton("Resume", f"resume_tor+{torrent_hash}"),
            InlineKeyboardButton("Pause", f"pause_tor+{torrent_hash}"),
            InlineKeyboardButton("Delete", f"delete_tor+{torrent_hash}"),
        ],
        [
            InlineKeyboardButton("Priority", f"priority+{torrent_hash}"),
        ],
        [
            InlineKeyboardButton("Update", f"update+{torrent_hash}"),
            InlineKeyboardButton("Back", f"back"),
        ]
    ]

    return buttons


@MediaCenterBot.on_message(custom_filters.current_module('qbt') & custom_filters.command("list"))
async def send_torrent_list(_, message: Message):
    torrents = QBT().torrents()
    if not len(torrents) == 0:
        text = ""
        count = 1
        for x in QBT().torrents():
            text += f"{count}. {x['name']}\n\n"
            count += 1

        await message.reply(text)
    else:
        await message.reply(f"**You have no torrents!** {emoji.EXCLAMATION_MARK}")


@MediaCenterBot.on_message(custom_filters.current_module('qbt') & custom_filters.command("torrents"))
async def all_torrents(_, message: Message, **kwargs):
    buttons = []

    torrents = QBT().torrents()
    if len(torrents) == 0:
        await message.reply(f"**You have no torrents!** {emoji.EXCLAMATION_MARK}")
        return

    for x in torrents:
        button = [
            InlineKeyboardButton(
                text=x['name'],
                callback_data=f"torrent+{x['hash']}"
            )
        ]
        buttons.append(button)

    if kwargs.get('back'):
        await message.edit_text("Here is all the torrents available", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply("Here is all the torrents available", reply_markup=InlineKeyboardMarkup(buttons))


@MediaCenterBot.on_callback_query(custom_filters.current_module('qbt') & custom_filters.callback_query('torrent'))
async def torrent(_, callback: CallbackQuery, **kwargs):
    if kwargs.get('torrent_hash'):
        torrent_hash = kwargs.get('torrent_hash')
    else:
        torrent_hash = callback.payload

    if kwargs.get('update') and (False if kwargs.get('answer') else True):
        await callback.answer("Updating...")

    if kwargs.get('update'):
        sleep(3)

    torrent_details = QBT().single_torrent(torrent_hash)
    completed_on = human_unix_time(torrent_details['completion_date'])
    completed_on = "Incomplete" if torrent_details['completion_date'] == -1 else completed_on
    priority_level = torrent_details['priority'] if torrent_details['priority'] != -1 else ''
    progress = round(float(torrent_details['progress'] * 100), 2) if torrent_details['progress'] else 0
    total_size = human_bytes(torrent_details['total_size']) if torrent_details['total_size'] != -1 or 0 else 0

    constructed_message = (
        f"**Torrent**:\n"
        f"{str(priority_level) + '. ' if priority_level else ''}__{QBT().find_torrent_name(torrent_hash)}__\n\n"

        f"**Status**:\n"
        f"__{torrent_details['state'].title()}__\n\n"

        f"**Size**:\n"
        f"__{total_size}__ ({progress}%)\n\n"

        f"**Category**:\n"
        f"__{torrent_details['category'] if torrent_details['category'] else 'None'}__\n\n"

        f"**Time Elapsed**:\n"
        f"__{time_delta(torrent_details['time_elapsed'])}__\n\n"

        f"**Completed on**:\n"
        f"__{completed_on}__\n\n"
    )

    buttons = make_torrent_buttons(torrent_hash)

    try:
        await callback.edit_message_text(
            constructed_message,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except pyro_errors.MessageNotModified:
        await callback.answer("No change")
        message = await callback.message.reply("Torrent details have not changed")
        await message.delete()


@MediaCenterBot.on_message(custom_filters.current_module('qbt') & custom_filters.command("add"))
async def add_torrent(_, message: Message):
    try:
        torrent_link = message.command[1]
        added_torrent = QBT().add_torrent(torrent_link)

        if added_torrent == "Ok.":
            await message.reply(f"**Torrent Added Successfully! {emoji.PARTY_POPPER}**")
        else:
            await message.reply(
                f"Either that was an incorrect torrent link or you just sent some gibberish "
                f"{emoji.FACE_VOMITING} "
                f"Nothing I can do to fix that {emoji.MAN_SHRUGGING_MEDIUM_LIGHT_SKIN_TONE}"
            )

    except IndexError:
        await message.reply("Please send a the link to the torrent after the command")


# # Command help section
add_command_help(
    'qbittorrent', [
        ['/list', 'Lists all the torrents in the client.'],
        ['/torrents', 'Sends torrent buttons to interact with each torrent.'],
        ['/add', 'Add a new torrent. Send link to torrent as argument..'],
    ],
)
