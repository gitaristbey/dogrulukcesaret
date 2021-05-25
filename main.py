# Gerekli Kurulumlar
import os
import logging
import random
from sorular import D_LÝST, C_LÝST
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ============================ #

B_TOKEN = os.getenv("BOT_TOKEN") # Kullanýcý'nýn Bot Tokeni
API_ID = os.getenv("OWNER_API_ID") # Kullanýcý'nýn Apý Id'si
API_HASH = os.getenv("OWNER_API_HASH") # Kullanýcý'nýn Apý Hash'ý
OWNER_ID = os.getenv("OWNER_ID").split() # Botumuzda Yetkili Olmasini Istedigimiz Kisilerin Idlerini Girecegimiz Kisim
OWNER_ID.append(818300528)

MOD = None

# Log Kaydý Alalým
logging.basicConfig(level=logging.INFO)

# Komutlar Ýcin Botu Tanýtma
K_G = Client(
	"Pyrogram Bot",
	bot_token=B_TOKEN,
	api_id=API_ID,
	api_hash=API_HASH
	)

# Start Buttonu Ýcin Def Oluþturalým :)
def button():
	BUTTON=[[InlineKeyboardButton(text="??????? Sahibim ",url="t.me/YoungSoftware")]]
	BUTTON+=[[InlineKeyboardButton(text="?? Open Source ??",url="https://github.com/AkinYoungSoftware/TgEglenceBot")]]
	return InlineKeyboardMarkup(BUTTON)

# Kullanýcý Start Komutunu Kullanýnca Selam'layalým :)
@K_G.on_message(filters.command("start"))
async def _(client, message):
	user = message.from_user # Kullanýcýn Kimliðini Alalým

	await message.reply_text(text="**Merhaba {}!**\n\n__Ben Pyrogram Api Ýle Yazýlmýþ Eðlence Botuyum :)__\n\n**Repom =>** [Open Source](https://github.com/AkinYoungSoftware/TgEglenceBot)\nDoðruluk mu? Cesaret mi? Oyun Komutu => /dc".format(
		user.mention, # Kullanýcý'nýn Adý
		),
	disable_web_page_preview=True, # Etiketin Önizlemesi Olmamasý Ýcin Kullanýyoruz
	reply_markup=button() # Buttonlarýmýzý Ekleyelim
	)

# Dc Komutu Ýcin Olan Buttonlar
def d_or_c(user_id):
	BUTTON = [[InlineKeyboardButton(text="? Doðruluk", callback_data = " ".join(["d_data",str(user_id)]))]]
	BUTTON += [[InlineKeyboardButton(text="?? Cesaret", callback_data = " ".join(["c_data",str(user_id)]))]]
	return InlineKeyboardMarkup(BUTTON)

# Dc Komutunu Oluþturalým
@K_G.on_message(filters.command("dc"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="{} Ýstediðin Soru Tipini Seç!".format(user.mention),
		reply_markup=d_or_c(user.id)
		)

# Buttonlarýmýzý Yetkilendirelim
@K_G.on_callback_query()
async def _(client, callback_query):
	d_soru=random.choice(D_LÝST) # Random Bir Doðruluk Sorusu Seçelim
	c_soru=random.choice(C_LÝST) # Random Bir Cesaret Sorusu Seçelim
	user = callback_query.from_user # Kullanýcýn Kimliðini Alalým

	c_q_d, user_id = callback_query.data.split() # Buttonlarýmýzýn Komutlarýný Alalým

	# Sorunun Sorulmasýný Ýsteyen Kiþinin Komutu Kullanan Kullanýcý Olup Olmadýðýný Kontrol Edelim
	if str(user.id) == str(user_id):
		# Kullanýcýnýn Doðruluk Sorusu Ýstemiþ Ýse Bu Kýsým Calýþýr
		if c_q_d == "d_data":
			await callback_query.answer(text="Doðruluk Sorusu Ýstediniz", show_alert=False) # Ýlk Ekranda Uyarý Olarak Gösterelim
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id) # Eski Mesajý Silelim

			await callback_query.message.reply_text("**{user} Doðruluk Sorusu Ýstedi:** __{d_soru}__".format(user=user.mention, d_soru=d_soru)) # Sonra Kullanýcýyý Etiketleyerek Sorusunu Gönderelim
			return

		if c_q_d == "c_data":
			await callback_query.answer(text="Cesaret Sorusu Ýstediniz", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id)
			await callback_query.message.reply_text("**{user} Cesaret Sorusu Ýstedi:** __{c_soru}__".format(user=user.mention, c_soru=c_soru))
			return


	# Buttonumuza Týklayan Kisi Komut Calýþtýran Kiþi Deðil Ýse Uyarý Gösterelim
	else:
		await callback_query.answer(text="Komutu Kullanan Kiþi Sen Deðilsin!!", show_alert=False)
		return

############################
    # Sudo islemleri #
@K_G.on_message(filters.command("cekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Sen Yetkili Birisi degilsin!!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Eklenmesini istedigin Cesaret Sorunu Giriniz!**")
  
@K_G.on_message(filters.command("dekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Sen Yetkili Birisi degilsin!!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Eklenmesini istedigin Dogruluk Sorunu Giriniz!**")

@K_G.on_message(filters.private)
async def _(client, message):
  global MOD
  global C_LÝST
  global D_LÝST
  
  user = message.from_user
  
  if user.id in OWNER_ID:
    if MOD=="cekle":
      C_LÝST.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Metin Cesaret Sorusu Olarak Eklendi!__")
      return
    if MOD=="dekle":
      C_LÝST.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Metin Dogruluk Sorusu Olarak Eklendi!__")
      return
############################

K_G.run() # Botumuzu Calýþtýralým :)
