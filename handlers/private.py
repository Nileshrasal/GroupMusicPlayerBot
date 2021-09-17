from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_photo("https://telegra.ph/file/ed4f68f51b48861989d6e.jpg")
    await message.reply_text(
        f"""**Hey, I'm 『『PRINCE PATIL 𝙼𝚄𝚂𝙸𝙲』 Bᴏᴛ |🎵

I can play ꬺᶙȿᶖɕ  in your group's voice CHAT Developed by [『PRINCE PATIL✰』](https://t.me/Princepatil96k)

Add me to your group and play music freely😆!**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝐎𝐖𝐍𝐄𝐑", url="https://t.me/Princepatil96k")
                  ],[
                    InlineKeyboardButton(
                        "𝐒𝐔𝐏𝐏𝐎𝐑𝐓", url="https://t.me/STUDY_FLOWER"
                    ),
                ],[ 
                    InlineKeyboardButton(
                        "GROUP ME LEJAO 😆", url="https://t.me/PRINCE_PATIL_OP_BOT?startgroup=true"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""**BOT IS WORKING**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝐒𝐔𝐏𝐏𝐎𝐑𝐓", url="https://t.me/STUDY_FLOWER")
                ]
            ]
        )
   )


