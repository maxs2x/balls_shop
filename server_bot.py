import aiohttp
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_polling
from aiogram.utils.emoji import emojize
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, code, italic, text

import app
import config
import admin
from keyboard import *
import db_hendler


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, 'Служба доставки гелиевых шариков в Кирове. Выберите нужный пункт в меню',
                    reply_markup=main_menu_kb)
    await app.add_user(message.chat.id)

@dp.message_handler(commands=['admin'])
async def cmd_start(message: types.Message):
    con2 = db_hendler.DB_select()
    con = db_hendler.DB_insert()
    tut = con2.string_with_value('user_id', 'user_data', "user_id", str(message.chat.id))
    print(tut[0][0])
    if str(tut[0][0]) != str(message.chat.id):
        con.full_string('user_data', ['user_id'], [str(message.chat.id)])
    await bot.send_message(message.chat.id, 'Выбери нужное действие',
                    reply_markup=admin_menu_kb)


@dp.message_handler(lambda message: message.md_text and ';' in message.md_text)
async def add_product(message: types.Message):
    if message.md_text.count(';') >= 1:
        print('handler')
        con = DB_select()
        status = con.string_with_value('callback_in', 'user_data', 'user_id', str(message.chat.id))
        if str(status[0][0]) == 'add_prod':
            await admin.parse_text(message.chat.id, message.md_text)


@dp.message_handler(content_types='photo')
async def input_photo(message: types.ContentType.PHOTO):
    download_photo = message.photo[2].file_id
    see_cache = DB_select()
    insert_photo = DB_update()
    cache = see_cache.string_with_value('cache', 'user_data', 'user_id', message.chat.id)
    callback_in = see_cache.string_with_value('callback_in', 'user_data', 'user_id', message.chat.id)
    if cache[0][0] == 'photo' and callback_in[0][0] != 'red_prod':
        arr_uniq_id = app.search_max_uniq_id()
        insert_photo.string_with_value(arr_uniq_id[1], 'file_id', 'uniq_id', arr_uniq_id[0], download_photo)
        insert_photo.string_with_value('user_data', 'cache', 'user_id', message.chat.id, 'added')
    elif callback_in[0][0] == 'red_prod':
        insert_photo.string_with_value('user_data', 'cache', 'user_id', message.chat.id, download_photo)
    elif callback_in[0][0] == 'add_prod' or callback_in[0][0][:11] == 'enter_field':
        new_cache = str(cache[0][0]) + ';' + str(download_photo)
        insert_photo.string_with_value('user_data', 'cache', 'user_id', message.chat.id, new_cache)


@dp.message_handler(content_types='text')
async def cmd_menu(message: types.Message):
    print(message.md_text)
    cht_id = message.chat.id
    forw_id = message.message_id
    db_obj = db_hendler.DB_update()
    db_select = db_hendler.DB_select()
    callback_in = db_select.string_with_value('callback_in', 'user_data', 'user_id', cht_id)
    if message.md_text == '✅  Подтвердить  ✅':
        status = await app.verifi_phone(cht_id, forw_id)
        print(status)
        if status == 'done':
            await app.format_order(cht_id)
            await app.nav_back(cht_id, forw_id, 'four')
            await bot.send_message(cht_id, 'Заказ успешно отправлен. Спасибо за покупку!', reply_markup=back_categories_kb)
            await app.remove_all_cart(cht_id)
        else:
            db_obj.string_with_value('user_data', 'phone', 'user_id', cht_id, None)
    elif message.md_text != '✅  Подтвердить  ✅' and callback_in[0][0] != 'add_prod' and callback_in[0][0] != 'red_prod' and callback_in[0][0][:11] != 'enter_field':
        in_cart = db_select.string_with_value('in_cart', 'user_data', 'user_id', cht_id)
        print(in_cart)
        if in_cart[0][0] != None and callback_in[0][0] != 'red_prod':
            db_obj.string_with_value('user_data', 'phone', 'user_id', cht_id, message.md_text)
    elif callback_in[0][0] == 'add_prod' or callback_in[0][0][:11] == 'enter_field':
        cache = db_select.string_with_value('cache', 'user_data', 'user_id', cht_id)[0][0]
        if cache != None:
            if cache.count(';') == 0:
                valid = admin.ValidationInput.price(message.md_text)
                if valid == True:
                    new_cache = cache + ';' + message.md_text
                else:
                    await app.nav_back(message.chat.id, int(message.message_id), 'one_one')
                    print(callback_in[0][0])
                    callback = callback_in[0][0][:-1] + '2'
                    enter_product_kb = await RedactCartKB.enter_product_kb(callback)
                    await bot.send_message(cht_id, 'Отправленое сообщение должно состоять из цифр',
                                           reply_markup=enter_product_kb)
                    new_cache = cache
            elif cache.count(';') == 1:
                await app.nav_back(message.chat.id, int(message.message_id), 'four')
                print(callback_in[0][0])
                enter_product_kb = await RedactCartKB.enter_product_kb(callback_in[0][0])
                await bot.send_message(cht_id, 'Отправленое сообщение не является изображением', reply_markup=enter_product_kb)
                new_cache = cache
        else:
            new_cache = message.md_text

        db_obj.string_with_value('user_data', 'cache', 'user_id', message.chat.id, new_cache)
    elif 1 < len(message.md_text) < 100:
        print(callback_in)
        if callback_in[0][0] == 'red_prod':
            db_obj.string_with_value('user_data', 'cache', 'user_id', cht_id, message.md_text)



@dp.callback_query_handler(lambda callback_query: True)
async def some_callback_handler(callback_query: types.CallbackQuery):
    print(callback_query)
    call_back = callback_query.data
    cht_id = callback_query.message.chat.id
    forw_id = callback_query.message.message_id


    async def _send_fun_(call_back, chat_id, forw_id):
        # Блок основного меню
        if call_back == 'start':
            await bot.send_message(cht_id, '.............. ', reply_markup=remove_kb)
            await app.nav_back(cht_id, forw_id, 'no')
            await bot.delete_message(cht_id, str(int(forw_id) + 1))
            await bot.send_message(chat_id, 'Служба доставки гелиевых шариков в Кирове. Выберите нужный пункт в меню',
                                   reply_markup=main_menu_kb)
        elif call_back == 'categories':
            await app.nav_back(chat_id, forw_id, 'no')
            await bot.send_message(chat_id, 'Выберите одну из категорий', reply_markup=categories_kb)
        elif call_back == 'about':
            await app.nav_back(cht_id, forw_id, 'no')
            await bot.send_message(chat_id, 'Tелефон:  +7 (953) 696-28-31 ')
            await bot.send_message(chat_id, 'https://vk.com/gelievye.shariki.vkirove', reply_markup=back_categories_kb, reply_to_message_id=str(int(forw_id) + 1))
            await bot.delete_message(cht_id, str(int(forw_id) + 1))
        elif call_back == 'cart':
            await app.nav_back(cht_id, forw_id, 'yes')
            await app.in_cart(cht_id)

        # Блок меню корзины
        if call_back == 'remove_cart':
            await app.nav_back(cht_id, forw_id, 'yes')
            await app.remove_all_cart(cht_id)
            await app.in_cart(cht_id)
        elif call_back[:8] == 'by_order':
            print(call_back)
            await app.nav_back(cht_id, forw_id, 'no')
            if len(call_back) == 8:
                await app.order_by(cht_id, phone=None)
            elif call_back[9:] == 'phone':
                await app.order_by(cht_id, phone='redact')
            elif call_back[9:] == 'true_phone':
                await app.format_order(cht_id)
                await app.nav_back(cht_id, forw_id, 'one_one')
                await bot.send_message(cht_id, 'Заказ успешно отправлен. Спасибо за покупку!',
                                       reply_markup=back_categories_kb)
                await app.remove_all_cart(cht_id)

        # Блок навигации назад
        if call_back == 'back_start':
            await app.nav_back(cht_id, forw_id, 'one_one')
            await _send_fun_('start', chat_id, forw_id)
        elif call_back == 'back_categories':
            await app.nav_back(cht_id, forw_id, 'yes')
            await _send_fun_('categories', chat_id, forw_id)

        #Блок отображения карточек товара
        if call_back == 'imgfolga' or call_back == 'imggelii' or call_back == 'imgkmpzc':
            await app.send_product_kart(call_back, cht_id, forw_id)
        elif call_back[:7] == 'add_upp':
            await bot.answer_callback_query(callback_query.id, cache_time=0.5)
            await app.add_remove(cht_id, forw_id, call_back, None)
        elif call_back[:7] == 'add_end':
            await bot.answer_callback_query(callback_query.id, cache_time=0.5)
            await app.add_remove(cht_id, forw_id, call_back, back_categories)
        elif call_back[:10] == 'remove_upp':
            await bot.answer_callback_query(callback_query.id, cache_time=0.5)
            await app.add_remove(cht_id, forw_id, call_back, None)
        elif call_back[:10] == 'remove_end':
            await bot.answer_callback_query(callback_query.id, cache_time=0.5)
            await app.add_remove(cht_id, forw_id, call_back, back_categories)

        #Функционал админа
        if call_back == 'add_prod' or call_back == 'del_prod' or call_back == 'red_prod':
            await app.nav_back(cht_id, forw_id, 'no')
            await admin.enter_admin(call_back, cht_id)
        elif call_back == 'admin_select_imggelii' or call_back == 'admin_select_imgfolga' or call_back == 'admin_select_imgkmpzc':
            await app.nav_back(cht_id, forw_id, 'no')
            await admin.get_data(call_back, cht_id, forw_id)
            print(forw_id)
        elif call_back[:11] == 'enter_field':
            await app.nav_back(cht_id, forw_id, 'no')
            await admin.AdminAddProdukt.enter_product(cht_id, call_back, forw_id)
        elif call_back[:11] == 'set_product':
            await app.nav_back(cht_id, int(forw_id) + 1, 'one_one')
            await admin.AdminAddProdukt.set_product(cht_id, call_back, forw_id)
        elif call_back[:11] == 'admin_added':
            await app.nav_back(cht_id, forw_id, 'no')
            await admin.set_data(call_back, cht_id, forw_id)
        elif call_back[:10] == 'delet_card':
            await admin.delet_card(call_back, cht_id, forw_id)
        elif call_back == 'start_admin':
            await app.nav_back(cht_id, forw_id, 'yes_every')
            await bot.send_message(cht_id, 'Выбери нужное действие',
                                   reply_markup=admin_menu_kb)
        elif call_back[:6] == 'choose':
            await app.nav_back(cht_id, forw_id, 'no')
            await admin.AdminCardForRedact.redact_card(cht_id, call_back)
        elif call_back[:6] == 'redact':
            #await app.nav_back(cht_id, forw_id, 'two')
            await admin.AdminCardForRedact.modify_card(cht_id, call_back, forw_id)
        elif call_back[:9] == 'do_redact':
            do = await admin.AdminCardForRedact.do_redact(cht_id, call_back, forw_id)
            await app.nav_back(cht_id, forw_id, 'two')
            if do == 'ok':
                await bot.send_message(cht_id, 'Карточка успешно отредактирована. Выбери нужное действие',
                                   reply_markup=admin_menu_kb)


    #Эта функция нужна для реализации кнопки "Назад"
    await _send_fun_(call_back, cht_id, forw_id)


if __name__ == '__main__':
    start_polling(dp, skip_updates=True)