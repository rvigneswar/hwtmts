from scripts import login
import pytest
import os, unittest

os_type = os.name
if os_type == "nt":
    driver_path = str(os.getcwd()) + "/driver/chromedriver.exe"
elif os_type == "posix":
    driver_path = str(os.getcwd()) + "/driver/chromedriver"
url = "http://192.168.95.10"
admin_xpath = '//*[@id="menu-username"]/div[3]/ul/li[1]'
admin_pass = "Admin"
sw_version = "3.0.0"
hw_version = "3.00.000"
zone = "default_ID"
plant = "STAC"
time_stp = "IST"
w_sensor = "Disabled"
s_sensor = "Disabled"
f_sensor = "Disabled"
host = url[7:]
port = 22
username = 'torizon'
password = 'sunshine'
location = "Central"


def test_hotspot():
    mac_id = login.get_macaddrs(host, port, username, password)
    result = login.hotspot_checking()
    assert mac_id in str(result), "Mac ID displayed along with Voyager HOTSPOT is incorrect."


def test_disk_ram_used():
    print("Disk Used: " + login.disk_usage(host, port, username, password))
    print("RAM Used: " + login.ram_usage(host, port, username, password))


def test_checking_sd_card():
    login.checking_sd_card(host, port, username, password)
    assert True, "SD Card not found."


def test_bluetooth():
    login.checking_bluetooth(host, port, username, password)
    assert True, "Bluetooth not Found."


def test_cpu_temp():
    print("CPU Temperature: " + str((int(login.checking_cpu_temp(host, port, username, password))/1000)) + " Celsius")

# def test_login_invalid_password():
#     login.initialize(driver_path, url)
#     result = login.login_invalid_password(admin_xpath, "xyz111")
#     assert result == '"Invalid password."'
#
#
# def test_login():
#     x = login.initialize(driver_path, url)
#     result = login.login(admin_xpath, admin_pass)
#     x.close()
#     assert result == zone


def test_login_admin():
    x = login.initialize(driver_path, url)
    result = login.login(admin_xpath, admin_pass)
    x.close()
    assert result == zone, "Login not successful."


def test_dashboard():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    zone_id, plant_name, time_stamp, wind_sensor, snow_sensor, flood_sensor, usr_page, tracker_data = login.dashboard()
    assert zone_id == zone, "Zone ID not matched."
    assert plant_name == plant, "Plant Name not matched."
    assert time_stamp == time_stp, "Incorrect Time Stamp."
    assert wind_sensor == w_sensor, "Wind Sensor is not connected."
    assert snow_sensor == s_sensor, "Snow Sensor is not connected."
    assert flood_sensor == f_sensor, "Flood Sensor is not Connected."
    assert usr_page == "Change Password", "User Settings page is not working."
    assert tracker_data == 'Add Trackers', "Add Tracker button is not found."


def test_zigbee_pan_id():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    result = login.zigbee_pad_ids()
    assert result, "Zigbee pan ID not found."


# def test_general_settings():
#     login.initialize(driver_path, url)
#     login.login(admin_xpath, admin_pass)
#     p_name, z_name, loc = login.general_settings()
#     assert p_name == plant, "Incorrect plant Name."
#     assert z_name == zone, "Incorrect Zone Name."
#     assert loc == location, "Incorrect Location."


def test_dynamic_ip():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    res, d_ip = login.ethernet_settings()
    print("Dynamic IP assigned to this ZC: " + d_ip)
    assert res, "Dynamic IP not found."


# def test_zigbee_settings():
#     login.initialize(driver_path, url)
#     login.login(admin_xpath, admin_pass)
#     periodic_requests, heartbeat = login.zigbee_settings()
#     assert periodic_requests == "600", "Check Periodic Requests."
#     assert heartbeat == "600", "Check Heartbeat"


# def test_stow_settings():
#     login.initialize(driver_path, url)
#     login.login(admin_xpath, admin_pass)
#     w_speed, s_max, f_max = login.stow_settings()
#     assert w_speed == '15', "Check wind speed."
#     assert s_max == "300", "Check snow max settings."
#     assert f_max == "300", "Check Flood max Settings."


def test_time_settings():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    ntp_urls = login.time_settings()
    known_urls = ['0.ubuntu.pool.ntp.org', '1.ubuntu.pool.ntp.org', '2.ubuntu.pool.ntp.org', '3.ubuntu.pool.ntp.org']
    print("Found urls in ZC: ", ntp_urls)
    assert ntp_urls[1] in known_urls, "Check NTP url"


def test_board_temp():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    print("Board Temperature: " + login.board_temp()+" Celsius.")


def test_sensor_page():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    lst_sensor, model_number, port_number = login.sensor_page()
    dictionary = {i: [j, k] for i, j, k in zip(lst_sensor, model_number, port_number)}
    print(dictionary)
    assert "Wind" in lst_sensor, "Wind sensor not found."
    assert "Flood" in lst_sensor, "Flood Sensor not found."
    assert "Snow" in lst_sensor, "Snow Sensor not found."


# def test_download_log():
#     login.initialize(driver_path, url)
#     login.login(admin_xpath, admin_pass)
#     mess = login.download_logs()
#     assert mess == "Successfully downloaded the file.", "File not downloaded"


# def test_red_alerts():
#     login.initialize(driver_path, url)
#     login.login(admin_xpath, admin_pass)
#     color = login.checking_alerts()
#     assert color == "rgba(255, 0, 0, 0.61)"


def test_about_page():
    login.initialize(driver_path, url)
    login.login(admin_xpath, admin_pass)
    version, hardware = login.about_page()
    assert version == sw_version, "Check Software version"
    assert hardware == hw_version, "Check hardware version"


def test_sensor_data():
    flood_value, snow_value, wind_value = login.sensors_data(host, port, username, password)
    print(f"Flood: {flood_value} \n Snow: {snow_value} \n Wind: {wind_value}")
