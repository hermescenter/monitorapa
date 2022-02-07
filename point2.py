#!/usr/bin/env python3
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import sys
import socket
from urllib import parse

def normalizeUrl(url):
	url = url.lower()
	if not url.startswith('http'):
		return 'http://' + url
	return url

def runCheck(pa, lineNum, script):
	valid_hostname=True
	url = ""
	try:
		url = normalizeUrl(pa[8])
		split_url = parse.urlsplit(url)
		socket.gethostbyname(split_url.netloc)
	except:
		valid_hostname=False

	if "@" in pa[8] or pa[8] == "" or not valid_hostname:
		fname = 'out/%s.ERR.txt' % lineNum
		with open(fname, 'w') as f:
			f.write("invalid url: %s" % pa[8])
		return

	op = webdriver.ChromeOptions()
	op.add_argument('--headless')
	op.add_argument('--disable-web-security')
	op.add_argument('--no-sandbox')
	op.add_argument('--disable-extensions')
	op.add_argument('--dns-prefetch-disable')
	op.add_argument('--disable-gpu')
	op.add_argument('--ignore-certificate-errors')
	op.add_argument('--ignore-ssl-errors')
	op.add_argument('enable-features=NetworkServiceInProcess')
	op.add_argument('disable-features=NetworkService')
	op.add_argument('--window-size=1920,1080')
	op.add_argument('--aggressive-cache-discard')
	op.add_argument('--disable-cache')
	op.add_argument('--disable-application-cache')
	op.add_argument('--disable-offline-load-stale-cache')
	op.add_argument('--disk-cache-size=0')

	driver = webdriver.Chrome('chromedriver', options=op)

	try:
		driver.get(url)
		time.sleep(2)
		driver.execute_script(script)
		time.sleep(8)
		fname = 'out/%s.OK.txt' % lineNum
		with open(fname, 'w') as f:
			f.write(driver.title)
		print("%s: found '%s', saved in %s" %(url, driver.title, fname))
	except WebDriverException as err:
		fname = 'out/%s.ERR.txt' % lineNum
		with open(fname, 'w') as f:
			f.write("%s\n" % url)
			f.write("%s" % err)
	#time.sleep(100000)
	driver.close()

def usage():
	print("""
./point2.py test_to_run.js [optional=starting_index]
""")
	sys.exit(-1)

def main(argv):
	if len(argv) > 3 or len(argv) < 2:
		usage()
	test = argv[1]
	try:
		starting_index = int(argv[2])
	except:
		starting_index = 0
	count = 0
	with open('amministrazioni.txt', 'r') as f, open(test) as s:
		script = s.read()
		for line in f:
			if count > 0 and count >= starting_index:
				fields = line.split('\t')

				try:
					runCheck(fields, count, script)
				except (KeyboardInterrupt):
					print("Esco")
					break
				except:
					print("Qualcosa è andato storto con una scheda. Informazioni della scheda: ")
					print("Fields: " + str(fields))
					print("Count: " + str(count))

			count += 1
#			if count > 121:
#				break

if __name__ == "__main__":
    main(sys.argv)
