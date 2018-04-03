import time
import datetime
import numpy
import random
from faker import Faker
from tzlocal import get_localzone

local = get_localzone()
faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime.now()
outFileName = 'web_app_log' + timestr + '.log'

f = open(outFileName, 'w')

level = ["Info", "Notice", "Debug", "Error", "Warning", "Critical"]

# Http Header
resources = ["/list", "/wp-content", "/wp-admin", "/explore", "/search/tag/list", "/app/main/posts",
             "/posts/posts/explore", "/apps/cart.jsp?appID=", "/login"]
verb = ["GET", "POST", "DELETE", "PUT"]
# Http Message
response = ["200", "404", "500", "301"]
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
    vrb = numpy.random.choice(verb, p=[0.6, 0.1, 0.1, 0.2])

    uri = random.choice(resources)
    if uri.find("apps") > 0:
        uri += str(random.randint(1000, 10000))

    resp = numpy.random.choice(response, p=[0.9, 0.04, 0.02, 0.04])
    byt = int(random.gauss(5000, 50))
    referer = faker.uri()
    useragent = numpy.random.choice(ualist, p=[0.3, 0.5, 0.1, 0.05, 0.05])()

    if counter % 3 == 0:
        f.write('%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s"\n' % (
            dt, "Info", "192.34.238.24 ", "POST", "/login", "503", byt, useragent))
    f.write('%s FakeWebApp.%s %s "%s %s HTTP/1.0" %s %s "%s"\n' % (
        dt, logLevel, ip, vrb, uri, resp, byt, useragent))
    f.flush()

    if increment:
        time.sleep(1)
