#This file is used to send request to the server and get the response from the server
#the input is the land code and url
#the output is the response from the server
import random
import psycopg2
import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from dotenv import load_dotenv

load_dotenv()
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G985F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 10; en-us; SM-N960U Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (BB10; Touch) AppleWebKit/537.35+ (KHTML, like Gecko) Version/10.3.3.3216 Mobile Safari/537.35+",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254",
    "Mozilla/5.0 (Windows NT 10.0; ARM; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254"
]
request = requests.Session()
class SendRequest:
    AMAZON_BASE_URL = "https://www.amazon.com/"
    def __init__(self, land_code, url):
        self.land_code = land_code
        self.url = url

    def send_request(self):
       def send_request(url):

        index = 0

        """Fetch and parse subcategories using requests and BeautifulSoup."""
        userAgentIndex = random.randint(0, len(USER_AGENTS) - 1)
        user = USER_AGENTS[userAgentIndex]
        # if "ref" in url:
        #     url = url.split("ref")[0]
        headers = {
            "user-agent": user,
             "Cookie": "uQEO+0qKCQfzI7nHWfd1pdzL2v8lKZmhW0OGIzAUjSH8ZESnSiO2TD58r8IuZ6xw8sJn1ve"
                         "/Ndf/cjciqUYzg5K14tNT1RbavpKNWxmHDYfL7pPp+SkvXMD1qFEF7BaAWWJuypaTFEddGKwl8SgIaqQ/"
                         "iZPcFFHPBfyBAEX507EAWOEUiazCsDG6aAzudHv/Lo+77wvm81x8wrko8nO2xfWP3SCdA8vKM8bP24u9uaKMVD2oxytQuCV+1Ey0TSXiJYFw9UNbfGjxQ8CF2prWanvK42m9N3+SWE2AGcBGwRapLcWhLSoQGiZdGnQYL2qNTFfNlAjI/g6XBvQ8XpMDOtNS/WJxlm7u ",


            "Referer": "https://www.amazon.com",
            "authority": "www.amazon.com",
            "path": url,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
        }

        full_url = "https://www.amazon.com" + url
        print(full_url)
        request.headers.update(headers)
        retryBackOff = 1
        response = None
        while not response:
            response = request.get(full_url, headers=headers, cookies={})
            if retryBackOff >= 10:
                break
            time.sleep(retryBackOff)
            retryBackOff = retryBackOff + 1
        print('Response HTTP Status Code: ', response.status_code)
        return response

