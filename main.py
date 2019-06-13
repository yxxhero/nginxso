#!/usr/bin/env python3
from pyquery import PyQuery as pq
from utils.nginx_module_page_helper import get_nginx_modules
from utils.log_helper import logger
import requests

nginx_doc_url = "http://nginx.org/en/docs/"
requests_timeout = 5


if __name__ == "__main__":
    logger.info("Start get url {}".format(nginx_doc_url))
    nginx_module_page_html = requests.get(nginx_doc_url, timeout=requests_timeout).text
    print(get_nginx_modules(nginx_module_page_html))
