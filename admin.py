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
        rows_in_table = ['description', 'price', 'file_id', 'uniq_id']
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
        await server_bot.bot.send_message(cht_id, 'Выбери категорию из которой будет удалён товар', reply_markup=admin_sel_cat)
    elif call_back == 'red_prod':
        update_callback = con.string_with_value('user_data', 'callback_in',  'user_id', str(cht_id), str(call_back))
        await server_bot.bot.send_message(cht_id, 'Выбери категорию в которой будет отредактирован товар', reply_markup=admin_sel_cat)


async def parse_text(cht_id, message_text):
    elem_mess = message_text.split(';')
    print(elem_mess)
    con = DB_select()
    cache = con.string_with_value('cache', 'user_data', 'user_id', cht_id)[0][0]
    card = CardProduct(cache, description=elem_mess[1], price=elem_mess[0])
    print('add prod in ' +  card.add_product())
    update_cache = DB_update()
    update_cache.string_with_value('user_data', 'cache', 'user_id', cht_id, 'photo')


async def set_data(call_back, cht_id, forw_id):
    con = DB_select()
    cache = con.string_with_value('cache', 'user_data', 'user_id', cht_id)
    if cache[0][0] == 'added':
        await server_bot.bot.send_message(cht_id, 'Добавлено', reply_markup=admin_menu_kb)
    elif cache[0][0] == 'error':
        await server_bot.bot.send_message(cht_id, 'Ошибка при добавлении', reply_markup=admin_menu_kb)
    else:
        print('xz')

async def del_data(call_back, cht_id):
    table = call_back[-8:]
    db_sell = db_hendler.DB_select()
    all_card = db_sell.max_value('id', table)
    if all_card == None:
        await server_bot.bot.send_message(cht_id, 'В этой категории нет товара', reply_markup=admin_sel_cat)
        return False
    for i in range(1, int(all_card) + 1):
        data_product = db_sell.string_with_value('*', table, 'id', str(i))
        text = data_product[0][1]
#        price = data_product[0][3]
        file_id = data_product[0][2]
        print(file_id)
        await server_bot.bot.send_message(cht_id, text)
        if i == int(all_card + 1):
            number_card = await c_b_card_del(i, table, 'no_end')
            await server_bot.bot.send_photo(cht_id,
                                            file_id,
                                            reply_markup=number_card)
            sleep(0.1)
        else:
            number_card = await c_b_card_del(i, table, 'end')
            await server_bot.bot.send_photo(cht_id,
                                            file_id,
                                            reply_markup=number_card)


async def add_prod(call_back, cht_id):
    table = call_back[13:]
    print(table)
    con = DB_update()
    con.string_with_value('user_data', 'cache', 'user_id', cht_id, table)
    keyboard = AdminCalback(table).make_callback()
    text = 'Добавь информацию о товаре используя в качестве разделителя ; в формате: Цена;Описание  В конце загрузите изображение товара и нажмите кнопку "Отправить" для добавления всей этой информации в магазин'
    await server_bot.bot.send_message(cht_id, text, reply_markup=keyboard)


async def get_data(call_back, cht_id):
    db_sell = db_hendler.DB_select()
    admin_do = db_sell.string_with_value('callback_in', 'user_data', 'user_id', cht_id)
    if admin_do[0][0] == 'add_prod':
        await add_prod(call_back, cht_id)
    elif admin_do[0][0] == 'del_prod':
        await del_data(call_back, cht_id)
    elif admin_do[0][0] == 'red_prod':
        print('red')
    print('get_data' + admin_do[0][0])


async def delet_card(call_back, cht_id, fwd_id):
    arr_callback = call_back.split('_')
    print('delet_card')
    print(arr_callback)
    delet_obj = db_hendler.DB_delet()
    delet_obj.dell_string(arr_callback[3], 'id', arr_callback[2])
    await server_bot.bot.delete_message(cht_id, fwd_id)
    await server_bot.bot.delete_message(cht_id, str(int(fwd_id) - 1))
    return 'ok'