import aiogram
from time import sleep
import vkAPI

from keyboard import *
import db_hendler
from db_hendler import conn
import server_bot


async def number_of_added(cht_id, file_id):
    vsego = 0

    # Что есть у пользователя
    info_of_user = db_hendler.get_callback_fo_user_id(conn, cht_id)
    in_cart = info_of_user[3]

    if in_cart != None:
        if ' ' in in_cart:
            arr_in_cart = [str(elem) for elem in in_cart.split(' ')]

            for elem in arr_in_cart:
                if file_id == elem:
                    vsego += 1
        elif file_id == in_cart:
            vsego = 1

    return vsego


@server_bot.dp.message_handler(content_types=['text'])
async def send_product_kart(call_back, cht_id, for_id):
    await server_bot.bot.delete_message(cht_id, for_id)
    all_cart = db_hendler.max_id(conn, call_back)
    num_mes1 = int(for_id)
    db_hendler.add_cb_user(conn, cht_id, call_back, num_mes1)
    print('Chat_id produkt cart: ' + str(cht_id))
    for i in range(1, all_cart + 1):
        if i == 1:
            num_mes1 += 1
        else:
            num_mes1 += 2
        num_mes = str(num_mes1)
        descript = db_hendler.get_string_fo_id(conn, call_back, i)[1]
        file_id = db_hendler.get_string_fo_id(conn, call_back, i)[2]
        vsego = await number_of_added(cht_id, file_id)
        await server_bot.bot.send_message(cht_id, descript)
        if i < all_cart:
            product_card_kb = await assemble_keyboard('🛒 ' + str(vsego), None)
        else:
            product_card_kb = await assemble_keyboard('🛒 ' + str(vsego), back_categories)

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
    else:
        try:
            await server_bot.bot.delete_message(str(cht_id), str(for_id))
        except:
            print('Error in nav_back')


async def add_produkt(cht_id, forw_id):
    info_of_user = db_hendler.get_callback_fo_user_id(conn, cht_id)
    old_message_id = info_of_user[2]
    table = info_of_user[1]
    in_cart = info_of_user[3]
    if info_of_user[4] != None:
        price = int(info_of_user[4])
    else:
        price = 0
    id_produkt = (int(forw_id) - int(old_message_id))/2
    all_product_info = db_hendler.get_string_fo_id(conn, table, id_produkt)
    product_file_id = all_product_info[2]
    product_price = all_product_info[3]

    if price == 0 or price == 'Null':
        db_hendler.update_table(conn, 'user_data', 'user_id', 'in_cart', product_file_id, cht_id)
        db_hendler.update_table(conn, 'user_data', 'user_id', 'price', product_price, cht_id)
    elif price > 0:
        new_in_cart = in_cart + ' ' + product_file_id
        new_price = int(price) + int(product_price)
        db_hendler.update_table(conn, 'user_data', 'user_id', 'in_cart', new_in_cart, cht_id)
        db_hendler.update_table(conn, 'user_data', 'user_id', 'price', new_price, cht_id)

    return product_file_id


async def remove_produkt(cht_id, forw_id):
    info_of_user = db_hendler.get_callback_fo_user_id(conn, cht_id)
    old_message_id = info_of_user[2]
    table = info_of_user[1]
    in_cart = info_of_user[3]
    if info_of_user[4] != None:
        price = int(info_of_user[4])
    else:
        price = 0
    id_produkt = (int(forw_id) - int(old_message_id))/2
    all_product_info = db_hendler.get_string_fo_id(conn, table, id_produkt)
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
        db_hendler.update_table(conn, 'user_data', 'user_id', 'in_cart', new_in_cart, cht_id)
        db_hendler.update_table(conn, 'user_data', 'user_id', 'price', new_price, cht_id)

    return  product_file_id


async def in_cart(cht_id):
    all_in_cart = db_hendler.get_callback_fo_user_id(conn, cht_id)[3]
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


async def add_remove(cht_id, forw_id, add_remove, back_categories):
    if add_remove == 'add':
        file_id = await add_produkt(cht_id, forw_id)
    else:
        file_id = await remove_produkt(cht_id, forw_id)
    vsego = await number_of_added(cht_id, file_id)
    new_counter_kb = await assemble_keyboard('🛒 ' + str(vsego), back_categories)
    await server_bot.bot.edit_message_reply_markup(cht_id, forw_id, reply_markup=new_counter_kb)


async def remove_all_cart(cht_id):
    db_hendler.update_table(conn, 'user_data', 'user_id', 'in_cart', None, cht_id)
    db_hendler.update_table(conn, 'user_data', 'user_id', 'price', None, cht_id)



async def format_order(cht_id):
    phone = db_hendler.get_callback_fo_user_id(conn, cht_id)[6]
    all_in_cart = db_hendler.get_callback_fo_user_id(conn, cht_id)[3]
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
    phone = db_hendler.get_callback_fo_user_id(conn, cht_id)[6]
    if (len(phone) < 10) and (len(phone) < 13):
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
    for elem in arr_in_cart:
        for table in db_table:
            info_value = [0, 0]
            info_product = db_hendler.get_string_table_for_elem(conn, table, 'file_id', elem)
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
















