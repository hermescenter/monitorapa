# Quick & Dirty PA Web Sin Shamer

Setup python3, selenium and a selenium driver (change python2.py
if you do not want to use cromium driver)

## Get started

### Requirements

- [Python3](https://www.python.org)

On a Debian stable machine
```
apt-get install python3
```
On an Arch machine
```
pacman -S python3
```

If your Python3 package doesn't bundle Pip, you will have to [install it](https://pip.pypa.io/en/stable/installation/).

### Setup the repo and packages

Clone the repo:
```bash
git clone https://github.com/hermescenter/monitorapa.git
```
Enter the repo directory:
```bash
cd monitorapa
```
Create a Python Virtual Environment:
```bash
python -m venv .venv
```
Activate your environment:
- Windows
  ```bash
  .\.venv\Scripts\activate.bat
  ```
- Linux
  ```bash
  ./.venv/bin/activate
  ```

Install the required packages:
```bash
pip install -r requirements.txt
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
   amministrazioni.txt file, for example out/100.OK.txt
   (or out/100.ERR.txt in case of error)

Obviously, if GA is not found, the file will be empty.
If GA is found, it will contains the tracking ID (or any other metadata)

## Point 3
```
./point3.py
```

Will produce a new file point3.amministrazione.txt enriched as for specification.
