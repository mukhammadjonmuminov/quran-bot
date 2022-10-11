import logging
import requests
import time
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from pprint import pprint as print
from openpyxl import load_workbook

API_TOKEN = '5721499429:AAGmOI67fTkmrfUyd-Xc5LF7J2XGcQyEOrQ'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    """
    Start buyrug'i chaqirilganda
    """
    # await message.answer(f"Salom {message.from_user.username}")
    # with open("new_users", "r") as file:
    #     file.write(message.from_user.full_name)
    time = datetime.now()
    print(f"{time.time()} connect: " + message.from_user.username)
    # a = 1
    # with open("users.txt", 'a') as file:
    #     m = file.read()
    #     file.write(f"{a}. {message.from_user.username} ------ {time.time()}")
    #     a += 1


        # file.close()
    await message.answer(f"Bismillah.\n Assalomu alaykum va rohmatullohi va barokatuh  \n{message.from_user.full_name} botga xush kelibsiz. \nBotdan foydalanish tartibi: /help\nMuallif: @pip_sudo")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
    Help buyrug'i chaqirilganda
    """
    await message.reply("""Botdan foydalanish uchun siz sura nomi va oyat tartib raqamini yoki bo'lmasa sura va oyat tartib raqamlarini kiritishingiz kerak.
    Misol uchun Fotiha surasining  3 - oyati haqida bilmoqchi bo'lsangiz, 
    Fotiha, 3 yoki 1, 3 tartibda yozishingiz kerak bo'ladi.\n
    Agar Suraning barcha oyatlari haqida bilmoqchi bo'lsangiz u holda, sura nomi yoki suraning tartib raqamini kiritishingizni o'zi kifoya. """)

def request_rsult(url):
    r = requests.get(url)
    print(r.status_code)
    res = r.json()
    return res

def request_all_sura():
    book = load_workbook('sura_new.xlsx')
    sheet = book.active
    rows = sheet.rows
    headers = [cell.value for cell in next(rows)]
    all_rows = []
    for row in rows:
        data = {}
        for title, cell in zip(headers, row):
            data[title] = cell.value

        all_rows.append(list(data.values()))
        # all_rows.append(data)

    # for i in all_rows:
    #     # k = list(i)
    #     sura_id, sura = i[1].split(".")
    #     oyat = i[2]
    #     print(sura.lower())

    return all_rows

@dp.message_handler()
async def echo(message: types.Message):
    tex = message.text.split(", ")

    tafsir = 'uzb-muhammadsodikmu'
    # if isinstance(tex[0], int) or ()
    if len(tex) == 1:
        if tex[0].isdigit():
            sura = int(tex[0])
            url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{tafsir}/{sura}.json"
            res = request_rsult(url)
            m = request_all_sura()[sura-1]
            a = 0
            await message.answer(f"""{m[1].split(".")[1]} surasi
            Tartib raqami - {sura}
            Oyatlar soni - {m[2]} oyatdan iborat.""")
            time.sleep(3)
            for i in res["chapter"]:
                a += 1
                await message.answer(f"{a} - oyat. " + i["text"])

        elif tex[0].isalpha():
            for i in request_all_sura():
                sura_id, sura = i[1].split(".")
                all_oyat = i[2]
                if tex[0].lower() == sura.lower():
                    url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{tafsir}/{sura_id}.json"
                    res = request_rsult(url)
                    a = 0
                    await message.answer(f"""{sura} surasi
                    Tartib raqami - {sura_id}
                    Oyatlar soni - {all_oyat} oyatdan iborat. """)
                    time.sleep(3)
                    for i in res["chapter"]:
                        a += 1
                        await message.answer(f"{a} - oyat. " + i["text"])


    elif len(tex) == 2:
        if tex[0].isdigit() and tex[1].isdigit():
            sura = int(tex[0])
            oyat = int(tex[1])
            url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{tafsir}/{sura}/{oyat}.json"
            res = request_rsult(url)
            for i in request_all_sura():
                m = i[1].split(".")
                if m[0] == str(sura):
                    await message.answer(f"""{m[1]} surasi
                                        Tartib raqami - {sura}
                                        Oyatlar soni - {i[2]} oyatdan iborat. """)
                    time.sleep(3)
                    await message.answer(f"{oyat} - oyat. " + res["text"])

        elif tex[0].isalpha() and tex[1].isdigit():
            for i in request_all_sura():
                sura_id, sura = i[1].split(".")
                if tex[0].lower() == sura.lower():
                    all_oyat = i[2]
                    oyat_id = int(tex[1])
                    url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{tafsir}/{sura_id}/{oyat_id}.json"
                    res = request_rsult(url)
                    await message.answer(f"""{sura} surasi
                    Tartib raqami - {sura_id}
                    Oyatlar soni - {all_oyat} oyatdan iborat. """)
                    time.sleep(3)
                    await message.answer(f"{tex[1]} - oyat. " + res["text"])



@dp.message_handler()
async def send_mm(message: types.Message):
    """
    Mavjud bo'lmagan buyrug' chaqirilganda
    """
    await message.reply("Siz noto'g'ri so'rov kiritdingiz!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
