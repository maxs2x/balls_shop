from aiogram import Bot, types


back_start = types.InlineKeyboardButton(text='⬅ Назад', callback_data='back_start')
back_categories = types.InlineKeyboardButton(text='⬅ Назад', callback_data='back_categories')
cart = types.InlineKeyboardButton(text='🛒  Корзина ', callback_data='cart')
about = types.InlineKeyboardButton(text='📞  О нас', callback_data='about')
categories = types.InlineKeyboardButton(text='🎈  Ассортимент  🎈', callback_data='categories')
bt1 = types.InlineKeyboardButton(text='Фольгированые', callback_data='imgfolga')
bt2 = types.InlineKeyboardButton(text='Гелиевые', callback_data='imggelii')
bt3 = types.InlineKeyboardButton(text='Готовые композиции', callback_data='imgkmpzc')
send_cart = types.InlineKeyboardButton(text='✅  Отправить заказ  ✅', callback_data='by_order')
remove_cart = types.InlineKeyboardButton(text='⛔ Очистить корзину ⛔', callback_data='remove_cart')
create_order = types.KeyboardButton(text='✅  Подтвердить  ✅')

main_menu_kb = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=None)
main_menu_kb.add(categories)
main_menu_kb.add(about, cart)

categories_kb = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=None)
categories_kb.add(bt1)
categories_kb.add(bt2)
categories_kb.add(bt3)
categories_kb.add(back_start)

send_cart_kb = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=None)
send_cart_kb.add(send_cart)
send_cart_kb.add(back_start, remove_cart)

back_categories_kb = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=None)
back_categories_kb.add(back_start)

okey_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
okey_kb.add(create_order)

# Собираем клавиатуру для карточки товара
async def assemble_keyboard(vsego, back_categories):
    pl = types.InlineKeyboardButton(text='👍 Добавить', callback_data='add')
    mn = types.InlineKeyboardButton(text='👎 Убрать', callback_data='remove')
    pl_end = types.InlineKeyboardButton(text='👍 Добавить', callback_data='add_end')
    mn_end = types.InlineKeyboardButton(text='👎 Убрать', callback_data='remove_end')
    c_c = types.InlineKeyboardButton(text=str(vsego), callback_data='no')
    product_card_kb = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=None)
    if back_categories == None:
        product_card_kb.add(pl, c_c, mn)
    else:
        product_card_kb.add(pl_end, c_c, mn_end)
        product_card_kb.add(back_categories, cart)
    return product_card_kb




