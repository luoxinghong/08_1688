# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests
from lxml import etree
import re
import pymysql
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

db = pymysql.connect(host="localhost", user="root",
                     password="lxh123", db="1688", port=3306)
insert_id = "insert into total_id (id_num) values (%s)"
query_id = "select * from total_id where id_num=%s"
query_tel = "select * from info4 where tel=%s"
sql = "insert into info4(goods_name,url,company_name,linkman,tel) values (%s,%s,%s,%s,%s) "


def work(kw):
    for h in range(1, 51):
        print("*" * 100, h)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
        # driver = webdriver.Chrome(executable_path="chromedriver")
        url = "https://p4psearch.1688.com/p4p114/p4psearch/offer.htm?keywords={}&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&provinceValue=%E6%B7%B1%E5%9C%B3".format(quote(kw[1]))
        driver.get(url)
        time.sleep(3)

        page_number = driver.find_element_by_css_selector(".next-input.next-input-single.next-input-large")

        click_button = driver.find_element_by_css_selector(
            ".next-btn.next-btn-normal.next-btn-large.next-pagination-go")
        actions = ActionChains(driver)
        actions1 = ActionChains(driver)
        actions.move_to_element(page_number)
        actions.click()
        actions.send_keys(h)
        actions.perform()
        actions1.move_to_element(click_button)
        actions1.click().perform()
        time.sleep(8)
        for j in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        l = driver.find_elements_by_class_name("offer_item")
        for i in l:
            try:
                i.click()
                all = driver.window_handles
                time.sleep(5)
                driver.switch_to_window(all[-1])
                id = re.findall(r"offer/(.*?).html", driver.current_url)[0]
                url = "https://m.1688.com/offer/{}.htm".format(id)
                cur = db.cursor()
                if cur.execute(query_id, id) < 1:
                    cur.execute(insert_id, id)
                    driver.get(url)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    # print("111goods_id：", id)
                    company_id_list = re.findall(r'"memberId":"(.*?)",|"sellerMemberId": "(.*?)",', driver.page_source)[0]
                    company_id = [i for i in company_id_list if i != ""][0]
                    driver.get("https://m.1688.com/winport/company/{}.html".format(company_id))
                    # print("222company_url""https://m.1688.com/winport/company/{}.html".format(company_id))
                    time.sleep(3)
                    phone = re.findall(r'phone">(.*)<', driver.page_source)[0]
                    # print("333phone：", phone)

                    company_name = driver.find_element_by_xpath('//*[@id="scroller"]/div[1]/ul/li[1]/div/span').text
                    # print("444company_name：", company_name)

                    goods_name = driver.find_element_by_xpath('//*[@id="scroller"]/div[1]/ul/li[4]/div/span').text
                    # print("555goods_name：", goods_name)

                    linkman = re.findall(r'''>系</p><p>人 </p>: </em>
                <span>(.*)</span>''', driver.page_source)[0]
                    # print("666linkman：", linkman)

                    if phone.startswith("1") and cur.execute(query_tel, phone) < 1:
                        print("phone：", phone)
                        print("goods_name：", goods_name)
                        print("company_name：", company_name)
                        print("linkman：", linkman)
                        cur.execute(sql, (goods_name, url, company_name, linkman, phone))
                    db.commit()
                    cur.close()

            except Exception as e:
                print(url)
                print(company_id_list)
                print("!!!!!!!错误", e)
            finally:
                if len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to_window(all[0])
                print("*" * 100)
            continue
        driver.close()
    db.close()


if __name__ == "__main__":
    key_words = ["男装", "内衣", "鞋靴", "箱包", "配饰", "运动服饰", "运动装备", "母婴用品", "童装", "玩具", "工艺品", "宠物", "园艺", "日用百货", "办公文教",
                 "汽车用品", "食品饮料", "餐饮生鲜", "家纺家饰", "家装建材", "美容化妆", "个护家清", "3C", "手机", "家电", "电工电气", "照明", "仪表", "包装",
                 "印刷纸业",
                 "电子元器件", "安防", "机械", "五金工具", "劳保", "橡塑", "化工", "精细", "钢材", "纺织皮革", "医药"]

    executor = ThreadPoolExecutor(max_workers=10)

    for kw in enumerate(key_words):
        future = executor.submit(work, kw)
