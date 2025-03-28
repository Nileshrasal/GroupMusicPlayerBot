import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 30)
    draw.text((190, 560), f"Title: {title}", (51, 215, 255), font=font)
    draw.text(
        (190, 600), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 640), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 680),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(command("play") 
                   & filters.group
                   & ~filters.edited 
                   & ~filters.forwarded
                   & ~filters.via_bot)
async def play(_, message: Message):

    lel = await message.reply("🔄 **RUKH BHAI PRINCE SONG LAGA RAHA HAI**")
    
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "IronHeart"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>PRINCE PATIL MUSIC Add me as admin of yor group first!</b>")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**i joined this group for prince patil music play music 🎵**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>🛑 Flood Wait Error 🛑</b> \n\Hey {user.first_name}, assistant userbot couldn't join your group due to heavy join requests. Make sure userbot is not banned in group and try again later!")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>Hey {user.first_name}, assistant userbot is not in this chat, ask admin to send /play command for first time to add it.</i>")
        return
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"🙄🙄𝐕𝐢𝐝𝐞𝐨𝐬 𝐥𝐨𝐧𝐠𝐞𝐫 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 𝐚𝐫𝐞𝐧'𝐭 𝐚𝐥𝐥𝐨𝐰𝐞𝐝 𝐭𝐨 𝐩𝐥𝐚𝐲..!"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/9623c1b38ce338968f8ac.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="『PRINCE PATIL✰』⚜",
                        url="https://t.me/Princepatil96k")
                   
                ]
            ]
        )
        
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="PRINCE MUSIC DUNIYA 🎥",
                            url=f"{url}"),
                        InlineKeyboardButton(
                            text="PRINCE MUSIC SUPPORT",
                            url=f"https://t.me/PrinceMusicWorld1")

                    ]
                ]
            )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/9c71bd26b7772df92684a.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🔰⚡PRINCE PATIL⚡🔰",
                                url=f"https://t.me/Princepatil96k")

                        ]
                    ]
                )
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❌ 𝐕𝐢𝐝𝐞𝐨𝐬 𝐥𝐨𝐧𝐠𝐞𝐫 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 𝐚𝐫𝐞𝐧'𝐭 𝐚𝐥𝐥𝐨𝐰𝐞𝐝 𝐭𝐨 𝐩𝐥𝐚𝐲..!")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("🧐 **What's the song you want to play?**")
        await lel.edit("🔎 **𝐅𝐢𝐧𝐝𝐢𝐧𝐠 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("♫ **CONNECTING TO THE SERVER..!**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
        except Exception as e:
            await lel.edit(
                "❌ 𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.\n\n𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="PRINCE MUSIC DUNIYA 🎥",
                            url=f"{url}"),
                        InlineKeyboardButton(
                            text="🔰⚡PRINCE PATIL⚡🔰",
                            url=f"https://t.me/Princepatil96k")

                    ]
                ]
            )
        
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❌ 𝐕𝐢𝐝𝐞𝐨𝐬 𝐥𝐨𝐧𝐠𝐞𝐫 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 𝐚𝐫𝐞𝐧'𝐭 𝐚𝐥𝐥𝐨𝐰𝐞𝐝 𝐭𝐨 𝐩𝐥𝐚𝐲..!")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption="**𝗦𝗢𝗡𝗚:** {}\n**𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** {} min\n**𝗔𝗗𝗗𝗘𝗗 𝗕𝗬:** {}\n\n**#⃣ ǫᴜᴇᴜᴇᴅ ᴘᴏsɪᴛɪᴏɴ:** {}".format(
        title, duration, message.from_user.mention(), position
        ),
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="**𝗦𝗢𝗡𝗚:** {}\n**𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** {} ᴍɪɴ\n**𝗔𝗗𝗗𝗘𝗗 𝗕𝗬:** {}\n\n**▶️ ɴᴏᴡ ᴘʟᴀʏɪɴɢ ᴀᴛ `{}`...**".format(
        title, duration, message.from_user.mention(), message.chat.title
        ), )
        os.remove("final.png")
        return await lel.delete()
