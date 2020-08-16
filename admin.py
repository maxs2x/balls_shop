import aiogram
from time import sleep

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


class ValidationInput:
    @staticmethod
    def photo(file_id):
        if len(file_id) == 99:
            if 'A' in file_id:
                int = any(map(str.isdigit, file_id))
                if int == True:
                    return True


    @staticmethod
    def price(price):
        int = any(map(str.isdigit, price))
        if int == True:
            return True


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


class AdminAddProdukt:
    @staticmethod
    async def enter_product(cht_id, callback, fwd = None):
        print('enter_product ' + callback)
        text_stap_1 = 'Шаг 1. Отправьте сообщение с описанием товара и нажмите "Готово"'
        text_stap_1_err = 'Пустое сообщение. Отправьте сообщение с описанием товара и нажмите "Готово"'
        text_stap_2 = 'Шаг 2. Отправьте сообщение с ценой товара и нажмите "Готово"'
        text_stap_2_err = 'Пустое сообщение. Отправьте сообщение с ценой товара и нажмите "Готово"'
        text_stap_3 = 'Шаг 3. Отправьте фото товара и нажмите "Готово"'
        db_up = db_hendler.DB_update()
        if callback[:12] == 'admin_select':
            db_up.string_with_value('user_data', 'cache', 'user_id', cht_id, None)
            enter_product_kb = await RedactCartKB.enter_product_kb(callback[13:] + '_1')
            await server_bot.bot.send_message(cht_id, text_stap_1, reply_markup=enter_product_kb)
        elif callback[-1] == '2':
            try:
                db_up.string_with_value('user_data', 'callback_in', 'user_id', cht_id, callback)
                enter_product_kb = await RedactCartKB.enter_product_kb(callback)
                await server_bot.bot.delete_message(cht_id, int(fwd) + 1)
                await server_bot.bot.send_message(cht_id, text_stap_2, reply_markup=enter_product_kb)
            except:
                callback = callback[-10:-2] + '_1'
                enter_product_kb = await RedactCartKB.enter_product_kb(callback)
                await server_bot.bot.send_message(cht_id, text_stap_1_err, reply_markup=enter_product_kb)
        elif callback[-1] == '3':
            try:
                db_up.string_with_value('user_data', 'callback_in', 'user_id', cht_id, callback)
                await server_bot.bot.delete_message(cht_id, int(fwd) + 1)
                enter_product_kb = await RedactCartKB.enter_product_kb(callback)
                await server_bot.bot.send_message(cht_id, text_stap_3, reply_markup=enter_product_kb)
            except:
                callback = callback[:-1] + '2'
                enter_product_kb = await RedactCartKB.enter_product_kb(callback)
                await server_bot.bot.send_message(cht_id, text_stap_2_err, reply_markup=enter_product_kb)
        print('enter_product ' + callback)


    @staticmethod
    async def set_product(cht_id, callback, fwd):
        try:
            #await server_bot.bot.delete_message(cht_id, int(fwd) + 1)
            db_sel = db_hendler.DB_select()
            cache = db_sel.string_with_value('cache', 'user_data', 'user_id', cht_id)[0][0]
            arr_cache = cache.split(';')
            print(callback, arr_cache)
            build_card = CardProduct(categ=callback[12:-2], description=arr_cache[0], price=arr_cache[1], image=arr_cache[2])
            if build_card.add_product() == 'ok':
                await server_bot.bot.send_message(cht_id, 'Новая карточка успешно создана', reply_markup=admin_menu_kb)
        except:
            print('set_product ' + callback)
            callback = callback[:-1] + '3'
            enter_product_kb = await RedactCartKB.enter_product_kb(callback)
            await server_bot.bot.send_message(cht_id, 'ОШИБКА (фото не отправлено). Карточка не создана', reply_markup=enter_product_kb)


async def get_data(call_back, cht_id, fowd):
    db_sell = db_hendler.DB_select()
    admin_do = db_sell.string_with_value('callback_in', 'user_data', 'user_id', cht_id)
    if admin_do[0][0] == 'add_prod':
        await AdminAddProdukt.enter_product(cht_id, call_back)
    elif admin_do[0][0] == 'del_prod':
        await ProductCard.send_list_card(cht_id, call_back, fowd, 'del_prod')
    elif admin_do[0][0] == 'red_prod':
        await ProductCard.send_list_card(cht_id, call_back, fowd, 'red_prod')
    print('get_data ' + admin_do[0][0])


async def delet_card(call_back, cht_id, fwd_id):
    arr_callback = call_back.split('_')
    print('delet_card')
    print(arr_callback)
    delet_obj = db_hendler.DB_delet()
    delet_obj.dell_string(arr_callback[3], 'id', arr_callback[2])
    await server_bot.bot.delete_message(cht_id, fwd_id)
    if len(arr_callback) > 4:
        await server_bot.bot.edit_message_text('Карточка удалена', cht_id, int(fwd_id) - 1, reply_markup=admin_start_kb)
    else:
        await server_bot.bot.edit_message_text('Карточка удалена', cht_id, int(fwd_id) - 1)
    return 'ok'


class ProductCard():
    @staticmethod
    async def send_list_card(cht_id, callback, fowd, method):
        print('AddCardForRedact.send_card')
        table = callback[-8:]
        db_sel = db_hendler.DB_select()
        count_card = db_sel.count_string('id', table)
        real_id_card = 1
        print(count_card)
        if count_card[0][0] == 0:
            await server_bot.bot.send_message(cht_id, 'В этой категории нет товара', reply_markup=admin_sel_cat)
            return False
        for i in range(1, int(count_card[0][0]) + 1):
            get_card = app.get_string_fo_id(table, real_id_card)
            real_id_card = get_card[1]
            data_card = get_card[0]
            text_card = str(data_card[1]) + '" Цена "' + str(data_card[3]) + '"'
            if method == 'red_prod':
                text_card = 'Описание карточки "' + str(data_card[1]) + '" Цена товара "' + str(data_card[3]) + '"'
            if i == int(count_card[0][0]):
                if method == 'red_prod':
                    redact_kard_kb = await RedactCartKB.choose_card_kb(real_id_card, table, do=None, end='yes')
                else:
                    redact_kard_kb = await c_b_card_del(real_id_card, table, 'end')
                num_mes = int(fowd) + i * 2
                db_upd = db_hendler.DB_update()
                db_upd.string_with_value('user_data', 'message_id', 'user_id', cht_id, num_mes)
            else:
                if method == 'red_prod':
                    redact_kard_kb = await RedactCartKB.choose_card_kb(real_id_card, table)
                else:
                    redact_kard_kb = await c_b_card_del(real_id_card, table, 'no_end')
            await server_bot.bot.send_message(cht_id, text_card)
            await server_bot.bot.send_photo(cht_id, data_card[2], reply_markup=redact_kard_kb)
            real_id_card += 1

class AdminCardForRedact:
    @staticmethod
    async def redact_card(cht_id, callback):
        table = callback[7:15]
        id_card = callback[16:]
        db_obj = db_hendler.DB_select()

        count_card = db_obj.count_string('id', table)[0][0]
        message_id = int(db_obj.string_with_value('message_id', 'user_data', 'user_id', cht_id)[0][0])
        for i in range(0, int(count_card) * 2 ):
            try:
                await  server_bot.bot.delete_message(cht_id, message_id)
            except:
                message_id -= 0
            message_id -= 1
            print(message_id)
            sleep(0.1)

        data_card = db_obj.string_with_value('*', table, 'id', id_card)[0]
        redact_card_kb = await RedactCartKB.made_kb(id_card, table)
        text = 'Описание карточки "' + str(data_card[1]) + '" Цена товара "' + str(data_card[3]) + '"'
        await server_bot.bot.send_message(cht_id, text)
        await server_bot.bot.send_photo(cht_id, data_card[2], reply_markup=redact_card_kb)


    @staticmethod
    async def modify_card(cht_id, callback, forw_id):
        table = callback[7:15]
        do = callback[-1]
        callback = callback[:-2]
        id_card = callback[16:]
        await app.nav_back(cht_id, forw_id, 'one_one')
        print('modify_card ' + table + ' ' + id_card + ' ' + do)
        do_redact_kb = await RedactCartKB.choose_card_kb(id_card, table, do)
        if do == '1':
            await server_bot.bot.send_message(cht_id, 'Введите новое описание и нажмите применить', reply_markup=do_redact_kb)
        elif do == '2':
            await server_bot.bot.send_message(cht_id, 'Введите новую цену и нажмите применить', reply_markup=do_redact_kb)
        elif do == '3':
            update_cache = db_hendler.DB_update()
            update_cache.string_with_value('user_data', 'cache', 'user_id', cht_id, 'photo')
            await server_bot.bot.send_message(cht_id, 'Отправьте новую фотографию и нажмите применить', reply_markup=do_redact_kb)



    @staticmethod
    async def do_redact(cht_id, callback, fwd):
        do = callback[-1]
        callback = callback[:-2]
        table = callback[9:17]
        id_card = callback[18:]
        try:
            await server_bot.bot.delete_message(cht_id, int(fwd) + 1)
            callback = callback[:-2]
            db_obj = db_hendler.DB_select()
            update_table = db_hendler.DB_update()
            set_value = db_obj.string_with_value('cache', 'user_data', 'user_id', cht_id)[0][0]
            if do == '1':
                mad_row = 'description'
                update_table.string_with_value(table, mad_row, 'id', id_card, set_value)
            elif do == '2':
                mad_row = 'price'
                update_table.string_with_value(table, mad_row, 'id', id_card, set_value)
            else:
                mad_row = 'file_id'
                valid = ValidationInput.photo(set_value)
                if valid == True:
                    update_table.string_with_value(table, mad_row, 'id', id_card, set_value)
                else:
                    do_redact_kb = await RedactCartKB.choose_card_kb(id_card, table, do)
                    await server_bot.bot.send_message(cht_id, 'ОШИБКА! Отправленные данные не являются изображением! Повторите попытку',
                                                      reply_markup=do_redact_kb)
                    return 'false'
            return 'ok'
        except:
            do_redact_kb = await RedactCartKB.choose_card_kb(id_card, table, do)
            await server_bot.bot.send_message(cht_id, 'ОШИБКА! Пустой ввод! Повторите попытку', reply_markup=do_redact_kb)