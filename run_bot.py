import requests
from bs4 import BeautifulSoup
import os
import random
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


PAGE_URL = "https://www.facebook.com/profile.php?id=61585080781447"

KEYWORDS = [
    "ของใช้ในบ้าน",
    "gadgets",
    "อุปกรณ์มือถือ"
]


# -----------------------------
# ดึงสินค้า Shopee
# -----------------------------
def get_products(keyword):

    url = f"https://shopee.co.th/search?keyword={keyword}"

    headers = {
        "user-agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    products = []

    items = soup.select("a[data-sqe='link']")

    for item in items[:20]:

        title = item.get("title")
        link = "https://shopee.co.th" + item.get("href")

        img = item.find("img")
        image = img.get("src") if img else None

        if title and image:

            products.append({
                "title": title,
                "link": link,
                "image": image
            })

    return products


# -----------------------------
# ดาวน์โหลดรูป
# -----------------------------
def download_image(url, name):

    if not os.path.exists("images"):
        os.mkdir("images")

    path = f"images/{name}.jpg"

    r = requests.get(url)

    with open(path, "wb") as f:
        f.write(r.content)

    return os.path.abspath(path)


# -----------------------------
# เปิด browser
# -----------------------------
def start_browser():

    options = uc.ChromeOptions()

    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)

    driver.get("https://www.facebook.com")

    print("กรุณา Login Facebook แล้วกด Enter")

    input()

    return driver


# -----------------------------
# โพสต์ Facebook
# -----------------------------
def post_to_facebook(driver, message, image):

    driver.get(PAGE_URL)

    time.sleep(10)

    post_box = driver.find_element(By.XPATH, "//div[@role='textbox']")

    post_box.click()

    post_box.send_keys(message)

    time.sleep(3)

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")

    file_input.send_keys(image)

    time.sleep(10)

    post_btn = driver.find_element(By.XPATH, "//div[@aria-label='Post']")

    post_btn.click()

    print("โพสต์แล้ว")

    time.sleep(20)


# -----------------------------
# สร้าง Caption
# -----------------------------
def generate_caption(product):

    captions = [
        "🔥 สินค้าขายดีใน Shopee",
        "🔥 โปรลดราคาวันนี้",
        "🔥 แนะนำสินค้าดีราคาถูก",
        "🔥 ของใช้ยอดฮิต"
    ]

    caption = random.choice(captions)

    msg = f"""
{caption}

{product['title']}

สั่งซื้อ
{product['link']}

#Shopee #โปรShopee
"""

    return msg


# -----------------------------
# Run Bot
# -----------------------------
def run_bot():

    keyword = random.choice(KEYWORDS)

    products = get_products(keyword)

    random.shuffle(products)

    products = products[:10]

    driver = start_browser()

    for i, p in enumerate(products):

        print("กำลังโพสต์:", p["title"])

        img = download_image(p["image"], f"product{i}")

        message = generate_caption(p)

        post_to_facebook(driver, message, img)

        sleep_time = random.randint(3600, 7200)

        print("พัก", sleep_time, "วินาที")

        time.sleep(sleep_time)


# -----------------------------

run_bot()