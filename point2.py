#!/usr/bin/env python3
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import sys
import socket
from urllib import parse

def normalizeUrl(url):
	if not url.startswith('http'):
		return 'http://' + url
	return url

# very loosy validation: leave to the browser mind reading euristics
def looksValidUrl(url):
	if len(url) < 4:
		return False
	if "@" in url:
		return False
	if url.startswith('about:'):
		# yeah... somobody put "about:blank" as a PA web site
		return False
	return True
	
# very loosy check: ideally only verify if the DNS can resolve the hostname
def looksReachableUrl(url):
	try:
		split_url = parse.urlsplit(url)
		socket.gethostbyname(split_url.netloc)
		return True
	except:
		return False

def saveError(lineNum, error):
	fname = 'out/%s.ERR.txt' % lineNum
	with open(fname, 'w') as f:
		f.write(error)
	

def runCheck(pa, lineNum, script):
	url = pa[8].lower()
	if len(url) == 0:
		return # nothing to do... not even logging an error...
	if not looksValidUrl(url):
		saveError(lineNum, "invalid url: %s" % url)
		return

	url = normalizeUrl(url)
# Disabled: seemed a good idea, but can take several seconds to timeout
#           anyway and is less stable then the browser anyway
#           (for example the server might resolve to an unreachable
#            ip or redirect to an unreachable host)
#	if not looksReachableUrl(url):
#		saveError(lineNum, "unreachable: %s" % url)
#		return

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
		saveError(lineNum, "%s\n%s" % (url, err))
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
