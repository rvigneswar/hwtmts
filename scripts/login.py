import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
from scp import SCPClient
import time, subprocess, platform, paramiko, os, shutil

wait_time = 3
driver_path = "/Users/admin/FTC_Solar/Legacy/Hardware_team_test_Suite/driver/chromedriver"
url = "http://192.168.95.13"
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
    ssid = "voyager_" + stdout.readline().rstrip()
    return ssid


def hotspot_checking():
    operating_system = platform.system()
    mac = "Darwin"
    windows = "Windows"
    if operating_system == mac:
        devices = subprocess.check_output("networksetup -listpreferredwirelessnetworks en0", shell=True)
    elif operating_system == windows:
        i = 0
        while i <= 10:
            devices = subprocess.check_output('netsh wlan show network | find /I "SSID"', shell=True).decode().split(
                "\r\n")
            time.sleep(2)
            i = i + 1
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
        time.sleep(3)
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
    wind_sensor = driver.find_element(By.XPATH,
                                      '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/h6').text
    snow_sensor = driver.find_element(By.XPATH,
                                      '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[3]/div/div/div[2]/div[2]/h6').text
    flood_sensor = driver.find_element(By.XPATH,
                                       '//*[@id="root"]/div/div/div[1]/main/div[2]/div/div[2]/div[4]/div/div/div[2]/div[2]/h6').text
    time.sleep(2)
    for i in range(2, 7):
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[' + str(
            i) + ']/button').click()
        time.sleep(wait_time + 2)
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[1]/button').click()
    time.sleep(wait_time)
    add_tracker = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/button[1]').text

    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/header/div/button[2]').click()
    driver.implicitly_wait(wait_time * 1000)
    driver.find_element(By.XPATH, '//*[@id="simple-menu"]/div[3]/ul/li[1]').click()
    driver.implicitly_wait(wait_time * 3000)
    user_checking = driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div/div/div[1]/main/div[1]/div[1]/div/div/div/div[1]/h6').text
    driver.implicitly_wait(wait_time * 3000)
    driver.close()
    return zone_id, plant_id, time_stamp, wind_sensor, snow_sensor, flood_sensor, user_checking, add_tracker


def sensor_page():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[4]/button').click()
    driver.implicitly_wait(wait_time * 1000)
    sensors_lst = driver.find_elements(By.XPATH,
                                       '//*[@id="root"]/div/div/div[1]/main/div[1]/div[2]/div/table/tbody/tr/td[3]')
    sensors = [x.text for x in sensors_lst]
    temp1 = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div[2]/div/table/tbody/tr/td[4]')
    model_number = [x.text for x in temp1]
    temp2 = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div[2]/div/table/tbody/tr/td[2]')
    port_number = [x.text for x in temp2]
    driver.close()
    return sensors, model_number, port_number


def general_settings():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    time.sleep(wait_time)
    plant_name = driver.find_element(By.XPATH,
                                     '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div[2]/div/input').get_attribute(
        "value")
    zone_name = driver.find_element(By.XPATH,
                                    '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div[2]/div/input').get_attribute(
        "value")
    location = driver.find_element(By.XPATH,
                                   '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div[6]/div/input').get_attribute(
        "value")
    driver.close()
    return plant_name, zone_name, location


def zigbee_settings():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.implicitly_wait(wait_time * 1000)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[2]').click()
    time.sleep(wait_time)
    periodic_request = driver.find_element(By.XPATH,
                                           '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div/div[1]/div[2]/div/input').get_attribute(
        "value")
    heartbeat = driver.find_element(By.XPATH,
                                    '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div/div[2]/div/div[2]/div/input').get_attribute(
        "value")
    driver.close()
    return periodic_request, heartbeat


def ethernet_settings():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[3]').click()
    time.sleep(wait_time)
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div[1]/div[2]/button[1]').click()
    driver.implicitly_wait(2 + wait_time * 1000)
    dynamic_ip = driver.find_element(By.XPATH,
                                     '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div[6]/div/input').get_attribute(
        "value")
    time.sleep(wait_time)
    driver.close()
    if bool(dynamic_ip):
        return True, dynamic_ip
    else:
        return False, dynamic_ip


def stow_settings():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.implicitly_wait(wait_time * 1000)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[4]').click()
    time.sleep(wait_time)
    wind_speed = driver.find_element(By.XPATH,
                                     '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div[2]/div/input').get_attribute(
        "value")
    snow_max = driver.find_element(By.XPATH,
                                   '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div[2]/div/input').get_attribute(
        "value")
    flood_max = driver.find_element(By.XPATH,
                                    '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[3]/div[2]/div/input').get_attribute(
        "value")
    driver.close()
    return wind_speed, snow_max, flood_max


def time_settings():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.implicitly_wait(wait_time * 1000)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[5]').click()
    time.sleep(wait_time)
    temp = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div/div/ul/li')
    driver.close()
    ntp_servers = [x.text for x in temp]
    return ntp_servers


def board_temp():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[3]/button').click()
    driver.implicitly_wait(wait_time * 3000)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/button[7]').click()
    driver.implicitly_wait(wait_time * 3000)
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div/div/div/div/button[2]').click()
    driver.implicitly_wait(wait_time * 3000)
    temp = driver.find_element(By.XPATH,
                               '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/h2').text
    driver.close()
    return temp


def disk_usage(host, port, uname, passwd):
    command = "df -h | grep /dev/disk/by-label/otaroot | awk '{print $3}'"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, uname, passwd)
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.readline()


def ram_usage(host, port, uname, passwd):
    command = "free -mh | grep Mem | awk '{print $3}'"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, uname, passwd)
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.readline()


def zigbee_pad_ids():
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/nav/div[2]/div/div/div/div/div[2]/div/a[2]/button').click()
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/main/div[1]/header/div/div/div/div/div/button[2]').click()
    time.sleep(3)
    pan_id_1 = driver.find_element(By.XPATH, '//*[@id="scanParameter"]').get_attribute("value")
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div/div[1]/main/div[1]/div/div[1]/div/div/div/div/button[2]').click()
    time.sleep(3)
    pan_id_2 = driver.find_element(By.XPATH, '//*[@id="scanParameter"]').get_attribute("value")
    driver.close()
    if bool(pan_id_1) and bool(pan_id_2):
        return True
    else:
        return False


def checking_sd_card(host, port, uname, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, uname, passwd)
    stdin, stdout, stderr = ssh.exec_command("ls /dev/")
    output = stdout.readlines()
    for line in output:
        if "mmcblk1" in line.split('\n'):
            return True
    else:
        return False


def checking_bluetooth(host, port, uname, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, uname, passwd)
    stdin, stdout, stderr = ssh.exec_command("dmesg")
    output = stdout.readlines()
    for line in output:
        if "Blue" in line.split('\n'):
            return True
        else:
            return False


def checking_cpu_temp(host, port, uname, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, uname, passwd)
    stdin, stdout, stderr = ssh.exec_command("cat /sys/class/thermal/thermal_zone0/temp")
    temp = stdout.readline().split('\n')
    return temp[0]


def sensors_data(host, port, uname, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, uname, password)
    scp = SCPClient(client.get_transport())
    os.makedirs("log")
    sensor_logs = ["wind.log", "snow.log", "flood.log"]
    for item in sensor_logs:
        client.exec_command(f"docker cp web:/var/log/voyager/{item} ~/{item}")
        time.sleep(10)
        scp.get(item, f"./log/{item}")
        client.exec_command(f"rm {item}")
    with open(f"log/flood.log", "r") as file:
        flood_values = file.readlines()[-3]
    # print("flood: " + values)
    with open("log/snow.log", "r") as file:
        snow_value = file.readlines()[-2]
    # print("Snow: " + line)
    shutil.rmtree("log")
    return flood_values, snow_value



# def checking_serives(host, port, uname, passwd):
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(host, port, uname, passwd)
#     stdin, stdout, stderr = ssh.exec_command("docker exec -it web bash")
#     stdin, stdout, stderr = ssh.exec_command("cd ./install/app_config/service/files")
#     stdin, stdout, stderr = ssh.exec_command("")


# initialize(driver_path, url)
# login(admin_xpath, admin_pass)
# print(time_settings())
# print(ethernet_settings())
# print(zigbee_pad_ids())
# print(get_macaddrs("192.168.0.112", 22, "torizon", "sunshine"))
# print(hotspot_checking())
# print(checking_alerts())
# print(dashboard())
# print(sensor_page())
# print(general_settings())
# print(disk_usage("192.168.95.11", 22, "torizon", "sunshine"))
# print(ram_usage("192.168.95.11", 22, "torizon", "sunshine"))
# print(checking_sd_card("192.168.95.11", 22, "torizon", "sunshine"))
