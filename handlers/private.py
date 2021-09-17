from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_photo("https://telegra.ph/file/9c71bd26b7772df92684a.jpg")
    await message.reply_text(

        
        
        
     
        


















        f"""**Hey, I'm 『『PRINCE PATIL 𝙼𝚄𝚂𝙸𝙲』 Bᴏᴛ |🎵

I can play ꬺᶙȿᶖɕ  in your group's voice CHAT Developed by [『PRINCE PATIL✰』](https://t.me/Princepatil96k)

Add me to your group and play music freely😆 @STUDY_FLOWER_QUIZ_GROUP!**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "PRINCE PATIL CREATER", url="https://t.me/Princepatil96k")
                  ],[
                    InlineKeyboardButton(
                        "PRINCE MUSIC SUPPORT", url="https://t.me/PrinceMusicWorld1"
                    ),
                ],[ 
                    InlineKeyboardButton(
                        "PRINCE MUSIC KO LE JAO😉", url="https://t.me/PRINCE_PATIL_OP_BOT?startgroup=true"
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


