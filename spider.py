
# !/user/bin/env python3
# -*- coding: utf-8 -*-
# 多进程版本

"""已解决的错误：抓取信息为空，出现原因为对同一领导人页面访问过多时会被网站限制访问，通常出现在爬取省委书记和省长时，因此设置每条留言抓取四次，一般其中至少有一条访问成功"""
"""已解决的错误：只有一页没有翻页按钮，没有回复内容查找错误，没有留言内容，没有符合要求的留言，没有该fid"""

import csv
import os
import random
import re
import time

import dateutil.parser as dparser
from random import choice
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


# 时间节点
start_date = dparser.parse('2023-05-01')
# 浏览器设置选项
chrome_options = Options()
chrome_options.add_argument('blink-settings=imagesEnabled=false')

def get_time():
    '''获取随机时间'''
    return round(random.uniform(2, 5), 1)

def get_time2():
    return round(random.uniform(1, 2), 1)

def get_user_agent():
    '''获取随机用户代理'''
    user_agents = [
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    ]
    # 在user_agent列表中随机产生一个代理，作为模拟的浏览器
    user_agent = choice(user_agents)
    return user_agent

def get_fid():
    '''获取所有领导id'''
    with open('fid.txt', 'r') as f:
        content = f.read()
        fids = content.split()
    return fids


def get_detail_urls(position, list_url):
    '''获取每个领导的所有留言链接'''

    user_agent = get_user_agent()
    chrome_options.add_argument('user-agent=%s' % user_agent)
    drivertemp = webdriver.Chrome(options=chrome_options)
    drivertemp.maximize_window()
    drivertemp.get(list_url)
    print("在detail中打开了url为 "+list_url)
    time.sleep(get_time2())

    tids = []
    print("开始爬取detail")

    """三种情况：多页，一页，无留言"""

    # 建言：循环加载页面
    try:
        while WebDriverWait(drivertemp, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, "mordList"))):
            datestr = WebDriverWait(drivertemp, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@class="replyList"]/li[last()]/div[2]/div[1]/p')).text.strip()
            datestr = re.search(r'\d{4}-\d{2}-\d{2}', datestr).group()
            date = dparser.parse(datestr, fuzzy=True)
            print('爬取建言detailurl --', position, '--', date)
            # 模拟点击加载
            if  date < start_date:
                break
            WebDriverWait(drivertemp, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "mordList"))).click()
            time.sleep(1)
    except:
        print("没有下一页")
    finally:
        try:
            message_elements_label1 = drivertemp.find_elements(By.XPATH, '//div[@class="headMainS fl"]//span[@class="t-mr1 t-ml1"]')
            for element in message_elements_label1:
                tid = element.text.strip().split(':')[-1]
                tids.append(tid)
        except:
            print("无留言")
            return

    # 投诉/求助：循环加载页面
    WebDriverWait(drivertemp, 15).until(EC.element_to_be_clickable((By.ID, "tab-second"))).click()
    try:
        while WebDriverWait(drivertemp, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, "mordList"))):
            datestr = WebDriverWait(drivertemp, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@class="replyList"]/li[last()]/div[2]/div[1]/p')).text.strip()
            datestr = re.search(r'\d{4}-\d{2}-\d{2}', datestr).group()
            date = dparser.parse(datestr, fuzzy=True)
            print('爬取投诉求助detailurl --', position, '--', date)
            # 模拟点击加载
            if  date < start_date:
                break
            WebDriverWait(drivertemp, 50, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "mordList"))).click()
            time.sleep(1)
    except:
        print("没有下一页")
    finally:
        try:
            message_elements_label1 = drivertemp.find_elements(By.XPATH, '//div[@class="headMainS fl"]//span[@class="t-mr1 t-ml1"]')
            for element in message_elements_label1:
                tid = element.text.strip().split(':')[-1]
                tids.append(tid)
        except:
            print("无留言")
            return

    # 咨询：循环加载页面
    WebDriverWait(drivertemp, 7).until(EC.element_to_be_clickable((By.ID, "tab-third"))).click()
    try:
        while WebDriverWait(drivertemp, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, "mordList"))):
            datestr = WebDriverWait(drivertemp, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@class="replyList"]/li[last()]/div[2]/div[1]/p')).text.strip()
            datestr = re.search(r'\d{4}-\d{2}-\d{2}', datestr).group()
            date = dparser.parse(datestr, fuzzy=True)
            print('爬取咨询detailurl --', position, '--', date)
            # 模拟点击加载
            if  date < start_date:
                break
            WebDriverWait(drivertemp, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, "mordList"))).click()
            time.sleep(1)
    except:
        print("没有下一页")
    finally:
        try:
            message_elements_label1 = drivertemp.find_elements(By.XPATH, '//div[@class="headMainS fl"]//span[@class="t-mr1 t-ml1"]')
            for element in message_elements_label1:
                tid = element.text.strip().split(':')[-1]
                tids.append(tid)
        except:
            print("无留言")
            return

    # 获取所有链接
    print(position+"的tid列表为"+str(tids))
    for tid in tids:
        detail_url ="https://liuyan.people.com.cn/threads/content?tid={}".format(tid)
        yield detail_url
    drivertemp.quit()


def get_message_detail(driver, detail_url, writer, position, fid):
    '''获取留言详情'''
    driver.get(detail_url)
    print('正在爬取留言 --', position, '--', detail_url)
    max_retries = 3

    # 获取留言各部分内容

    '''.find_elements()没有.text或者.get_attribute的属性，只能用.find_element()'''
    for _ in range(max_retries):
        try:
            print("开始爬取具体信息")
            try:
                # 9回复机构
                reply_institute = WebDriverWait(driver, 2.5).until(
                    lambda driver: driver.find_element(By.XPATH, '//div[@class="replyHandleMain fl"]/div/h4')).text.strip()
                print("try完成")
            except:
                reply_institute = ""
                reply_content = ""
                reply_date = ""
                print("except完成")
            else:
                # 7回复内容
                reply_content = WebDriverWait(driver, 2.5).until(lambda driver: driver.find_element(By.XPATH, '//div[@class="replyHandleMain fl"]//p[@class="handleContent noWrap sitText"]')).text.strip()

                # 8回复时间
                reply_date = WebDriverWait(driver, 2.5).until(
                    lambda driver: driver.find_element(By.XPATH, '//div[@class="handleTime"]')).text
                print("else完成")
            finally:

                # 1留言时间
                message_date = WebDriverWait(driver, 2.5).until(
                    lambda driver: driver.find_element(By.XPATH, '//li[@class="replyMsg"]/span[2]')).text
                print("获取到时间temp为" + message_date)
                message_datetime = dparser.parse(message_date, fuzzy=True)
                if message_datetime < start_date:
                    return

                # 2留言标题
                message_title = WebDriverWait(driver, 2.5).until(lambda driver: driver.find_element(By.XPATH, '//div[@class="replyInfoHead clearfix"]//h1[@class="fl"]')).text.strip()

                # 3留言类型：建言、投诉、咨询
                message_type = WebDriverWait(driver, 2.5).until(lambda driver: driver.find_element(By.XPATH,'//p[@class="typeNameD"]')).text.strip()
                print("留言类型为"+message_type)

                # 4留言标签：城建、医疗、...
                message_label = WebDriverWait(driver, 2.5).until(lambda driver: driver.find_element(By.XPATH,'//p[@class="domainName"]')).text.strip()

                # 5留言状态：已回复、已办理、未回复、办理中
                message_state = WebDriverWait(driver, 2.5).until(
                    lambda driver: driver.find_element(By.XPATH, '//p[@class="stateInfo"]')).text.strip()

                # 6留言内容
                message_content = WebDriverWait(driver, 2.5).until(lambda driver: driver.find_element(By.XPATH, '//div[@class="clearfix replyContent"]//p[@id="replyContentMain"]')).text.strip()

                print("finally完成")

            # 存入CSV文件
            writer.writerow(
                [fid, position, message_title, message_type, message_label, message_state, message_datetime, message_content,
                 reply_content, reply_date, reply_institute])
            print("存入完成")

        except Exception as e:
            print(f"\033[1;30;43m出现错误\033[0m {str(e)}")
            # 页面加载失败，刷新页面
            print("\033[1;30;44m重新打开该网页\033[0m")
            driver.refresh()
            time.sleep(2)




"""三种情况：正常打开一个fid，不存在这个fid，网不好没转出来，使用mobile格式打开了出现错误"""

def get_officer_messages(args):
    '''获取并保存领导的所有留言'''
    user_agent = get_user_agent()
    chrome_options.add_argument('user-agent=%s' % user_agent)
    driver = webdriver.Chrome(options=chrome_options)
    index, fid = args
    list_url = "http://liuyan.people.com.cn/threads/list?fid={}".format(fid)
    driver.get(list_url)    #浏览器中加载url
    print("在officer中打开了url为 "+list_url)

    try:
        try:
            position = WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '//*[@class="leadReplyHead clearfix"]/h2')).text
        except:
            print("没有这个fid")
            return
        else:
            # 文件存在则删除重新创建
            print(index, '-- officer --', position)
            start_time = time.time()
            csv_name = str(fid) + '.csv'
            if os.path.exists(csv_name):
                os.remove(csv_name)
            with open(csv_name, 'a+', newline='', encoding='gb18030') as f:
                writer = csv.writer(f, dialect="excel")
                writer.writerow(
                    ['fid', '职位', '留言标题', '留言类型', '留言标签', '留言状态', '留言日期', '留言内容', '回复内容',
                     '回复日期', '回复机构'])
                for detail_url in get_detail_urls(position, list_url):
                    get_message_detail(driver, detail_url, writer, position, fid)
                    time.sleep(get_time2())
            end_time = time.time()
            crawl_time = int(end_time - start_time)
            crawl_minute = crawl_time // 60
            crawl_second = crawl_time % 60
            print(position, '已爬取结束！！！')
            print('该领导用时：{}分钟{}秒。'.format(crawl_minute, crawl_second))
            driver.quit()
            time.sleep(get_time2())
    except:
        print("返回Office message")
        driver.quit()
        get_officer_messages(args)


def main():
    '''主函数'''
    fids = get_fid()
    print('爬虫程序开始执行：')
    s_time = time.time()
    # 处理传入的参数，使之对应索引合并并且可迭代
    itera_merge = list(zip(range(1, len(fids) + 1), fids))
    # 创建进程池
    pool = Pool(8)
    # 将任务传入进程池并通过映射传入参数
    pool.map(get_officer_messages, itera_merge)
    print('爬虫程序执行结束！！！')
    e_time = time.time()
    c_time = int(e_time - s_time)
    c_minute = c_time // 60
    c_second = c_time % 60
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(s_time)))
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e_time)))
    print('{}位领导共计用时：{}分钟{}秒。'.format(len(fids), c_minute, c_second))

if __name__ == '__main__':
    '''执行主函数'''
    main()



