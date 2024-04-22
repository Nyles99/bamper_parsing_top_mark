from selenium import webdriver
import zipfile
import time
import os


def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()
    
    if use_proxy:
        chrome_options.add_argument("--proxy-server=188.119.120.30:40623")

    if user_agent:
        chrome_options.add_argument(f"--user-agent={user_agent}")

    driver = webdriver.Chrome(options=chrome_options)

    return driver

def main():
    driver = get_chromedriver(use_proxy=True)
    driver.get("https://atomurl.net/myip/")
    time.sleep(15)
    driver.quit()

if __name__ == "__main__":
    main()
