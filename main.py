import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup
from telebot import types
from browser_control import *
from async_sql_scripts import *
from async_markdownv2 import *
from webscraping_funcs import *
from text_scripts import *
from config import *


bot = AsyncTeleBot(telegram_token)


@bot.message_handler(commands=['start', 'menu'])
async def start(message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username

        if not await check_user_exists(user_id):
            try:
                await add_user_to_db(user_id, username)
            except Exception as error:
                print(f"Error adding user to db error:\n{error}")
        else:
            await update_username(user_id, username)

        text = await escape(dictionary['start_msg'], flag=0)
        button_list1 = [
            types.InlineKeyboardButton("📢 About 📢", callback_data="about_section"),
        ]
        button_list2 = [
            types.InlineKeyboardButton("➕ Add Wallet ➕", callback_data="add_wallet_section"),
        ]
        button_list3 = [
            types.InlineKeyboardButton("📊 Trading Coins 📊", callback_data="trading_coins_section"),
        ]
        button_list4 = [
            types.InlineKeyboardButton("📈 My Positions 📈", callback_data="my_positions_section"),
        ]
        button_list5 = [
            types.InlineKeyboardButton("🧾 Trade History 🧾", callback_data="trade_history_section"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])


        await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

        await change_menu_status(user_id, start_menu_status)

    except Exception as e:
        print(f"Error in start message: {e}")


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    user_id = call.message.chat.id

    if call.data == "about_section":
        await bot.answer_callback_query(call.id)

        text = await escape(dictionary["about_msg"], flag=0)
        button_list1 = [
            types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "add_wallet_section":
        await bot.answer_callback_query(call.id)

        text = await escape(dictionary["add_wallet"], flag=0)
        button_list1 = [
            types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

        await change_menu_status(user_id, add_wallet_1)

    elif call.data == "trading_coins_section":
        await bot.answer_callback_query(call.id)

        text = await escape(dictionary["trading_coins_msg"], flag=0)
        button_list0 = [
            types.InlineKeyboardButton("BADDOG / HUAHUA", url="https://coinhall.org/osmosis/osmo1j4grkrsre00j5wkx8h6lappsv7ngjhjt6ucs7kzgcpe8dwwrhvtqpjm8dj"),
        ]
        button_list1 = [
            types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2", disable_web_page_preview=True)

        await change_menu_status(user_id, add_wallet_1)

    elif call.data == "my_positions_section":
        await bot.answer_callback_query(call.id)

        try:
            traders_info = await get_info_tracking_info_huahua(user_id)

            wallet = traders_info[1]
            bought = int(traders_info[2])
            sold = int(traders_info[3])
            bought_volume_dollar = float(traders_info[4])
            sold_volume_dollar = float(traders_info[5])
            bought_value = float(traders_info[6])
            sold_value = float(traders_info[7])
            avg_buy_price = float(traders_info[8])
            avg_sell_price = float(traders_info[9])
            token = "BADDOG / HUAHUA"
            current_market_price = float(await get_tokens_price(token))

            remaining_tokens = bought_value - sold_value

            if remaining_tokens > 0:
                current_value_of_remaining_tokens = remaining_tokens * current_market_price

                pnl = round(current_value_of_remaining_tokens - (remaining_tokens * avg_buy_price), 2)
                formatted_number = "{:.13f}".format(avg_buy_price)
                formatted_current_price = "{:.13f}".format(current_market_price)
                text = await escape(dictionary["my_positions_section_huahua"].format(wallet, token, remaining_tokens, formatted_number, formatted_current_price, pnl), flag=0)
                button_list0 = [
                    types.InlineKeyboardButton("🟢 BUY", url="https://coinhall.org/osmosis/osmo1j4grkrsre00j5wkx8h6lappsv7ngjhjt6ucs7kzgcpe8dwwrhvtqpjm8dj"),
                    types.InlineKeyboardButton("🔴 SELL", url="https://coinhall.org/osmosis/osmo1j4grkrsre00j5wkx8h6lappsv7ngjhjt6ucs7kzgcpe8dwwrhvtqpjm8dj"),
                ]
                button_list1 = [
                    types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
                ]
                reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["no_open_positions_huahua"], flag=0)
                button_list1 = [
                    types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
                ]
                reply_markup = types.InlineKeyboardMarkup([button_list1])
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
        except:
            text = await escape(dictionary["no_open_positions_huahua"], flag=0)
            button_list1 = [
                types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
    elif call.data == "trade_history_section":
        await bot.answer_callback_query(call.id)

        try:
            traders_info = await get_info_tracking_info_huahua(user_id)

            wallet = traders_info[1]
            bought = int(traders_info[2])
            sold = int(traders_info[3])
            bought_volume_dollar = float(traders_info[4])
            sold_volume_dollar = float(traders_info[5])
            bought_value = float(traders_info[6])
            sold_value = float(traders_info[7])
            avg_buy_price = float(traders_info[8])
            avg_sell_price = float(traders_info[9])
            token = "BADDOG / HUAHUA"
            current_market_price = float(await get_tokens_price(token))

            # total_buy_cost = bought_value * avg_buy_price
            total_sell_revenue = sold_value * avg_sell_price
            pnl = round(total_sell_revenue , 2)

            formatted_number = "{:.13f}".format(avg_sell_price)
            formatted_current_price = "{:.13f}".format(current_market_price)
            text = await escape(dictionary["my_history_trade"].format(wallet, token, sold_value, formatted_number, formatted_current_price, pnl), flag=0)
            button_list0 = [
                types.InlineKeyboardButton("🟢 BUY", url="https://coinhall.org/osmosis/osmo1j4grkrsre00j5wkx8h6lappsv7ngjhjt6ucs7kzgcpe8dwwrhvtqpjm8dj"),
                types.InlineKeyboardButton("🔴 SELL", url="https://coinhall.org/osmosis/osmo1j4grkrsre00j5wkx8h6lappsv7ngjhjt6ucs7kzgcpe8dwwrhvtqpjm8dj"),
            ]
            button_list1 = [
                types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
        except:
            text = await escape(dictionary["no_history_trades_huahua"], flag=0)
            button_list1 = [
                types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
    elif call.data == "back_to_main_menu":
        await bot.answer_callback_query(call.id)

        text = await escape(dictionary['start_msg'], flag=0)
        button_list1 = [
            types.InlineKeyboardButton("📢 About 📢", callback_data="about_section"),
        ]
        button_list2 = [
            types.InlineKeyboardButton("➕ Add Wallet ➕", callback_data="add_wallet_section"),
        ]
        button_list3 = [
            types.InlineKeyboardButton("📊 Trading Coins 📊", callback_data="trading_coins_section"),
        ]
        button_list4 = [
            types.InlineKeyboardButton("📈 My Positions 📈", callback_data="my_positions_section"),
        ]
        button_list5 = [
            types.InlineKeyboardButton("🧾 Trade History 🧾", callback_data="trade_history_section"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

        await change_menu_status(user_id, start_menu_status)


@bot.message_handler(func=lambda message: True, content_types=['text'])
async def handle_text(message):
    user_id = message.chat.id
    user_status = await get_user_menu_status(user_id)

    if user_status == add_wallet_1:
        wallet_address = message.text

        if not await check_added_wallet_by_user_id(user_id):
            try:
                await add_new_tracking_wallet_huahua(user_id, wallet_address)
                text = await escape(dictionary['wallet_added'], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                await change_menu_status(user_id, start_menu_status)
            except:
                text = await escape(dictionary["wallet_already_added"], flag=0)
                button_list1 = [
                    types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
                ]
                reply_markup = types.InlineKeyboardMarkup([button_list1])
                await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup,parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["you_already_added_wallet"], flag=0)
            button_list1 = [
                types.InlineKeyboardButton("Back", callback_data="back_to_main_menu"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1])
            await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")


async def update_info_in_database(traders_wallet_address):
    try:
        scanned_html = await coinhall_scrap(traders_wallet_address)
        bought_info, sold_info, price_of_huahua = await parse_coinhall_traders(scanned_html)

        bought, bought_volume, bought_value, avg_buy_price = int(bought_info[0][0]), str(bought_info[0][1]), str(bought_info[0][2]), str(bought_info[0][3])
        sold, sold_volume, sold_value, avg_sell_price = int(sold_info[0][0]), str(sold_info[0][1]), str(sold_info[0][2]), str(sold_info[0][3])

        await update_coins_price(price_of_huahua, "BADDOG / HUAHUA")
        await update_traders_info_huahua(traders_wallet_address, bought, bought_volume, bought_value, sold, sold_volume, sold_value, avg_buy_price, avg_sell_price)
    except Exception as error:
        print(error)


async def check_huahua_wallets_traders_info():
    try:
        while True:
            get_list_of_wallets = await full_wallet_lists_of_huahua()
            for traders_wallet_address in get_list_of_wallets:
                await update_info_in_database(traders_wallet_address)
                await change_wallet_updated_status_huahua(traders_wallet_address)
            await change_all_wallets_updated_status_huahua()
            await asyncio.sleep(15)
    except Exception as error:
        print(error)


async def run_services():
    try:
        bot_task = asyncio.create_task(bot.polling(non_stop=True, request_timeout=500))
        huahua_traders_scanner = asyncio.create_task(check_huahua_wallets_traders_info())
        await asyncio.gather(bot_task, huahua_traders_scanner)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_services())
    loop.run_forever()
