import asyncio
import sys
import requests
from DrissionPage import ChromiumPage, ChromiumOptions


async def scroll_block(driver, pause_time, scroll_count):
    try:
        block = driver.ele('xpath://div[@class="h-[27rem] px-3 pt-3"]')

        count = 0
        while True:
            if count >= scroll_count:
                break
            else:
                try:
                    rows = block.eles('xpath:.//tbody/tr')
                    if not rows:
                        break

                    last_row = rows[-1]

                    last_row.drag_to(block)
                    await asyncio.sleep(pause_time)
                except Exception as error:
                    print(error)
                    break
            count += 1
    except Exception as e:
        print(f"Error: {e}")


async def coinhall_scrap(trader_wallet):
    sys.stdout.reconfigure(encoding='utf-8')

    browser_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    # browser_path = "/usr/bin/google-chrome"


    options = ChromiumOptions()
    options.set_paths(browser_path=browser_path)

    arguments = [
        "-no-first-run",
        "-force-color-profile=srgb",
        "-metrics-recording-only",
        "-password-store=basic",
        "-use-mock-keychain",
        "-export-tagged-pdf",
        "-no-default-browser-check",
        "-disable-background-mode",
        "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
        "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
        "-deny-permission-prompts",
        "-disable-gpu"
        "-headless=new"
        "-incognito"
    ]

    for argument in arguments:
        options.set_argument(argument)


    driver = ChromiumPage(addr_driver_opts=options)


    url = f'https://coinhall.org/osmosis/osmo1j4grkrsre00j5wkx8h6lappsv7ngjhjt6ucs7kzgcpe8dwwrhvtqpjm8dj?trader={trader_wallet}'

    driver.get(url)


    while True:
        try:
            spinner = driver('xpath://div/iframe').ele("xpath://*[@id='challenge-stage']/div/label/input", timeout=0.1)
            if spinner:
                print("get spinner")
                spinner.click()
                await asyncio.sleep(0.5)
            else:
                ele = driver.s_ele('xpath://a[@class="text-xs font-medium text-violet-300 underline transition duration-100 hover:text-violet-200 sm:text-sm inactive"]')
                if ele.text == "Follow @HallFDN for $HALL updates!":
                    break
                await asyncio.sleep(0.5)
        except:
            ele = driver.s_ele('xpath://a[@class="text-xs font-medium text-violet-300 underline transition duration-100 hover:text-violet-200 sm:text-sm inactive"]')
            if ele.text == "Follow @HallFDN for $HALL updates!":
                break
        await asyncio.sleep(0.5)

    await asyncio.sleep(5)

    # await scroll_block(driver, pause_time=1.5, scroll_count=5)

    html = driver.html

    # with open("html.txt", 'w', encoding='utf-8') as file:
    #     file.write(html)

    return html
