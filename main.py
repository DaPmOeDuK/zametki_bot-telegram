import telebot
from telebot.types import Message, ReplyKeyboardMarkup as RKM, ReplyKeyboardRemove as RKR
from telebot.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB, CallbackQuery
from config import TOKEN
from data_bases import *

bot = telebot.TeleBot(TOKEN)
temp = {}
clear = RKR()


@bot.message_handler(commands=["start"])
def start(m: Message):
    if new_usr(m):
        temp[m.chat.id] = {}
        zametkil = []
        zametkil.append(m.chat.id)
        zametkil.append([])
        zametkil.append([])
        zametki.write(zametkil)
        menu(m)
        return
    else:
        menu(m)
        return


def new_usr(m: Message):
    db = zaetki.read_all()
    for i in db:
        if m.chat.id == i[0]:
            return False
    return True


@bot.message_handler(commands=["меню"])
def menu(m:Message):
    kb = RKM(True, True)
    kb.row("Добавить заметку","Посмотреть мои заметки", "Отметить заметку как выполненную", 'очистить выполненные заметки')
    bot.send_message(m.chat.id,'Что Вы хотите сделать?', reply_markup=kb)
    bot.register_next_step_handler(m, reg1)


def as_compl(m:Message):
    zametkil = zametki.read("user_id",m.chat.id)
    kb = RKM(True, True)
    for i in zametkil[1]:
        kb.add(i)
    bot.send_message(m.chat.id,"Какое дело Вы выполнили?",reply_markup=kb)
    bot.register_next_step_handler(m,reg_compl_zam)


def new_zam(m:Message):
    bot.send_message(m.chat.id,"Напишите, как называется Ваша заметка")
    bot.register_next_step_handler(m,reg_new_zam)


def clear_zam(m:Message):
    zametkil = zametki.read("user_id", m.chat.id)
    zametkil[2].clear()
    zametki.write(zametkil)
    bot.send_message(m.chat.id, "Заметки очищены")
    menu(m)
    return


def check_zam(m:Message):
    zametkil = zametki.read("user_id", m.chat.id)
    text = "Невыполненные:\n"
    for i in zametkil[1]:
        text += i+"\n"
    bot.send_message(m.chat.id,text)
    text = "Выполненные:\n"
    for i in zametkil[2]:
        text += i + "\n"
    bot.send_message(m.chat.id, text)
    menu(m)
    return


def reg1(m:Message):
    if m.text == "Добавить заметку":
        new_zam(m)
        return
    elif m.text == "Отметить заметку как выполненную":
        as_compl(m)
        return
    elif m.text == 'очистить выполненные заметки':
        clear_zam(m)
        return
    elif m.text == "Посмотреть мои заметки":
        check_zam(m)
        return

def reg_new_zam(m:Message):
    zametkil = zametki.read("user_id", m.chat.id)
    zametkil[1].append(m.text.lower())
    zametki.write(zametkil)
    bot.send_message(m.chat.id,"Заметка добавлена")
    menu(m)
    return


def reg_compl_zam(m:Message):
    zametkil = zametki.read("user_id", m.chat.id)
    zametkil[1].pop(zametkil[1].index(m.text))
    zametkil[2].append(m.text)
    zametki.write(zametkil)
    bot.send_message(m.chat.id,"Заметка добавлена в выполненные")
    menu(m)
    return


bot.infinity_polling()