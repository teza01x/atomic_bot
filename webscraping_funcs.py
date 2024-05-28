import asyncio
import re
from bs4 import BeautifulSoup


async def parse_coinhall_traders(html):
    try:
        # with open('html.txt', 'r', encoding='utf-8') as file:
        #     html = file.read()

        soup = BeautifulSoup(html, 'html.parser')

        trade_info_block = soup.find('div', class_="h-[27rem] px-3 pt-3")

        price_block = soup.find('div', class_='inline-flex items-center')
        price = price_block.find('span', attrs={'price': True})
        price = price['price']

        # txs_block = soup.find('div', class_='h-full overflow-x-auto overflow-y-auto break-normal rounded-lg bg-gray-850 [-webkit-overflow-scrolling:touch]')
        # transactions = []
        #
        # for tr in txs_block.find_all('tr'):
        #     try:
        #         tds = tr.find_all('td')
        #         if len(tds) == 0:
        #             continue
        #
        #         date_time = tds[0].get_text(strip=True)
        #         transaction_type = tds[1].find('div', class_='text-right').get_text(strip=True)
        #         price1 = tds[2].find('span').get_text(strip=True).replace('\u2009', '')
        #         price2 = tds[3].find('span').get_text(strip=True).replace('\u2009', '')
        #         quantity = tds[4].find('span').get_text(strip=True).replace('\u2009', '')
        #         address = tds[5].find('span').get_text(strip=True)
        #         link = tds[6].find('a')['href']
        #
        #         transactions.append({
        #             'date_time': date_time,
        #             'type': transaction_type,
        #             'price1': price1,
        #             'price2': price2,
        #             'quantity': quantity,
        #             'address': address,
        #             'link': link
        #         })
        #     except Exception as error:
        #         print(error)
        # for transaction in transactions:
        #     print(transaction)


        traders_block = trade_info_block.find('thead')
        rows = traders_block.find_all('tr')

        count = 0

        bought_info = list()
        sold_info = list()
        for row in rows[-2:]:
            count += 1

            if count == 1:
                buys = row.find('th', class_='flex justify-end whitespace-nowrap py-2 text-right font-normal').text
                buys = buys.split()[0]
                span = row.find_all('span', attrs={'price': True})
                avg_buy_price = float(span[-3]['price'])
                avg_buy_price = "{:.15f}".format(avg_buy_price)
                bought_volume = round(float(span[-2]['price']), 2)
                bought_value = round(float(span[-1]['price']), 2)

                bought_info.append([buys, bought_volume, bought_value, avg_buy_price])

            elif count == 2:
                sells = row.find('th', class_='flex justify-end whitespace-nowrap py-2 text-right font-normal').text
                sells = sells.split()[0]
                span = row.find_all('span', attrs={'price': True})
                avg_sell_price = float(span[-3]['price'])
                avg_sell_price = "{:.15f}".format(avg_sell_price)
                sold_volume = round(float(span[-2]['price']), 2)
                sold_value = round(float(span[-1]['price']), 2)

                sold_info.append([sells, sold_volume, sold_value, avg_sell_price])

        return bought_info, sold_info, price
    except Exception as error:
        print(error)
