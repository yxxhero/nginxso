#!/usr/bin/env python3
import requests
import time

from utils.log_helper import logger
from utils.nginx_module_menu_helper import get_modules_menu
from utils.nginx_module_page_helper import get_nginx_modules, get_nginx_module_item, get_nginx_module_variable_info, get_modules_variables

nginx_doc_url = "http://nginx.org/en/docs/"
requests_timeout = 5
retain_keyword = ["arguments", "summary", "issues", "example", "directives", "compatibility", "definitions", "protocol", "variables", "commands", 'data', 'compatibility', 'properties']


if __name__ == "__main__":
    logger.info("Start get url {}".format(nginx_doc_url))
    nginx_module_page_html = requests.get(
        nginx_doc_url, timeout=requests_timeout).text
    nginx_module_origin_info = get_nginx_modules(nginx_module_page_html)
    for item in nginx_module_origin_info:
        module_name = item.split("/")[-1].split(".")[0]
        if module_name.startswith("ngx_") and "http_api" not in module_name:
            # print(get_modules_menu(nginx_doc_url + item))
            # print(get_nginx_module_item(nginx_doc_url + item))
            variable_info = get_nginx_module_variable_info(nginx_doc_url + item)
            if variable_info:
                print(item)
                print(get_modules_variables(variable_info))
            time.sleep(1)
