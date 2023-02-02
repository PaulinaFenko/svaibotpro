import telebot
from telebot import types
import time
from datetime import datetime, timedelta
import threading

bot = telebot.TeleBot('5974405967:AAE6gKS8tezauunomqw4XiWyk9eq8iUXsr8')  # Токен бота в телеграм

users_access = {}  # Запоминаем введенные данные для рассчета по каждому пользователю


# Проверяем нажал ли пользователь кнопку ОК в течение двух секунд
def tg_check(x):
    while True:
        for user_id in users_access:
            time_wait = users_access[user_id]["wait_ok"]  # время когда пользователя нужно перенести в начало диалога
            if users_access[user_id]["wait_ok"] != False:
                if time_wait < datetime.now():
                    users_access[user_id]["wait_ok"] = False
                    start(user_id)


threading.Thread(target=tg_check, args=([(1, 2)])).start()  # Проверяем нажал ли пользователь кнопку ОК (за 2 секунды)

# Типы грунтов, которые будут использоваться в программе
list_soils = ["Песок плотный", "Песок рыхлый", "Супесь", "Глина твердая", "Глина мягкопластичная", "Глина юрская",
              "Суглинок", "Насыпной грунт", "Мергель"]


# Указываем приветственное сообщение
@bot.message_handler(commands=["start"])
def start(message):
    if str(message).isdigit():  # Если пользователь возвращается сюда из середины меню
        user_id = message
    else:
        user_id = message.chat.id  # Ид пользователя
        bot.send_message(user_id, "Привет, я помогу тебе рассчитать усилие вдавливания 💪")

    # Запоминаем данные пользователя для последующих проверок на каком этапе находится пользователь
    users_access.update({user_id: {"piles": False,
                                   "L": False,
                                   "wait_ok": False,
                                   "soil": False,
                                   "H": False,
                                   "E1": False,
                                   "E2": False}})

    # Выводим печерень параметров сваи
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton('300', callback_data='piles_300'))
    key.add(types.InlineKeyboardButton('350', callback_data='piles_350'))
    key.add(types.InlineKeyboardButton('400', callback_data='piles_400'))
    bot.send_message(user_id, "Выберите сечение сваи S, в мм: ", reply_markup=key)


# Проверяем корректность введенных данных длины сваи
def check_piles(user_id, piles, length):
    if piles == 300 and length <= 12:
        type_soil(user_id)
    elif piles == 350 and length <= 14:
        type_soil(user_id)
    elif piles == 400 and length <= 16:
        type_soil(user_id)
    else:
        # Если длина сваи находится не в требуемых условиях и нужно задать уточняющий вопрос
        key = types.InlineKeyboardMarkup()
        key.add(types.InlineKeyboardButton('Да', callback_data='yes_check'))
        key.add(types.InlineKeyboardButton('Нет', callback_data='no_check'))
        bot.send_message(user_id, "Похоже, свая составная? ", reply_markup=key)


# Проверяем корректность введенных данных глубины кровли
def check_roof(user_id, length, roof):
    if length < roof:  # Если глубина кровли находится не в требуемых условиях и нужно задать уточняющий вопрос
        key = types.InlineKeyboardMarkup()
        key.add(types.InlineKeyboardButton('Длину сваи', callback_data='change_pile'))
        key.add(types.InlineKeyboardButton('Выберем другой слой грунта', callback_data='other_soil'))
        bot.send_message(user_id, "Острие сваи не достигает кровли выбранного грунта. Что изменим?", reply_markup=key)
    else:
        bot.send_message(user_id, "Введите усилие под острием зонда, в МПа:")


# Если пользователь нажал на кнопку сваи
def piles(user_id, name_call):
    users_access[user_id]["L"] = False
    users_access[user_id]["H"] = False
    users_access[user_id]["piles"] = int(name_call[6:])  # Запоминаем выбор пользователя
    bot.send_message(user_id, "Укажите длину сваи, в м:")


# Если пользователь ответил, что свая составная
def yes_check(user_id):
    piles = users_access[user_id]["piles"]  # Сечение сваи, которое выбрал пользователь
    piles_length = users_access[user_id]["L"]  # Сечение сваи, которое выбрал пользователь в мм

    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton('Да', callback_data='yes'))
    key.add(types.InlineKeyboardButton('Нет', callback_data='no'))
    bot.send_message(user_id, f"Введенные вами данные:\n\n"
                              f"Сечение сваи = {piles} м\n"
                              f"Длина сваи = {piles_length} м\n\n"
                              f"Все верно?", reply_markup=key)


# Если пользователь ответил, что свая не составная
def no_check(user_id):
    piles = users_access[user_id]["piles"]  # Сечение сваи, которое выбрал пользователь

    if piles == 300:
        piles_length = 12  # Максимальная длина сваи
    elif piles == 350:
        piles_length = 14  # Максимальная длина сваи
    elif piles == 400:
        piles_length = 16  # Максимальная длина сваи

    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton('ок', callback_data='ok'))
    bot.send_message(user_id, f"Максимальная длина сваи сечением {piles} мм не может превышать {piles_length} м",
                     reply_markup=key)

    # Засекаем две секунды
    users_access[user_id]["wait_ok"] = datetime.now() + timedelta(seconds=2)  # Когда нужно перенести в начало диалога


# Если сечение и длина сваи прошли проверку
def type_soil(user_id):
    users_access[user_id]["H"] = False
    users_access[user_id]["E1"] = False

    key = types.InlineKeyboardMarkup()
    for i in range(len(list_soils)):
        key.add(types.InlineKeyboardButton(f'{list_soils[i]}', callback_data=f'soil{i}'))
    bot.send_message(user_id, f"Выберите тип грунта:", reply_markup=key)


# Выбрал неправильный грунт
def bad_soil(user_id, soil):
    if soil == "soil4":
        soil = "глина мягкопластичная"
    else:
        soil = "насыпной грунт"
    bot.send_message(user_id, f"По СП {soil} не может служить основанием для свайного фундамента")
    type_soil(user_id)


# Выбрал правильный грунт
def good_soil(user_id, number_soil):
    users_access[user_id]["soil"] = list_soils[number_soil]
    bot.send_message(user_id, f"Введите глубину, на которой расположена кровля самого твердого грунта, "
                              f"в метрах от поверхности земли:")


# Проверяем введенное усилие под острием зонда
def force_under_probe(user_id, force):
    if force > 50:
        bot.send_message(user_id, f"Введенное усилие под острием зонда превышает 50 МПа, требуется выбрать другой "
                                  f"тип грунта")
        type_soil(user_id)
    else:
        bot.send_message(user_id, "Введите усилие по боковой поверхности зонда, в КПа:")


# Проверяем введенное усилие под острием зонда
def effort(user_id):
    S = users_access[user_id]["piles"]  # Сечение сваи (мм)
    L = users_access[user_id]["L"]  # Длина сваи (м)
    T = users_access[user_id]["soil"]  # Тип грунта (фраза)
    H = users_access[user_id]["H"]  # Глубина кровли  (м)
    E1 = users_access[user_id]["E1"]  # Усилие под острием зонда  (МПа)
    E2 = users_access[user_id]["E2"]  # Усилие по боковой поверхности зонда (КПа)

    # Расчет усилия
    ES = (S + L) * H * E1 + (L - H) * E2
    bot.send_message(user_id, f"Введенные вами данные:\n\n"
                              f"Сечение сваи: {S} мм\n"
                              f"Длина сваи: {L} м\n"
                              f"Тип грунта: {T}\n"
                              f"Глубина кровли: {H} м\n"
                              f"Усилие под острием зонда: {E1} МПа\n"
                              f"Усилие по боковой поверхности зонда: {E2} КПа\n")
    bot.send_message(user_id,
                     f"Для прорезания песка с модулем деформации, равным {E1}, сваей сечением {S} мм требуется усилие {int(ES)} тонн")
    if ES >= 250:
        img = open("table.png", 'rb')
        bot.send_photo(user_id, img, caption="Удостоверьтесь, что свая не сломается", parse_mode="html")

    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton('Да', callback_data='yes_end'))
    key.add(types.InlineKeyboardButton('Нет', callback_data='no_end'))
    bot.send_message(user_id, "Посчитаем другой слой?", reply_markup=key)


# Действие при нажатии на кнопку
@bot.callback_query_handler(func=lambda call: call.data)
def answer(call):
    user_id = call.from_user.id  # Ид пользователя
    name_call = call.data  # Название нажатой кнопки
    if "piles" in call.data:  # Нажал на любую кнопку с с любым сечением сваи
        piles(user_id, name_call)
    elif "yes_check" == call.data:  # Ответил, что свая составная
        yes_check(user_id)
    elif "no_check" == call.data:  # Ответил, что свая не составная
        no_check(user_id)
    elif "yes" == call.data:  # Подтвердил данные по сечению и длине сваи
        type_soil(user_id)
    elif "no" == call.data or "ok" == call.data:  # Не подтвердил данные по сечению и длине сваи или свая не составная
        start(user_id)
    elif "change_pile" == call.data:  # Решил изменить длину сваи
        piles(user_id, f"piles_{users_access[user_id]['piles']}")
    elif "other_soil" == call.data:  # Решил изменить слой грунта
        type_soil(user_id)
    elif "yes_end" == call.data:  # В конце всего диалога нажал да
        start(user_id)
    elif "no_end" == call.data:  # В конце всего диалога нажал нет
        bot.send_message(user_id, "Досвидания!")
    elif "soil4" == call.data or "soil7" == call.data:  # Выбрал неправильный грунт
        bad_soil(user_id, call.data)
    elif "soil" in call.data:  # Выбрал правильный грунт
        good_soil(user_id, int(call.data[4:]))


# Работа бота при написании любого текста
@bot.message_handler(content_types=['text'])
def text(message):
    user_id = message.from_user.id  # Ид пользователя
    text = message.text  # Текст пользователя
    if user_id in users_access:  # Если пользователь ранее нажимал кнопку Start
        # Пользователь ввел длину длину сваи
        if users_access[user_id]["piles"] != False and users_access[user_id]["L"] == False:
            if text.isdigit():  # Проверяем чтобы пользователь ввел целочисленное значение
                users_access[user_id]["L"] = int(text)
                check_piles(user_id, users_access[user_id]["piles"], int(text))  # Проверяем введеную длину сваи
            else:
                bot.send_message(user_id, "Вы ввели некорректное значение, повторите ввод:")

        # Пользователь ввел глубину кровли
        elif users_access[user_id]["piles"] != False and users_access[user_id]["L"] != False and users_access[user_id][
            "H"] == False:
            text_check = text.replace(".", "")
            if text_check.isdigit():  # Проверяем чтобы пользователь ввел число с плавающей точкой или целое число
                users_access[user_id]["H"] = float(text)
                check_roof(user_id, users_access[user_id]["L"], users_access[user_id]["H"])  # Проверяем глубину кровли
            else:
                bot.send_message(user_id, "Вы ввели некорректное значение, повторите ввод:")

        # Пользователь ввел усилие под острием зонда
        elif users_access[user_id]["piles"] != False and users_access[user_id]["L"] != False and \
                users_access[user_id]["H"] != False and users_access[user_id]["E1"] == False:
            if text.isdigit():  # Проверяем чтобы пользователь ввел целочисленное значение
                users_access[user_id]["E1"] = int(text)
                force_under_probe(user_id, users_access[user_id]["E1"])  # Проверяем введенное усилие под острием зонда
            else:
                bot.send_message(user_id, "Вы ввели некорректное значение, повторите ввод:")

        # Пользователь ввел усилие по боковой поверхности зонда
        elif users_access[user_id]["piles"] != False and users_access[user_id]["L"] != False and users_access[user_id][
            "H"] != False \
                and users_access[user_id]["E1"] != False and users_access[user_id]["E2"] == False:
            if text.isdigit():  # Проверяем чтобы пользователь ввел целочисленное значение
                users_access[user_id]["E2"] = int(text)
                effort(user_id)  # Рассчитываем усилие (главная формула)
            else:
                bot.send_message(user_id, "Вы ввели некорректное значение, повторите ввод:")


# Код для бесперебойной работы бота
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(1)
