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
        # driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="chromedriver")
        # driver.get("https://login.1688.com/member/signin.htm?tracelog=member_signout_signin")
        # time.sleep(3)
        driver.get(
            "https://p4psearch.1688.com/p4p114/p4psearch/offer.htm?keywords={}&province=%E5%B9%BF%E4%B8%9C&city=%E6%B7%B1%E5%9C%B3&provinceValue=%E6%B7%B1%E5%9C%B3".format(
                kw))
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
        print("①l：", len(l))
        for i in l:
            try:
                i.click()
                all = driver.window_handles
                driver.switch_to_window(all[-1])
                id = re.findall(r"offer/(.*?).html", driver.current_url)[0]
                cur = db.cursor()
                print(id, "----", "cur", cur.execute(query_id, id))
                if cur.execute(query_id, id) < 1:
                    print("②id：", id)
                    cur.execute(insert_id, id)
                    url = "https://detail.1688.com/offer/{}.html?spm=a312h.2018_new_sem.dh_002.9.bcf65ee0JJSa44&tracelog=p4p&clickid=ca57d130afd343ebbae7be48d5f53889&sessionid=13d47a361f39f7818cd4124948b189ad".format(
                        id)
                    response = requests.get(url, cookies=cookie_dict, timeout=10)
                    html = response.content
                    if response.status_code == 200 and len(
                            etree.HTML(html).xpath("//dd[@class='mobile-number']/text()")) > 0:
                        tel = etree.HTML(html).xpath("//dl[@class='m-mobilephone']/@data-no")[0].strip()
                        print("③tel：", tel)
                        name = etree.HTML(html).xpath("//div[@id='mod-detail-title']/h1/text()")[0].strip()
                        company_name = etree.HTML(html).xpath(
                            "//div[@class='supplierinfo-common']//div[@class='company-name']/a//text()|//div[@class='smt-info']//div[@class='nameArea']/a//text()")[
                            0].strip()

                        linkman = etree.HTML(html).xpath(
                            "//div[contains(@class,'mod mod-contactSmall app-contactSmall')]//div[@class='m-content']/div[1]/a/text()")[
                            0].strip()

                        if cur.execute(query_tel, (n, tel)) < 1:
                            print("phone", tel)
                            print("name", name)
                            print("company_name", company_name)
                            print("call_name", linkman)
                            print("*" * 100)
                            cur.execute(sql, (n, name, url, company_name, linkman, tel))
                db.commit()
                cur.close()
                driver.close()
                driver.switch_to_window(all[0])
            except Exception as e:
                print("!!!!!!!错误", e)
                continue
        driver.close()
    db.close()
