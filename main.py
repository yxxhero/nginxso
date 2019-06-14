#!/usr/bin/env python3
import requests
from pyquery import PyQuery as pq

from utils.log_helper import logger
from utils.nginx_module_page_helper import get_nginx_modules

nginx_doc_url = "http://nginx.org/en/docs/"
requests_timeout = 5


if __name__ == "__main__":
    logger.info("Start get url {}".format(nginx_doc_url))
    nginx_module_page_html = requests.get(nginx_doc_url, timeout=requests_timeout).text
    nginx_module_origin_info = get_nginx_modules(nginx_module_page_html)
    for item in nginx_module_origin_info:
        module_name = item.split("/")[-1].split(".")[0]
        if module_name.startswith("ngx_"):
            print(module_name)
