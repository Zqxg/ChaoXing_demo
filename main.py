from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.edge.service import Service


edge_service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=edge_service)

driver.implicitly_wait(8)
driver.get('http://passport2-api.chaoxing.com/login?fid=&refer=')
driver.maximize_window()  # 最大化浏览器窗口


# 学校 学号 密码
def login():
    # 账号 密码
    input_phone_number = str(123456789)
    input_password = '密码'
    # 定位
    username = driver.find_element(By.XPATH, '//*[@id="phone"]')
    password = driver.find_element(By.ID, 'pwd')
    # 传入
    username.send_keys(input_phone_number)
    password.send_keys(input_password)
    # 定位登录元素+点击该元素
    driver.find_element(By.ID, 'loginBtn').click()
    print("---------- 正在登陆 ----------")


# 进入主页，选择课程,并进入
def html_1():
    time.sleep(random.random() * 3)  # *3表示生成0-3直接的数字
    print("---------- 登录成功 ----------\n----------正在进入课程----------")
    time.sleep(3)  # 固定等待3s
    driver.switch_to.frame('frame_content')  # 定位到名为frame_content的框架下，这样才可以找到内部的元素
    time.sleep(2)

    # 点击元素
    driver.find_element(By.XPATH, '//*[@id="c_237393989"]/div[2]/h3/a').click()
    print("----------进入课程成功----------\n----------正在进入章节----------")




# 选章节
def html_2():
    time.sleep(1)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        driver.find_element(By.XPATH, '//*[@id="nav_6893"]/a').click()
        print('----------进入章节成功----------')
        time.sleep(random.random() * 3)
        driver.switch_to.frame('frame_content-zj')
        time.sleep(1)

        # 进入具体视频界面
        # //*[@id="cur787164946"]/div/div[2]/
        driver.find_element(By.XPATH, '//*[@id="cur787164949"]/div/div[2]/a').click()
        time.sleep(random.random() * 3)
        print('----------进入小结成功----------')
        time.sleep(1)
    else:
        print("没有第二个窗口句柄。")


# 点击播放课程
def video_button():
    time.sleep(random.random() * 5)
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame('iframe')  # 定位该页面框架
        time.sleep(3)  # 此处等待需要久一些就不会报错终止程序
        frame = driver.find_element(By.XPATH, '//*[@id="ext-gen1050"]/iframe')
        driver.switch_to.frame(frame)
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@id="video"]/button').click()
        print('---------- 等待播放 ----------')
        time.sleep(1)
        print("----------课程正在播放中----------")

    except Exception as e:  # except Exception as e:这种写法是捕获所有类型的异常。不论try中出现什么异常,都会执行except中相应处理代码。
        print('Error at:', e.args[0], e.args[1])  # 查看错误元组第一和第二的错误信息
        driver.switch_to.default_content()
        print("----------此处不是视频，即将点击下一页----------")
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="prevNextFocusNext"]').click()
        time.sleep(2)
        #   重回button
        video_button()


# 下一页
def next_page():
    time.sleep(1)

    try:
        driver.switch_to.default_content()
        time.sleep(2)
        driver.find_element(By.ID, 'prevNextFocusNext').click()
        time.sleep(2)
        print('---------即将进入下一页----------')
    except Exception:
        print('---------课程播放结束----------')


# 判断课程是不是视频
def is_video():
    try:
        driver.switch_to.frame('iframe')
        time.sleep(random.random() * 2)
        frame = driver.find_element(By.XPATH, '/html/body/div[2]/div/p/div/iframe')
        time.sleep(random.random() * 2)
        driver.switch_to.frame(frame)
        driver.find_element(By.XPATH, '//*[@id="video"]/button')
        # driver.find_element(By.CLASS_NAME, 'prev_title')
        return 1
    except:
        driver.switch_to.default_content()
        return 0

# 判断当前任务点是否完成
def is_task_completed():
    try:
        # 切换到iframe
        driver.switch_to.default_content()
        driver.switch_to.frame('iframe')  # 定位该页面框架
        time.sleep(3)  # 此处等待需要久一些就不会报错终止程序

        # 查找具有特定 aria-label 属性值的元素
        task_element = driver.find_element(By.XPATH, '//*[@id="ext-gen1051"]')  # 替换为实际的定位方式
        aria_label = task_element.get_attribute("aria-label")
        # 如果找到符合条件的元素，表示任务点已完成
        # 检查 aria-label 属性的值
        if aria_label == "任务点已完成":
            print("----------任务点已完成----------")
            return True
        else:
            print("----------任务点未完成----------")
            return False
    except Exception:
        print("--------找不到任务点元素--------")
        return False

# 判断视频是否播放完成
def is_video_finished():
    try:
        # 获取视频元素
        video = driver.find_element(By.XPATH, '//*[@id="video_html5_api"]')  # 请替换为实际的视频元素定位方式

        # 获取视频的当前时间和总时长
        current_time = video.get_property("currentTime")
        duration = video.get_property("duration")

        # 如果当前时间等于总时长，表示视频已播放完
        if current_time == duration:
            return True
        else:
            return False
    except Exception as e:
        print("视频状态检测失败:", str(e))
        return False

# 判断课程是否为ppt
def is_ppt():
    try:
        driver.switch_to.frame('iframe')
        time.sleep(random.random() * 2)
        frame1 = driver.find_element(By.XPATH, '//*[@id="ext-gen1048"]/div[2]/div/p/div/iframe')
        driver.switch_to.frame(frame1)
        return 1
    except:
        driver.switch_to.default_content()
        return 0

# 完成对ppt的播放
def go_ppt():
    driver.switch_to.frame('iframe')
    time.sleep(random.random() * 2)
    frame1 = driver.find_element(By.XPATH, '//*[@id="ext-gen1048"]/div[2]/div/p/div/iframe')
    driver.switch_to.frame(frame1)
    time.sleep(random.random() * 2)
    frame2 = driver.find_element(By.ID, 'panView')
    time.sleep(random.random() * 2)
    driver.switch_to.frame(frame2)
    driver.execute_script('window.scrollBy(0,1000000)', '')
    time.sleep(random.random() * 2)
    driver.switch_to.default_content()
    time.sleep(random.random() * 2)
    driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
    next_page()

# 提示 当前章节还有任务点（测验）未完成，是否去完成？
def warning_task():
    try:
        # 使用WebDriverWait等待元素出现，最多等待3秒
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainid"]/div[1]/div')))
        # 如果元素出现，执行点击下一页按钮的操作
        if element.is_displayed():
            print("----------任务点（测验）未完成----------")
            return 1
    except:
        driver.switch_to.default_content()
        print("提示框未出现")
        return 0

# 跳过警告 下一页
def jump_warn():
    try:
        driver.switch_to.default_content()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="mainid"]/div[1]/div/div[3]/a[2]').click()
        time.sleep(1)
        print("----------跳过警告进入下一页----------")
    except Exception:
        print('---------跳过警告失败----------')

if __name__ == '__main__':
    circulate_flag = True
    login()
    html_1()
    html_2()
    while circulate_flag:
        if is_video():
            if not is_task_completed():
                video_button()
                play_flag = False
                # 在视频未播放完的情况下，不断检查视频状态
                while not is_video_finished():
                    time.sleep(1)  # 每隔一秒检查一次
                # 当视频播放完毕，执行翻页操作
                next_page()
            else:
                next_page()

        if is_ppt():
            go_ppt()
        else:
            if warning_task():
                jump_warn()
            else:
                next_page()
