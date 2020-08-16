import aiogram
from time import sleep
import vkAPI

from keyboard import *
import db_hendler
import server_bot
import admin

# Секция с функциями для запросов к БД
def get_callback_fo_user_id(user_id):
    get_callback_fo_user = db_hendler.DB_select()
    callback_user = get_callback_fo_user.string_with_value('*', 'user_data', 'user_id', user_id)
    print('get_callback_fo_user_id')
    print(callback_user[0])
    return callback_user[0]


def get_string_fo_id(name_table, id):
    db_obj = db_hendler.DB_select()
    it_be = db_obj.string_with_value('price', name_table, 'id', str(id))
    if len(it_be) == 0:
        new_id = int(id) + 1
        return get_string_fo_id(name_table, new_id)
    row = db_obj.string_with_value('*', str(name_table), 'id', str(id))
    ret_info = [row[0], id]
    print('get_string_fo_id')
    print(ret_info)
    return ret_info


async def add_user(user_id):
    db_obj = db_hendler.DB_select()
    info_user = db_obj.string_with_value('*', 'user_data', 'user_id', user_id)
    arr_user_id = [user_id]
    if len(info_user) == 0:
        print(arr_user_id)
        in_obj = db_hendler.DB_insert()
        in_obj.full_string('user_data', ['user_id'], arr_user_id)


# Функции бота
async def number_of_added(cht_id, file_id):
    vsego = 0
    # Что есть у пользователя
    info_of_user = get_callback_fo_user_id(cht_id)
    in_cart = info_of_user[3]

    if in_cart != None:
        if ' ' in in_cart:
            arr_in_cart = [str(elem) for elem in in_cart.split(' ')]
            for elem in arr_in_cart:
                if file_id == elem:
                    vsego += 1
        elif file_id == in_cart:
            vsego = 1
    print('number_of_added ' + str(vsego))
    return vsego


@server_bot.dp.message_handler(content_types=['text'])
async def send_product_kart(call_back, cht_id, for_id):
    await server_bot.bot.delete_message(cht_id, for_id)
    get_card = db_hendler.DB_select()
    count_cart = get_card.count_string('id', str(call_back))[0][0]
    print(count_cart)
    num_mes1 = int(for_id)
    db_obj = db_hendler.DB_update()
    db_obj.string_with_value('user_data', 'callback_in', 'user_id', cht_id, call_back)
    db_obj.string_with_value('user_data', 'message_id', 'user_id', cht_id, str(num_mes1))

    print('Chat_id produkt cart: ' + str(cht_id))
    start_index = 1
    for i in range(1, int(count_cart) + 1):
        if i == 1:
            num_mes1 += 1
        else:
            num_mes1 += 2
        num_mes = str(num_mes1)
        info_about_prod = get_string_fo_id(call_back, start_index)
        if start_index != int(info_about_prod[1]):
            start_index = int(info_about_prod[1])
        start_index += 1
        descript = info_about_prod[0]
        file_id = info_about_prod[0][2]
        vsego = await number_of_added(cht_id, file_id)
        text = str(descript[1]) + '\n Цена ' + str(descript[3])
        await server_bot.bot.send_message(cht_id, text)
        if i < int(count_cart):
            product_card_kb = await assemble_keyboard('🛒 ' + str(vsego), None, descript[4])
        else:
            product_card_kb = await assemble_keyboard('🛒 ' + str(vsego), back_categories, descript[4])

        await server_bot.bot.send_photo(cht_id,
                                        file_id,
                                        reply_markup=product_card_kb,
                                        reply_to_message_id=num_mes)
        await server_bot.bot.delete_message(cht_id, num_mes)
        sleep(0.1)




async def nav_back(cht_id, for_id, many):
    err = 0

    print('for_id = ' + str(for_id))
    if many == 'yes':
        for i in range(0, 60, 2):
            num_mes = int(for_id) - i
            try:
                await server_bot.bot.delete_message(str(cht_id), str(num_mes))
            except:
                print('error NO deleted ' + str(num_mes))
                err += 1
                break
    elif many == 'yes_every':
        for i in range(0, 60):
            num_mes = int(for_id) - i
            try:
                await server_bot.bot.delete_message(str(cht_id), str(num_mes))
            except:
                print('error NO deleted ' + str(num_mes))
                err += 1
                break
    elif many == 'two':
        try:
            await server_bot.bot.delete_message(str(cht_id), str(for_id))
            bac_mes = int(for_id) - 1
            await server_bot.bot.delete_message(str(cht_id), str(bac_mes))
        except:
            print('two Error in nav_back')
    elif many == 'thre':
        try:
            for i in range(3):
                bac_mes = int(for_id) - i
                await server_bot.bot.delete_message(str(cht_id), str(bac_mes))
        except:
            print('tree Error in nav_back')
    elif many == 'one_one':
        try:
            await server_bot.bot.delete_message(str(cht_id), str(for_id - 1))
            await server_bot.bot.delete_message(str(cht_id), str(for_id))
        except:
            print('one_one Error in nav_back')
    elif many == 'four':
        try:
            for i in range(0, 4):
                bac_mes = int(for_id) - i
                await server_bot.bot.delete_message(str(cht_id), str(bac_mes))
        except:
            print('one_one Error in nav_back')
    else:
        try:
            await server_bot.bot.delete_message(str(cht_id), str(for_id))
        except:
            print('Error in nav_back')


async def add_produkt(cht_id, forw_id, uniq_id):
    info_of_user = get_callback_fo_user_id(cht_id)
    table = info_of_user[1]
    in_cart = info_of_user[3]
    if info_of_user[4] != None:
        price = int(info_of_user[4])
    else:
        price = 0
    db_select = db_hendler.DB_select()
    all_product_info = db_select.string_with_value('*', table, 'uniq_id', str(uniq_id))[0]
    product_file_id = all_product_info[2]
    product_price = all_product_info[3]
    db_obj = db_hendler.DB_update()
    if price == 0 or price == 'Null':
        db_obj.string_with_value('user_data', 'in_cart', 'user_id', cht_id, product_file_id)
        db_obj.string_with_value('user_data', 'price', 'user_id', cht_id, product_price)
    elif price > 0:
        new_in_cart = in_cart + ' ' + product_file_id
        new_price = int(price) + int(product_price)
        db_obj.string_with_value('user_data', 'in_cart', 'user_id', cht_id, new_in_cart)
        db_obj.string_with_value('user_data', 'price', 'user_id', cht_id, new_price)
    print('add_product')
    print(product_file_id)
    return product_file_id


async def remove_produkt(cht_id, forw_id, uniq_id):
    info_of_user = get_callback_fo_user_id(cht_id)
    table = info_of_user[1]
    in_cart = info_of_user[3]
    if info_of_user[4] != None:
        price = int(info_of_user[4])
    else:
        price = 0
    db_select = db_hendler.DB_select()
    all_product_info = db_select.string_with_value('*', table, 'uniq_id', str(uniq_id))[0]
    product_file_id = all_product_info[2]
    product_price = all_product_info[3]

    if price == 0 or price == 'Null':
        print('0 - 0')
    elif price > 0:
        arr_in_cart = [str(s) for s in in_cart.split(' ')]
        if len(arr_in_cart) > 1:
            arr_in_cart.remove(product_file_id)
            new_in_cart = ' '.join(elem for elem in arr_in_cart)
            new_price = int(price) - int(product_price)
        else:
            new_in_cart = None
            new_price = None
        db_obj = db_hendler.DB_update()
        db_obj.string_with_value('user_data', 'in_cart', 'user_id', cht_id, new_in_cart)
        db_obj.string_with_value('user_data', 'price', 'user_id', cht_id, new_price)
    return  product_file_id


async def in_cart(cht_id):
    all_in_cart = get_callback_fo_user_id(cht_id)[3]
    if all_in_cart != None:
        if ' ' in all_in_cart:
            arr_in_cart = [str(elem) for elem in all_in_cart.split(' ')]
        else:
            arr_in_cart = []
            arr_in_cart.append(all_in_cart)
    else:
        await server_bot.bot.send_message(cht_id, "Ваша корзиа пуста", reply_markup=back_categories_kb)
        return

    ret_in = await whots_in_cart(cht_id, arr_in_cart)
    string_output = ret_in[0]
    all_price = ret_in[1]

    string_output += '\n Общфя стоимость ' + str(all_price)
    await server_bot.bot.send_message(cht_id, string_output, 'html', reply_markup=send_cart_kb)


async def order_by(cht_id, phone=None):
    if phone == None:
        phon_numb = get_callback_fo_user_id(cht_id)[6]
        print(phone)
    else:
        phon_numb = 'redact'

    if phon_numb == phone:
        await server_bot.bot.send_message(cht_id,
                               'Для уточнения деталей заказа отправьте сообщение с Вашим номер телефона в формате 89ХХ ХХХ ХХХХ или +79ХХ ХХХ ХХХХ  нажмите кнопку ПОДТВЕРДИТЬ',
                               reply_markup=okey_kb)
        await server_bot.bot.send_message(cht_id, 'Далее нажмите кнопку ПОДТВЕРДИТЬ', reply_markup=back_categories_kb)
    else:
        text = 'Ранее Вы делали у нас заказ и оставляли номер ' + str(phon_numb) + '. Использовать этот номер снова?'
        await  server_bot.bot.send_message(cht_id, text, reply_markup=it_phone_kb)


async def add_remove(cht_id, forw_id, callback, back_categories):
    if callback[:3] == 'add':
        uniq_id = callback[8:]
        file_id = await add_produkt(cht_id, forw_id, uniq_id)
    else:
        uniq_id = callback[11:]
        file_id = await remove_produkt(cht_id, forw_id, uniq_id)
    vsego = await number_of_added(cht_id, file_id)
    new_counter_kb = await assemble_keyboard('🛒 ' + str(vsego), back_categories, str(uniq_id))
    await server_bot.bot.edit_message_reply_markup(cht_id, forw_id, reply_markup=new_counter_kb)


async def remove_all_cart(cht_id):
    db_obj = db_hendler.DB_update()
    db_obj.string_with_value('user_data', 'price', 'user_id', cht_id, None)
    db_obj.string_with_value('user_data', 'in_cart', 'user_id', cht_id, None)


async def format_order(cht_id):
    phone = get_callback_fo_user_id(cht_id)[6]
    all_in_cart = get_callback_fo_user_id(cht_id)[3]
    if ' ' in all_in_cart:
        arr_in_cart = [str(elem) for elem in all_in_cart.split(' ')]
    else:
        arr_in_cart = []
        arr_in_cart.append(all_in_cart)
    ret_in = await whots_in_cart(cht_id, arr_in_cart)
    string_output = ret_in[0]
    all_price = ret_in[1]
    text = ret_in[0] + ' ИТОГО ' + str(ret_in[1]) + '\n Телефон ' + str(phone)
    vkAPI.send_order(text)


async def verifi_phone(cht_id, forw_id):
    a = 0
    phone = get_callback_fo_user_id(cht_id)[6]
    print(phone)
    if (len(phone) <= 10) and (len(phone) < 13):
        await nav_back(cht_id, forw_id, 'thre')
        await server_bot.bot.send_message(cht_id, 'В номере должно быть 11 цифр', reply_markup=okey_kb)
    elif 11 <= len(phone):
        if len(phone) >= 12:
            phone = phone[3:]
        for i in phone:
            try:
                a += 1
                i = int(i)
            except ValueError:
                await nav_back(cht_id, forw_id, 'thre')
                await server_bot.bot.send_message(cht_id, 'В номере должны быть только цифры', reply_markup=okey_kb)
                break

    if a > 9:
        return 'done'
    else:
        return 'fail'


async def whots_in_cart(cht_id, arr_in_cart):
    all_price = 0
    dict_values = {}
    string_output = str()

    db_table = ['imgfolga', 'imggelii', 'imgkmpzc']
    db_obj = db_hendler.DB_select()
    for elem in arr_in_cart:
        for table in db_table:
            info_value = [0, 0]
            info_product = db_obj.string_with_value('*', table, 'file_id', elem)
            if len(info_product) > 0:
                name_product = info_product[0][1]
                price_product = info_product[0][3]
                info_value[0], info_value[1] = price_product, 1
                if name_product in dict_values:
                    dict_values[name_product][1] += 1
                else:
                    dict_values[name_product] = info_value
                all_price += int(price_product)

    string_output = ''
    i = 1
    for x, y in dict_values.items():
        sum = int(y[0]) * int(y[1])
        string_output +=  str(i) + '. <b>' + str(x) + '</b> \n' + str(y[0]) + ' x ' + str(y[1]) + ' = ' + str(sum) + '\n'
        i += 1

    ret = [string_output, all_price]
    return ret

def search_max_uniq_id():
    name_table = ['imgfolga', 'imggelii', 'imgkmpzc']
    uniq_id = [0, 'imgfolga']
    max_id_req = DB_select()
    for elem in name_table:
        uniq_id_req = max_id_req.max_value('uniq_id', elem)
        print(uniq_id_req)
        if uniq_id_req != None:
            if uniq_id[0] < int(uniq_id_req):
                uniq_id = [int(uniq_id_req), elem]
    print('max uniq_id = ' + str(uniq_id))
    return uniq_id

















