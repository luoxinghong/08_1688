# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests
from lxml import etree
import xlrd, xlwt
import re
import pymysql


def work(n, kw, ck_str):
    cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in ck_str.split("; ")}

    db = pymysql.connect(host="localhost", user="root",
                         password="lxh123", db="1688", port=3306)

    insert_id = "insert into total_id (id_num) values (%s)"
    query_id = "select * from total_id where id_num=%s"
    query_tel = "select * from info%s where tel=%s"
    sql = "insert into info%s(goods_name,url,company_name,linkman,tel) values (%s,%s,%s,%s,%s) "

    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path="chromedriver")

    for h in range(1, 51):
        print("!" * 100, h)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
        # driver = webdriver.Chrome(executable_path="chromedriver")
        # driver.get("https://login.1688.com/member/signin.htm?tracelog=member_signout_signin")
        # time.sleep(3)
        driver.get(
            "https://p4psearch.1688.com/p4p114/p4psearch/offer.htm?keywords={}&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&provinceValue=%E6%B7%B1%E5%9C%B3".format(kw))
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
        time.sleep(5)
        for j in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        l = driver.find_elements_by_class_name("offer_item")
        print("：：：：：：：：：：", len(l))
        for i in l:
            try:
                i.click()
                all = driver.window_handles
                time.sleep(3)
                driver.switch_to_window(all[-1])
                id = re.findall(r"offer/(.*?).html", driver.current_url)[0]
                url = "https://m.1688.com/offer/{}.htm".format(id)

                cur = db.cursor()
                if cur.execute(query_id, id) < 1:
                    cur.execute(insert_id, id)
                    # print("000url：", url)
                    driver.get(url)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    # print("111id：", id)
                    company_id = re.findall(r'"memberId":"(.*?)",', driver.page_source)[0]
                    # print("222company_id：", company_id)
                    driver.get("https://m.1688.com/winport/company/{}.html".format(company_id))
                    print("https://m.1688.com/winport/company/{}.html".format(company_id))
                    time.sleep(3)
                    phone = re.findall(r'phone">(.*)<', driver.page_source)[0]
                    # print("333phone：", phone)

                    company_name = driver.find_element_by_xpath('//*[@id="scroller"]/div[1]/ul/li[1]/div/span').text
                    # print("444company_name：", company_name)

                    goods_name = driver.find_element_by_xpath('//*[@id="scroller"]/div[1]/ul/li[4]/div/span').text
                    # print("555goods_name：", goods_name)

                    # linkman = driver.find_element_by_xpath('//*[@id="scroller"]/div[3]/ul/li[1]/div/span').text
                    linkman = re.findall(r'''>系</p><p>人 </p>: </em>
                <span>(.*)</span>''',driver.page_source)[0]
                    # print("666linkman：", linkman)

                    if cur.execute(query_tel, (n, phone)) < 1:
                        print("phone：", phone)
                        print("goods_name：", goods_name)
                        print("company_name：", company_name)
                        print("linkman：", linkman)
                        cur.execute(sql, (n, goods_name, url, company_name, linkman, phone))
                    db.commit()
                    cur.close()

            except Exception as e:
                print("!!!!!!!错误", e)
            finally:
                if len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to_window(all[0])
                print("*" * 100)
            continue
        driver.close()
    db.close()