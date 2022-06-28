from scripts import login
import pytest
import os, unittest

os_type = os.name
if os_type == "nt":
    driver_path = str(os.getcwd()) + "/driver/chromedriver.exe"
elif os_type == "posix":
    driver_path = str(os.getcwd()) + "/driver/chromedriver"
url = "http://192.168.95.11"
admin_xpath = '//*[@id="menu-username"]/div[3]/ul/li[1]'
admin_pass = "Admin"
sw_version = "2.7.0.29"
hw_version = "1.00.000"
zone = "ZCVignesh"
plant = "VigneshPlant"
time_stp = "IST"
w_sensor = "Disabled"
s_sensor = "Disabled"
f_sensor = "Disabled"
host = url[7:]
port = 22
username = 'torizon'
password = 'sunshine'
location = "Central"


def test_login_admin():
    x = login.initialize(driver_path, url)
    result = login.login(admin_xpath, admin_pass)
    x.close()
    assert result == zone


def test_login_invalid_password():
    login.initialize(driver_path, url)
    result = login.login_invalid_password(admin_xpath, "xyz111")
    assert result == '"Invalid password."'


def test_login():
    x = login.initialize(driver_path, url)
    result = login.login(admin_xpath, admin_pass)
    x.close()
    assert result == zone


def test_hotspot():
    mac_id = login.get_macaddrs(host, port, username, password)
    result = login.hotspot_checking()
    assert mac_id in str(result)


def test_about_page():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    version, hardware = login.about_page()
    assert version == sw_version
    assert hardware == hw_version


def test_download_log():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    mess = login.download_logs()
    assert mess == "Successfully downloaded the file."


def test_red_alerts():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    color = login.checking_alerts()
    assert color == "rgba(255, 0, 0, 0.61)"


def test_dashboard():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    zone_id, plant_name, time_stamp, wind_sensor, snow_sensor, flood_sensor, usr_page, tracker_data = login.dashboard()
    assert zone_id == zone
    assert plant_name == plant
    assert time_stamp == time_stp
    assert wind_sensor == w_sensor
    assert snow_sensor == s_sensor
    assert flood_sensor == f_sensor
    assert usr_page == "Change Password"
    assert tracker_data == 'Add Trackers'


def test_zigbee_pan_id():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    result = login.zigbee_pad_ids()
    assert result


def test_sensor_page():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    lst_sensor = login.sensor_page()
    assert "Wind" in lst_sensor
    assert "Flood" in lst_sensor
    assert "Snow" in lst_sensor


def test_general_settings():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    p_name, z_name, loc = login.general_settings()
    assert p_name == plant
    assert z_name == zone
    assert loc == location


def test_dynamic_ip():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    d_ip = login.ethernet_settings()
    assert d_ip


def test_zigbee_settings():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    periodic_requests, heartbeat = login.zigbee_settings()
    assert periodic_requests == "600"
    assert heartbeat == "10000"


def test_stow_settings():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    w_speed, s_max, f_max = login.stow_settings()
    assert w_speed == '15'
    assert s_max == "300"
    assert f_max == "300"


def test_time_settings():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    ntp_url = login.time_settings()
    assert ntp_url == "0.debian.pool.ntp.org"


def test_board_temp():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    print(login.board_temp()+" Cel")


def test_disk_ram_used():
    print(login.disk_usage(host, port, username, password))
    print(login.ram_usage(host, port, username, password))


def test_checking_sd_card():
    login.checking_sd_card(host, port, username, password)


def test_bluetooth():
    login.checking_bluetooth(host, port, username, password)
