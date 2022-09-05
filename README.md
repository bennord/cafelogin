# cafelogin

A python command line tool for logging into cafe wifi portals.

### Compatibility:
- Browser WebDriver
  - Chrome
  - Firefox (Geckodriver)
- Wifi Portal
  - https://service.wi2.ne.jp
    - Starbucks JP
    - Wired Cafe JP
    - Doutor JP

## Install

```zsh
pip install cafelogin
```

## Usage

```sh
cafelogin [-h] [-c CONFIG_FILE] [--version] [--browser {chrome,firefox}] [--chrome-driver-version CHROME_DRIVER_VERSION] [--firefox-driver-version FIREFOX_DRIVER_VERSION] [--watch] [--watch-interval WATCH_INTERVAL]
```

Examples:

```sh
# Check portal connection and login via any detected portal
cafelogin

# Watch the portal connection continuously for changes
cafelogin --watch

# Specify a web-driver version to use
cafelogin --browser firefox --firefox-driver-version "v0.28.0"
```

## WebDriver cache

Run the command once with an internet connection to install the web-driver to the cache.

```
cafelogin

[WDM] - ====== WebDriver manager ======
[WDM] - There is no [linux64] geckodriver for browser  in cache
[WDM] - Getting latest mozilla release info for v0.29.0
[WDM] - Trying to download new driver from https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
[WDM] - Driver has been saved in cache [/home/me/.wdm/drivers/geckodriver/linux64/v0.29.0]
```
