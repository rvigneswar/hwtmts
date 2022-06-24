import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, subprocess, platform, paramiko


wait_time = 3
driver_path = "/Users/admin/FTC_Solar/Legacy/Hardware_team_test_Suite/driver/chromedriver"
url = "http://172.16.0.3"
admin_pass = "Admin"
admin_xpath = '//*[@id="menu-username"]/div[3]/ul/li[1]'


def initialize(wdriver, addrs):
    global driver
    driver = webdriver.Chrome(executable_path=wdriver)
    driver.maximize_window()
    driver.get(addrs)
    time.sleep(wait_time)
    return driver


def login(username, password):
    driver.find_element(By.XPATH, '//*[@id="username-select"]').click()
    driver.find_element(By.XPATH, username).click()
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[2]/form/div[2]/div/input').send_keys(
        password)
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[2]/form/div[3]/div[2]/button').click()
    time.sleep(wait_time)
    name = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/div[2]/div[1]/h6').text
    time.sleep(wait_time)
    return name


def login_invalid_password(username, password):
    driver.find_element(By.XPATH, '//*[@id="username-select"]').click()
    driver.find_element(By.XPATH, username).click()
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[2]/form/div[2]/div/input').send_keys(
        password)
    time.sleep(wait_time)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[2]/form/div[3]/div[2]/button').click()
    time.sleep(wait_time)
    name = driver.find_element(By.XPATH, '//*[@id="client-snackbar"]').text
    driver.close()
    return name


def get_macaddrs(host, port, uname, passwd):
    command = "sed -n 2p /sys/class/net/*/address"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, uname, passwd)
    stdin, stdout, stderr = ssh.exec_command(command)
    ssid = "voyager_"+stdout.readline().rstrip()
    return ssid


def hotspot_checking():
    operating_system = platform.system()
    mac = "Darwin"
    windows = "Windows"
    if operating_system == mac:
        devices = subprocess.check_output("networksetup -listpreferredwirelessnetworks en0", shell=True)
    elif operating_system == windows:
        devices = subprocess.check_output("netsh wlan show network")
    return devices


def about_page():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[6]/button').click()
    driver.implicitly_wait(wait_time * 1000)
    hardware = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/code').text
    version = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/code').text
    driver.close()
    return version, hardware


def download_logs():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[5]/button').click()
    driver.implicitly_wait(wait_time * 1000)
    for i in range(1, 4):
        driver.find_element(By.XPATH,
                            '//*[@id="root"]/div/div/div[1]/main/div[1]/div[1]/ul[1]/div[' + str(i) + ']').click()
        message = driver.find_element(By.XPATH, '//*[@id="client-snackbar"]').text
    driver.close()
    return message


def checking_alerts():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[5]/button').click()
    driver.implicitly_wait(wait_time * 1000)
    style = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div[2]/ul/li[19]').get_attribute(
        'style').split(";")
    bg_color = style[0].split(":")
    driver.close()
    return bg_color[1].strip()


def dashboard():
    zone_id = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/div[2]/div[1]/h6').text
    plant_id = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/div[2]/div[2]/h6').text
    time_stamp = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/div[3]/h6').text
    wind_sensor = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/h6').text
    snow_sensor = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[3]/div/div/div[2]/div[2]/h6').text
    flood_sensor = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[4]/div/div/div[2]/div[2]/h6').text
    driver.implicitly_wait(wait_time*1000)
    for i in range(2, 7):
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a['+str(i)+']/button').click()
        time.sleep(wait_time+2)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[1]/button').click()
    time.sleep(wait_time)
    add_tracker = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/button[1]').text
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/button[2]').click()
    driver.implicitly_wait(wait_time*1000)
    driver.find_element(By.XPATH, '//*[@id="simple-menu"]/div[3]/ul/li[1]').click()
    user_checking = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div[1]/div/div/div/div[1]/h6').text
    driver.close()
    return zone_id, plant_id, time_stamp, wind_sensor, snow_sensor, flood_sensor, user_checking, add_tracker


def sensor_page():
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[4]/button').click()
    driver.implicitly_wait(wait_time*1000)
    sensors_lst = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div[2]/div/table/tbody/tr/td[3]')
    sensors = []
    for sensor in sensors_lst:
        sensors.append(sensor.text)
    driver.close()
    return sensors


def general_settings():
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    time.sleep(wait_time)
    plant_name = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div[2]/div/input').get_attribute("value")
    zone_name = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div[2]/div/input').get_attribute("value")
    location = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div[6]/div/input').get_attribute("value")
    driver.close()
    return plant_name, zone_name, location


def zigbee_settings():
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.implicitly_wait(wait_time*1000)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[2]').click()
    time.sleep(wait_time)
    periodic_request = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div/div[1]/div[2]/div/input').get_attribute("value")
    heartbeat = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div/div[2]/div/div[2]/div/input').get_attribute("value")
    driver.close()
    return periodic_request, heartbeat


def stow_settings():
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.implicitly_wait(wait_time*1000)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[4]').click()
    time.sleep(wait_time)
    wind_speed = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div[2]/div/input').get_attribute("value")
    snow_max = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div[2]/div/input').get_attribute("value")
    flood_max = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[3]/div[2]/div/input').get_attribute("value")
    driver.close()
    return wind_speed, snow_max, flood_max


def time_settings():
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.implicitly_wait(wait_time * 1000)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[5]').click()
    time.sleep(wait_time)
    ntp_server = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div/div/ul/li[1]/div[1]').text
    driver.close()
    return ntp_server


def row_controller():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[2]/button').click()
    time.sleep(1)
    check_box = driver.find_elements(By.XPATH,
                                     '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div/table/tbody/tr[1]/td')
    check_box[0].click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div[3]/p[1]/button').click()
    driver.find_element(By.XPATH, '//*[@id="simple-menu"]/div[3]/ul/li').click()
    params = driver.find_elements(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div[2]/fieldset/div/div/label')
    driver.implicitly_wait(2 + wait_time * 1000)
    print(len(params))
    driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div[2]/div/button').click()
    driver.implicitly_wait(wait_time * 1000)
    driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div/div/div[2]/div/button[1]').click()
    driver.implicitly_wait(1000)
    time.sleep(1)


# initialize(driver_path, url)
# login(admin_xpath, admin_pass)
# print(get_macaddrs("192.168.0.112", 22, "torizon", "sunshine"))
# print(hotspot_checking())
# print(checking_alerts())
# print(dashboard())
# print(sensor_page())
# print(general_settings())