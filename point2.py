#!/usr/bin/env python3
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import sys

def normalizeUrl(url):
	if not url.startswith('http'):
		return 'http://' + url
	return url

def runCheck(pa, lineNum, script):
	if "@" in pa[8]:
		fname = 'out/%s.ERR.txt' % lineNum
		with open(fname, 'w') as f:
			f.write("invalid url: %s" % pa[8])
		return
	op = webdriver.ChromeOptions()
	op.add_argument('--headless')
	op.add_argument('--disable-web-security')

	driver = webdriver.Chrome('chromedriver', options=op)
	try:
		url = normalizeUrl(pa[8])
		driver.get(url)
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
	driver.close()

def usage():
	print("""
./point2.py test_to_run.js
""")
	sys.exit(-1)

def main(argv):
	if len(argv) != 2:
		usage()
	test = argv[1]
	count = 0
	with open('amministrazioni.txt', 'r') as f, open(test) as s:
		script = s.read()
		for line in f:
			if count > 0:
				fields = line.split('\t')
				runCheck(fields, count, script)
			count += 1
#			if count > 121:
#				break

if __name__ == "__main__":
    main(sys.argv)


