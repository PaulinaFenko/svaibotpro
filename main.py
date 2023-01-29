import telebot
from telebot import types

bot = telebot.TeleBot("5974405967:AAE6gKS8tezauunomqw4XiWyk9eq8iUXsr8")

s_svai = 0
l_svai = 0
l_grunt = 0
Mpa_z = 0
Klpa_z = 0
t_s_ost = 0
t_s_bok = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Hi")
    btn2 = types.KeyboardButton("Введите сечение сваи в миллиметрах.")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text=".".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Hi":
        bot.send_message(message.chat.id, text=".")
    elif message.text == "Введите сечение сваи в миллиметрах.":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("300")
        btn2 = types.KeyboardButton("350")
        back = types.KeyboardButton("400")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text=".", reply_markup=markup)

    elif message.text == "300":
        bot.send_message(message.chat.id, "Сечение 300 мм.")


    elif message.text == "350":
        bot.send_message(message.chat.id, "Сечение 350 мм.")


    elif message.text == "400":
        bot.send_message(message.chat.id, "Сечение 400 мм.")
    bot.register_next_step_handler(message, dlina_svai)


def dlina_svai(message):
    global s_svai
    s_svai = int(message.text)
    bot.send_message(message.chat.id, text="Введите длину сваи в метрах.")
    bot.register_next_step_handler(message, dlina)


def dlina(message):
    global l_svai
    l_svai = int(message.text)
    if s_svai == 300:
        if l_svai > 12:
            bot.send_message(message.chat.id, "Свая составная?")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Да.")
            btn2 = types.KeyboardButton("Нет.")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text=".", reply_markup=markup)

        elif message.text == 'Да.':
            bot.send_message(message, '.')

        elif message.text == 'Нет.':
            bot.send_message(message, '''Так быть не может''')
            #должен отправиться в функцию dlina_svai

        else:
            bot.send_message(message.chat.id, f"Длина сваи: {l_svai}")
    if s_svai == 350:
        if l_svai > 14:
            bot.send_message(message.chat.id, "Свая составная?")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Да.")
            btn2 = types.KeyboardButton("Нет.")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text=".", reply_markup=markup)

        elif message.text == 'Да.':
            bot.send_message(message, '.')

        elif message.text == 'Нет.':
            bot.send_message(message, '''Так быть не может''')
            # должен отправиться в функцию dlina_svai
        else:
            bot.send_message(message.chat.id, f"Длина сваи: {l_svai}")
    if s_svai == 400:
        if l_svai > 16:
            bot.send_message(message.chat.id, "Свая составная?")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Да.")
            btn2 = types.KeyboardButton("Нет.")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text=".", reply_markup=markup)

        elif message.text == 'Да.':
            bot.send_message(message, '.')

        elif message.text == 'Нет.':
            bot.send_message(message, '''Так быть не может''')
            # должен отправиться в функцию dlina_svai
        else:
            bot.send_message(message.chat.id, f"Длина сваи: {l_svai}")
    bot.send_message(message.chat.id, "Укажите глубину залегания в метрах самого прочного грунта")
    bot.register_next_step_handler(message, glubina)


def glubina(message):
    global l_grunt
    l_grunt = int(message.text)
    if l_grunt <= l_svai:
        bot.send_message(message.chat.id, text="Теперь введите максимальную прочность Е, Мпа под осторием зонда")
    else:
        bot.send_message(message.chat.id,
                         text="Глубина грунта не может быть больше длины сваи. Вы ошиблись в параметрах"
                              "грунта или длины сваи?")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Длина сваи.")
        btn2 = types.KeyboardButton("Грунта.")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text=".", reply_markup=markup)
        # В зависимости от ответа дожны перенаправляться в функцию либо длины сваи, либо длины грунта
    bot.register_next_step_handler(message, zond_ost)


def zond_ost(message):
    global Mpa_z
    Mpa_z = int(message.text)
    bot.send_message(message.chat.id,
                     text="Теперь введите максимальную прочность грунта Е, Лпа по боковой поверхности зонда")
    bot.register_next_step_handler(message, zond_bok)


def zond_bok(message):
    global Klpa_z
    Klpa_z = int(message.text)
    bot.send_message(message.chat.id,
                     text="Теперь введите тонн под острием сваи")
    bot.register_next_step_handler(message, si_ostr)


def si_ostr(message):
    global t_s_ost
    t_s_ost = int(message.text)
    bot.send_message(message.chat.id,
                     text="Теперь введите тонн по боковой поверхности сваи")
    bot.register_next_step_handler(message, prover)


def prover(message):
    global t_s_bok
    t_s_bok = int(message.text)
    if t_s_ost > 40:
        bot.send_message(message.chat.id,
                         text="Вы неправильно указали усилие в тоннах под острием сваи")
        # должен отправиться в функцию zond_bok
    if t_s_bok > 40:
        bot.send_message(message.chat.id,
                         text="Вы неправильно указали усилие в тоннах по боковой поверхности сваи")
        # должен отправиться в функцию si_ostr
    bot.register_next_step_handler(message, konec)


def konec(message):
    bot.send_message(message.chat.id,
                     text=f"Для того чтобы проколоть грунт, кровля которого расположена на {l_grunt} метров, "
                          f"а сопротивление"
                          f"под острием зонда составляет {Mpa_z} мега паскалей, а по боковой поверхности - "
                          f"{Klpa_z} килопаскалей"
                          f"на сваю сечением {s_svai} * {s_svai} миллиметров и длиной {l_svai} "
                          f"метров необходимо приложить"
                          f"усилие в "
                          f"{s_svai * s_svai * 0.01 * Mpa_z * 10.19711621 + l_svai * 100 * 0.1 * s_svai * 4 * Klpa_z + 0.01097162}")


bot.polling(none_stop=True)
