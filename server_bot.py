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
    app.add_user(message.from_user.id)

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
    cache = see_cache.string_with_value('cache', 'user_data', 'user_id', message.chat.id)
    if cache[0][0] == 'photo':
        arr_uniq_id = app.search_max_uniq_id()
        insert_photo = DB_update()
        insert_photo.string_with_value(arr_uniq_id[1], 'file_id', 'uniq_id', arr_uniq_id[0], download_photo)
        insert_photo.string_with_value('user_data', 'cache', 'user_id', message.chat.id, 'added')


@dp.message_handler(content_types='text')
async def cmd_menu(message: types.Message):
    print(message.md_text)
    cht_id = message.chat.id
    forw_id = message.message_id

    if message.md_text == '✅  Подтвердить  ✅':
        status = await app.verifi_phone(cht_id, forw_id)
        if status == 'done':
            await app.format_order(cht_id)
            await app.nav_back(cht_id, forw_id, 'thre')
            await bot.send_message(cht_id, 'Заказ успешно отправлен. Спасибо за покупку!', reply_markup=back_categories_kb)
            await app.remove_all_cart(cht_id)
        else:
            await app.nav_back(cht_id, forw_id, 'two')
            db_obj = db_hendler.DB_update()
            db_obj.string_with_value('user_data', 'phone', 'user_id', cht_id, None)
    elif message.md_text != '✅  Подтвердить  ✅':
        db_select = db_hendler.DB_select()
        callback_in = db_select.string_with_value('in_cart', 'user_data', 'user_id', cht_id)
        print(callback_in)
        if callback_in[0][0] != None:
            db_obj = db_hendler.DB_update()
            db_obj.string_with_value('user_data', 'phone', 'user_id', cht_id, message.md_text)






@dp.callback_query_handler(lambda callback_query: True)
async def some_callback_handler(callback_query: types.CallbackQuery):
    call_back = callback_query.data
    cht_id = callback_query.message.chat.id
    forw_id = callback_query.message.message_id


    async def _send_fun_(call_back, chat_id, forw_id):
        # Блок основного меню
        if call_back == 'start':
            await app.nav_back(cht_id, forw_id, 'no')
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
        elif call_back == 'by_order':
            await app.nav_back(cht_id, forw_id, 'no')
            await bot.send_message(cht_id, 'Для уточнения деталей заказа введите Ваш номер телефона в формате 89ХХ ХХХ ХХХХ или +79ХХ ХХХ ХХХХ и нажмите кнопку ПОДТВЕРДИТЬ', reply_markup=okey_kb)

        # Блок навигации назад
        if call_back == 'back_start':
            await app.nav_back(cht_id, forw_id, 'no')
            await _send_fun_('start', chat_id, forw_id)
        elif call_back == 'back_categories':
            await app.nav_back(cht_id, forw_id, 'yes')
            await _send_fun_('categories', chat_id, forw_id)

        #Блок отображения карточек товара
        if call_back == 'imgfolga' or call_back == 'imggelii' or call_back == 'imgkmpzc':
            await app.send_product_kart(call_back, cht_id, forw_id)
        elif call_back == 'add':
            await app.add_remove(cht_id, forw_id, 'add', None)
        elif call_back == 'add_end':
            await app.add_remove(cht_id, forw_id, 'add', back_categories)
        elif call_back == 'remove':
            await app.add_remove(cht_id, forw_id, 'remove', None)
        elif call_back == 'remove_end':
            await app.add_remove(cht_id, forw_id, 'remove', back_categories)

        #Функционал админа
        if call_back == 'add_prod' or call_back == 'del_prod' or call_back == 'red_prod':
            await admin.enter_admin(call_back, cht_id)
        elif call_back == 'admin_select_imggelii' or call_back == 'admin_select_imgfolga' or call_back == 'admin_select_imgkmpzc':
            await admin.get_data(call_back, cht_id)
        elif call_back[:11] == 'admin_added':
            await admin.set_data(call_back, cht_id, forw_id)

    #Эта функция нужна для реализации кнопки "Назад"
    await _send_fun_(call_back, cht_id, forw_id)


if __name__ == '__main__':
    start_polling(dp, skip_updates=True)