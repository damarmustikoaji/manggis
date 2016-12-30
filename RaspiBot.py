import sys
import time
import threading
import random
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import emoji
import platform
from netifaces import interfaces, ifaddresses, AF_INET
import os
import glob

path_motion = "Motion/images/camera1"

eclean = emoji.emojize(':no_entry_sign:')
episau = emoji.emojize(':hocho:')
ewatch = emoji.emojize(':guardsman:')
ememory = emoji.emojize(':floppy_disk:')
edevice = emoji.emojize(':strawberry:')
eping = emoji.emojize(':triangular_flag_on_post:')
emenu = emoji.emojize(':speech_balloon:')
ecountavi = emoji.emojize(':video_camera:')
emotion = emoji.emojize(':camera:')
ecountjpg = emoji.emojize(':rainbow:')
emyip = emoji.emojize(':round_pushpin:')
erestart = emoji.emojize(':performing_arts:')
ehelp = emoji.emojize(':notebook:')
elastavi = emoji.emojize(':outbox_tray:')
eclose = emoji.emojize(':no_entry:')
ehome = emoji.emojize(':house_with_garden:')

message_with_inline_keyboard = None

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command

    if command == '/start':
        markup = ReplyKeyboardMarkup(keyboard=[
                     #['Plain text', KeyboardButton(text='Text only')],
                     ['PING', 'IP', 'Tutup'],
                     ['Pantau'],
                     ['Unduh Motion', 'Unduh Video'],
                     ['Penyimpanan', 'Arsip'],
                     ['Bersihkan Arsip'],
                     ['Perangkatku','Bantuan'],
                     ['Hidup-Ulang PI'],
                 ])
        bot.sendMessage(chat_id, emoji.emojize('Menu ada disini ya :speech_balloon::hocho:'), reply_markup=markup)
    elif command == 'Tutup':
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, emoji.emojize("/start untuk kembali ke Menu :notebook_with_decorative_cover:"), reply_markup=markup)
    elif command == 'Bantuan':
        bot.sendMessage(chat_id, emoji.emojize(":notebook: Ini adalah layanan Bot Telegram untuk membantu dalam memonitoring Motion Detect pada Raspberry Pi yang dijadikan kamera pengawas dirumah Anda, berikut perintah yang bisa Anda kirimkan : :radio: PING :house_with_garden: Perangkatku :postbox: IP :hourglass: Penyimpanan. Atau dapat Anda temukan di Menu."))
    elif command == 'Perangkatku':
        platfou = ehome+" Platform Uname "+str(platform.uname())
        bot.sendMessage(chat_id, platfou)
    elif command == 'IP':
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
            bot.sendMessage(chat_id,'%s: %s' % (ifaceName, ', '.join(addresses)))
    elif command == 'Penyimpanan':
        folder_size = 0
        for (path, dirs, files) in os.walk(path_motion):
            for file in files:
                filename = os.path.join(path, file)
                folder_size += os.path.getsize(filename)
        results = "%0.1f MB" % (folder_size/(1024*1024.0))
        bot.sendMessage(chat_id, ememory+" "+results)
    elif command == 'Bersihkan Arsip':
        files_path = os.path.join(path_motion, "*")
        files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=False)
        results = len(glob.glob(files_path))
        if results:
            count = emoji.emojize(':books: ')+str(results)+" berkas(*.all)"
            bot.sendMessage(chat_id=chat_id, text=count)
            x = 0
            batas = results
            while x < batas:
                path = files[x]
                os.remove(path)
                x += 1
            bot.sendMessage(chat_id, emoji.emojize(":toilet: Menghapus Semua, :heavy_check_mark: Selesai!"))
        else:
            bot.sendMessage(chat_id, emoji.emojize(":name_badge: Tidak ada berkas"))
    elif command == 'Arsip':
        #JPG
        files_path = os.path.join(path_motion, "*.jpg")
        files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
        results = len(glob.glob(files_path))
        if results > 0:
            count = ecountjpg+" "+str(results)+" berkas(.jpg)"
            bot.sendMessage(chat_id, "JPG "+count)
        else:
            bot.sendMessage(chat_id, emoji.emojize(":name_badge: JPG: Tidak ada berkas"))
        #AVI
        files_path = os.path.join(path_motion, "*.avi")
        files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
        results = len(glob.glob(files_path))
        if results > 0:
            count = ecountavi+" "+str(results)+" berkas(.avi)"
            bot.sendMessage(chat_id, "AVI "+count)
        else:
            bot.sendMessage(chat_id, emoji.emojize(":name_badge: AVI: Tidak ada berkas"))
    elif command == 'PING':
        ping = "PING!!"+emoji.emojize(':round_pushpin:')
        bot.sendMessage(chat_id, ping)
    elif command == 'Unduh Motion':
        files_path = os.path.join(path_motion, "*.jpg")
        files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=False)
        results = len(glob.glob(files_path))
        if results:
            count = emotion+" "+str(results)+" berkas(.jpg), Mohon tunggu :"
            bot.sendMessage(chat_id=chat_id, text=count)
            x = 0
            batas = results
            while x < batas:
                bot.sendPhoto(chat_id=chat_id, photo=open(files[x], "rb"))
                time.sleep(3)
                path = files[x]
                os.remove(path)
                x += 1
            bot.sendMessage(chat_id, emoji.emojize(":heavy_check_mark: Selesai"))
        else:
            bot.sendMessage(chat_id, emoji.emojize(":name_badge: Tidak ada berkas"))
    elif command == 'Unduh Video':
        files_path = os.path.join(path_motion, "*.avi")
        files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
        results = len(glob.glob(files_path))
        if results:
            bot.sendMessage(chat_id, "Mohon tunggu, proses mengunduh AVI "+elastavi)
            x = 0
            batas = 1
            while x < batas:
                bot.sendVideo(chat_id=chat_id, video=open(files[x], "rb"))
                x += 1
        else:
            bot.sendMessage(chat_id, emoji.emojize(":name_badge: Tidak ada berkas"))
    elif command == 'Hidup-Ulang PI':
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, erestart+" Mohon tunggu untuk proses menghidupkan ulang raspberry pi "+ehome+" dan coba kembali /start untuk ke Menu, setelah -/+ 1 menit berikut ini.", reply_markup=markup)
        os.system('sudo shutdown -r now')

TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)
#bot.setWebhook()
bot.message_loop(handle, run_forever = 'I am listening ...')

while 1:
    time.sleep(10)
