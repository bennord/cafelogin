# cafelogin

A python command line tool for logging into cafe wifi portals.

## Install

```zsh
pip install cafelogin
```

## Usage

```zsh
cafelogin [-h] [-c CONFIG_FILE] [--driver-version DRIVER_VERSION]
```

Run the command once with an internet connection to install the default web-driver to the cache.

Examples:

```zsh
# Check connection and login via any detected portal
cafelogin

# Specify a web-driver version to use
cafelogin --driver-version "v0.28.0"
```
