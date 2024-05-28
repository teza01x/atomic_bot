import aiosqlite
import asyncio
from config import *


async def check_user_exists(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT user_id FROM user WHERE user_id = ?", (user_id,))
            user = await result.fetchall()
        return bool(len(user))


async def add_user_to_db(user_id, username):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO user (user_id, username, menu_status) VALUES(?, ?, ?)",
                (user_id, username, 0))
            await conn.commit()


async def update_username(user_id, username):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE user SET username = ? WHERE user_id = ?", (username, user_id,))
            await conn.commit()


async def change_menu_status(user_id, status):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE user SET menu_status = ? WHERE user_id = ?", (status, user_id,))
            await conn.commit()


async def get_user_menu_status(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT menu_status FROM user WHERE user_id = ?", (user_id,))
            user_status = await result.fetchone()
            return user_status[0]


async def update_traders_info_huahua(traders_wallet_address, bought, bought_volume, bought_value, sold, sold_volume, sold_value, avg_buy_price, avg_sell_price):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE traders_data_huahua SET bought = ?, sold = ?, bought_volume = ?, sold_volume = ?, bought_value = ?, sold_value = ?, avg_buy_price = ?, avg_sell_price = ? WHERE wallet = ?", (bought, sold, bought_volume, sold_volume, bought_value, sold_value, avg_buy_price, avg_sell_price, traders_wallet_address,))
            await conn.commit()


async def full_wallet_lists_of_huahua():
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT wallet FROM traders_data_huahua WHERE updated_status = ?", (0,))
            wallet_list = await result.fetchall()
            return [wallet[0] for wallet in wallet_list]


async def change_wallet_updated_status_huahua(traders_wallet_address):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE traders_data_huahua SET updated_status = ? WHERE wallet = ?", (1, traders_wallet_address,))
            await conn.commit()


async def change_all_wallets_updated_status_huahua():
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE traders_data_huahua SET updated_status = ? WHERE updated_status = ?", (0, 1,))
            await conn.commit()


async def add_new_tracking_wallet_huahua(user_id, wallet):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO traders_data_huahua (user_id, wallet, bought, sold, bought_volume, sold_volume, bought_value, sold_value, avg_buy_price, avg_sell_price, updated_status, coin_name) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, wallet, 0, 0, "", "", "", "", "", "", 0, "BADDOG / HUAHUA"))
            await conn.commit()


async def get_info_tracking_info_huahua(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT * FROM traders_data_huahua WHERE user_id = ? AND coin_name = ?", (user_id, "BADDOG / HUAHUA",))
            traders_data = await result.fetchone()
            return traders_data


async def update_coins_price(price, token):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE tokens_price SET price = ? WHERE token = ?", (price, token,))
            await conn.commit()


async def get_tokens_price(token):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT price FROM tokens_price WHERE token = ?", (token,))
            token = await result.fetchone()
            return token[0]


async def check_added_wallet_by_user_id(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT user_id FROM traders_data_huahua WHERE user_id = ?", (user_id,))
            user = await result.fetchall()
        return bool(len(user))
