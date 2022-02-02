# Quick & Dirty PA Web Sin Shamer

Setup python3, selenium and a selenium driver (change python2.py
if you do not want to use cromium driver)

On a Debian stable machine
```
apt-get install python3 python3-selenium chromium-driver
```

## Point 1

```
./point1.py
```
Downloads amministrazione.txt

## Point 2

```
./point2.py ./google_analytics.js
```
Run point 2 checks over all the website listed in amministrazione.txt.

The software works this way:

1. python.py open the target websites in the Selenium Driver
   and run the provided JavaScript
2. google_analytics.js contains the JavaScript code used to detect
   Google Analytics. If it find GA, it put the tracking ID (or any 
   other metadata) in document's title or empty it if the site is
   free from Google Analytics surveillance.
3. python.py, after 5 seconds, get the title and write it into a file
   in the out/ directory named after its line number in the
   amministrazioni.txt file 

Obviously, if GA is not found, the file will be empty.
If GA is found, it will contains the tracking ID (or any other metadata)

