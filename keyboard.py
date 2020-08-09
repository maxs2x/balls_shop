from aiogram import Bot, types
from db_hendler import *


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
admin_add_prod = types.InlineKeyboardButton(text='✅  Добавить товар', callback_data='add_prod')
admin_del_prod = types.InlineKeyboardButton(text='✅  Удалить товар', callback_data='del_prod')
admin_red_prod = types.InlineKeyboardButton(text='✅  Редактировать товар', callback_data='red_prod')
admin_select_categ_gel = types.InlineKeyboardButton(text='👍 Гелий', callback_data='admin_select_imggelii')
admin_select_categ_fol = types.InlineKeyboardButton(text='👍 Фольга', callback_data='admin_select_imgfolga')
admin_select_categ_kpz = types.InlineKeyboardButton(text='👍 Композиции', callback_data='admin_select_imgkmpzc')

admin_menu_kb = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=None)
admin_menu_kb.add(admin_add_prod)
admin_menu_kb.add(admin_del_prod, admin_red_prod)

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

admin_sel_cat = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=None)
admin_sel_cat.add(admin_select_categ_fol, admin_select_categ_gel, admin_select_categ_kpz)



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


class AdminCalback:
    def __init__(self, name_table):
        self.name_table = name_table
        self.clbk_dt = 'admin_added'

    def make_callback(self):
        cb = self.clbk_dt + self.name_table
        admin_add_new_product = types.InlineKeyboardButton(text='Добавить', callback_data=cb)
        admin_add_prod = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=None)
        admin_add_prod.add(admin_add_new_product)
        return admin_add_prod




