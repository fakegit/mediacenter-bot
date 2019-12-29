from mediacenter.database.torrents import CompletedTorrents
from mediacenter.mediacenterbot import MediaCenterBot
from mediacenter.scheduler_system.create_jobs import add_job
from mediacenter import ADMIN


async def notify_torrent_complete(client: MediaCenterBot):
    for torrent in CompletedTorrents().to_be_notified():
        category = torrent['category'] + ' ' if torrent['category'] else ''

        message = (
            f"**{category}Download Complete**\n"
            f"Torrent: `{torrent['name']}`\n"
            f"Size: `{torrent['size']}`\n"
            f"Category: `{category}`\n"
            f"Date Run: `{torrent['date_run']}`\n"
        )

        try:
            await client.send_message(ADMIN, message)
        except Exception:
            print("The item will be retried on the next round of notifications.")
        else:
            CompletedTorrents().mark_as_notified(torrent)
            print("Torrent notifications sent.")

add_job(
    notify_torrent_complete,
)
