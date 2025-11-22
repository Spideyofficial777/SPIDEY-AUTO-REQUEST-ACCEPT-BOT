import jinja2
from configs import URL, LOG_CHANNEL
from Spidey.bot import SpideyBot
from Spidey.util.human_readable import humanbytes
from Spidey.util.file_properties import get_file_ids
import urllib.parse
import logging
import aiohttp


async def render_page(id, secure_hash, src=None):
    file = await SpideyBot.get_messages(int(LOG_CHANNEL), int(id))
    file_data = await get_file_ids(SpideyBot, int(LOG_CHANNEL), int(id))
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f"link hash: {secure_hash} - {file_data.unique_id[:6]}")
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash

    src = urllib.parse.urljoin(
        URL,
        f"{id}/{urllib.parse.quote_plus(file_data.file_name)}?hash={secure_hash}",
    )

    tag = file_data.mime_type.split("/")[0].strip()
    file_size = humanbytes(file_data.file_size)
    if tag in ["video", "audio"]:
        template_file = "Spidey/template/req.html"
    else:
        template_file = "Spidey/template/dl.html"
        async with aiohttp.ClientSession() as s:
            async with s.get(src) as u:
                file_size = humanbytes(int(u.headers.get("Content-Length")))

    with open(template_file) as f:
        template = jinja2.Template(f.read())

    file_name = file_data.file_name.replace("_", " ")

    return template.render(
        file_name=file_name,
        file_url=src,
        file_size=file_size,
        file_unique_id=file_data.unique_id,
    )
