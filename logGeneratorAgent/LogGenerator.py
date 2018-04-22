import time
import datetime
import numpy
import random
from faker import Faker
from tzlocal import get_localzone


def same_username_login_scenario(file, dt, logLevel, ip, byt, useragent):
    for i in range(9):
        ip = faker.ipv4()
        file.write(unsuccessful_login(dt, "Info", ip, "503", byt, useragent, "same_username"))
    file.write(unsuccessful_login(dt, "Error", ip, "503", byt, useragent, "same_username"))
    file.flush()
    return


def same_ip_login_scenario(file, dt, logLevel, ip, byt, useragent):
    for i in range(9):
        file.write(unsuccessful_login(dt, "Info", ip, "503", byt, useragent, "Unsuccessful Login"))
    file.write(unsuccessful_login(dt, "Error", ip, "503", byt, useragent, "Unsuccessful Login same IP"))
    file.flush()
    return


def unsuported_ip_alert(file, dt, logLevel, ip, byt, useragent):
    resources = ["GET", "POST", "PUT", "DELETE"]
    resource = numpy.random.choice(resources, p=[0.6, 0.15, 0.15, 0.1])
    file.write(
        '%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s Unsuported IP Address"\n' % (
            dt, "Error", ip, resource, "/recipe", "404", byt, useragent))
    file.flush()
    return


def random_scenario(file, dt, logLevel, ip, byt, useragent):
    options = [search_recipe, search_recipes, add_recipe, update_recipe, delete_recipe]
    file.write(successful_login(dt, logLevel, ip, "200", byt, useragent))
    for i in range(random.randint(2, 10)):
        resp = numpy.random.choice(response, p=[0.9, 0.04, 0.02, 0.04])
        logLevel = numpy.random.choice(level, p=[0.5, 0.1, 0.3, 0.02, 0.01, 0.07])
        file.write(
            numpy.random.choice(options, p=[0.15, 0.35, 0.2, 0.25, 0.05])(dt, logLevel, ip, resp, byt, useragent))
    file.write(successful_logout(dt, logLevel, ip, "200", byt, useragent))
    file.flush()
    return


def search_recipes(dt, logLevel, ip, resp, byt, useragent, message=""):
    return '%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s %s"\n' % (
        dt, logLevel, ip, "GET", "/recipe", resp, byt, useragent, message)


def search_recipe(dt, logLevel, ip, resp, byt, useragent, message=""):
    return '%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s %s"\n' % (
        dt, logLevel, ip, "GET", "/recipe/" + str(random.randint(1000, 10000)), resp, byt, useragent, message)


def add_recipe(dt, logLevel, ip, resp, byt, useragent, message=""):
    return '%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s %s"\n' % (
        dt, logLevel, ip, "POST", "/recipe", resp, byt, useragent, message)


def update_recipe(dt, logLevel, ip, resp, byt, useragent, message=""):
    return '%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s %s"\n' % (
        dt, logLevel, ip, "PUT", "/recipe/" + str(random.randint(1000, 10000)), resp, byt, useragent, message)


def delete_recipe(dt, logLevel, ip, resp, byt, useragent, message=""):
    return '%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s %s"\n' % (
        dt, logLevel, ip, "DELETE", "/recipe/" + str(random.randint(1000, 10000)), resp, byt, useragent, message)


def successful_login(dt, logLevel, ip, resp, byt, useragent, message=""):
    return '%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s %s"\n' % (
        dt, logLevel, ip, "POST", "/login", resp, byt, useragent, message)


def successful_logout(dt, logLevel, ip, resp, byt, useragent, message=""):
    return '%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s %s"\n' % (
        dt, logLevel, ip, "POST", "/logout", resp, byt, useragent, message)


def unsuccessful_login(dt, logLevel, ip, resp, byt, useragent, message=""):
    return '%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s %s"\n' % (
        dt, logLevel, ip, "POST", "/login", resp, byt, useragent, message)


local = get_localzone()
faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime.now()
outFileName = 'web_app_log' + timestr + '.log'

f = open(outFileName, 'w')
response = ["200", "404", "500", "301"]
level = ["Info", "Notice", "Debug", "Error", "Warning", "Critical"]
resources_and_scenarios = [same_ip_login_scenario, same_username_login_scenario, unsuported_ip_alert, random_scenario]
ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

flag = True
counter = 0
while flag:
    counter += 1

    increment = datetime.timedelta(seconds=random.randint(1, 5))
    otime += increment

    dt = otime.strftime('%Y-%m-%dT%H:%M:%S.0Z')
    tz = datetime.datetime.now(local).strftime('%z')

    logLevel = numpy.random.choice(level, p=[0.5, 0.1, 0.3, 0.02, 0.01, 0.07])
    ip = faker.ipv4()
    byt = int(random.gauss(5000, 50))

    useragent = numpy.random.choice(ualist, p=[0.3, 0.5, 0.1, 0.05, 0.05])()

    numpy.random.choice(resources_and_scenarios, p=[0.05, 0.1, 0.05, 0.8])(f, dt, logLevel, ip, byt,
                                                                           useragent)

    if increment:
        time.sleep(1)
