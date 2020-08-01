import aiohttp
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_polling
from aiogram.utils.emoji import emojize
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, code, italic, text


import config
from keyboard import *
import db_hendler


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, 'Служба доставки гелиевых шариков в Кирове. Выберите нужный пункт в меню',
                    reply_markup=main_menu_kb)
    db_hendler.add_user(db_hendler.conn, message.from_user.id)


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
            db_hendler.update_table(db_hendler.conn, 'user_data', 'user_id', 'phone', None, cht_id)
    elif message.md_text != '✅  Подтвердить  ✅':
        if db_hendler.get_callback_fo_user_id(db_hendler.conn, cht_id)[3] != None:
            db_hendler.update_table(db_hendler.conn, 'user_data', 'user_id', 'phone', message.md_text, cht_id)




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

    #Эта функция нужна для реализации кнопки "Назад"
    await _send_fun_(call_back, cht_id, forw_id)


if __name__ == '__main__':
    start_polling(dp, skip_updates=True)