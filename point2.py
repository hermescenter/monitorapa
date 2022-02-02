#!/usr/bin/env python3
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time

script = """
setTimeout(function(){
var html = document.all[0].innerHTML;
var test = html.match(/ga\('create', '.*'/);
if(!test){
	test = html.match(/gtag\('config', '.*'/);
}
document.title = test[0];
}, 0)
"""

def normalizeUrl(url):
	if not url.startswith('http'):
		return 'http://' + url
	return url

def runCheck(pa, lineNum):
	driver = webdriver.Chrome('chromedriver')
	try:
		url = normalizeUrl(pa[8])
		driver.get(url)
		originalTitle = driver.title
		driver.execute_script(script)
		time.sleep(5)
		newTitle = driver.title
		if originalTitle != newTitle:
			print("%s: %s -> %s" % (lineNum, url, driver.title))
		else:
			print("%s: %s -> NO Analytics"%(lineNum, url))
	except WebDriverException:
		pass
	driver.close()

count = 0
with open('amministrazioni.txt', 'r') as f:
	for line in f:
		fields = line.split('\t')
		if count > 0:
			runCheck(fields, count)
		count += 1
		if count > 50:
			break
	

