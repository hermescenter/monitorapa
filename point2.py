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
	driver = webdriver.Chrome('chromedriver')
	try:
		url = normalizeUrl(pa[8])
		driver.get(url)
		driver.execute_script(script)
		time.sleep(5)
		fname = 'out/%s.txt' % lineNum
		print("%s: found '%s', saved in %s" %(url, driver.title, fname))
		with open(fname, 'w') as f:
			f.write(driver.title)
	except WebDriverException:
		pass
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
			fields = line.split('\t')
			if count > 0:
				runCheck(fields, count, script)
			count += 1
#			if count > 50:
#				break

if __name__ == "__main__":
    main(sys.argv)


