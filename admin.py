import aiogram

from keyboard import *
import db_hendler
from db_hendler import *
import server_bot
import app


class CardProduct:
    def __init__(self, categ = None, description = None, price = None, image = None):
        self.categ = categ
        self.description = description
        self.price = price
        self.imageuniq_id = image


    def add_product(self):
        rows_in_table = ['description', 'file_id', 'price', 'uniq_id']
        con = DB_insert()
        uniq_id = app.search_max_uniq_id()
        print(uniq_id)
        arr_value = [self.description, self.price, self.imageuniq_id, str(int(uniq_id[0]) + 1)]
        con.full_string(str(self.categ), rows_in_table, arr_value)
        return 'ok'


async def enter_admin(call_back, cht_id):
    con = DB_update()
    if call_back == 'add_prod':
        update_callback = con.string_with_value('user_data', 'callback_in',  'user_id', str(cht_id), str(call_back))
        await server_bot.bot.send_message(cht_id, 'Выбери категорию в которой будет добавлен товар', reply_markup=admin_sel_cat)
    elif call_back == 'del_prod':
        update_callback = con.string_with_value('user_data', 'callback_in',  'user_id', str(cht_id), str(call_back))
        await server_bot.bot.send_message(cht_id, 'Выбери категорию в которой будет добавлен товар', reply_markup=admin_sel_cat)
    elif call_back == 'red_prod':
        update_callback = con.string_with_value('user_data', 'callback_in',  'user_id', str(cht_id), str(call_back))
        await server_bot.bot.send_message(cht_id, 'Выбери категорию в которой будет добавлен товар', reply_markup=admin_sel_cat)


async def get_data(call_back, cht_id):
    table = call_back[13:]
    print(table)
    con = DB_update()
    con.string_with_value('user_data', 'cache', 'user_id', cht_id, table)
    keyboard = AdminCalback(table).make_callback()
    text = 'Добавь информацию о товаре используя в качестве разделителя ; в формате: Цена;Описание  В конце загрузите изображение товара и нажмите кнопку "Отправить" для добавления всей этой информации в магазин'
    await server_bot.bot.send_message(cht_id, text, reply_markup=keyboard)


async def parse_text(cht_id, message_text):
    elem_mess = message_text.split(';')
    con = DB_select()
    cache = con.string_with_value('cache', 'user_data', 'user_id', cht_id)[0][0]
    card = CardProduct(cache, elem_mess[0], elem_mess[1])
    print('add prod in ' +  card.add_product())
    update_cache = DB_update()
    update_cache.string_with_value('user_data', 'cache', 'user_id', cht_id, 'photo')


async def set_data(call_back, cht_id, forw_id):
    con = DB_select()
    cache = con.string_with_value('cache', 'user_data', 'user_id', cht_id)
    if cache[0][0] == 'added':
        await server_bot.bot.send_message(cht_id, 'Добавлено', reply_markup=main_menu_kb)
    elif cache[0][0] == 'error':
        await server_bot.bot.send_message(cht_id, 'Ошибка при добавлении', reply_markup=main_menu_kb)
    else:
        print('xz')
