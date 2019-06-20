#!/usr/bin/env python3
import time

import requests

from utils.log_helper import logger
from utils.nginx_module_menu_helper import get_modules_menu
from utils.nginx_module_page_analyse import common_menu_context_pickup, common_direct_context_pickup
from utils.nginx_module_page_helper import (get_menu_name,
                                            get_modules_variables,
                                            get_nginx_module_item_location,
                                            get_nginx_module_variable_location,
                                            get_nginx_modules)

nginx_doc_url = "http://nginx.org/en/docs/"
requests_timeout = 10
requests_interval = 10
direct_retain_keyword = ["arguments", "summary", "issues", "example", "directives", "compatibility",
                         "definitions", "protocol", "variables", "commands", 'data', 'compatibility', 'properties']


if __name__ == "__main__":
    logger.info("Start get url {}".format(nginx_doc_url))
    nginx_module_page_html = requests.get(
        nginx_doc_url, timeout=requests_timeout).text
    nginx_module_origin_info = get_nginx_modules(nginx_module_page_html)
    for item in nginx_module_origin_info:
        module_name = item.split("/")[-1].split(".")[0]
        if module_name.startswith("ngx_") and "http_api" not in module_name:
            # 初始化菜单结构
            nginx_module_info = {"module_name": module_name, "directive_info": []}

            # 获取具体模块的html内容
            nginx_module_content = requests.get(nginx_doc_url + item, timeout=requests_timeout).text

            # 根据获取的模块页面的导航内容初始化模块详情的json结构
            for direct in get_modules_menu(nginx_module_content):
                if direct in direct_retain_keyword:
                    if direct not in nginx_module_info:
                        if direct == "directives":
                            nginx_module_info[direct] = []
                        else:
                            nginx_module_info[direct] = ""
                else:
                    nginx_module_info["directives"].append(direct)

            variable_info = get_nginx_module_variable_location(nginx_module_content)
            if variable_info:
                nginx_module_info["variables"] = get_modules_variables(variable_info)

            # 获取具体模块的a标签的位置
            for module_item in get_nginx_module_item_location(nginx_doc_url + item).items():
                module_item_name = get_menu_name(module_item)
                if module_item_name not in ["directives", "variables"] and module_item_name in direct_retain_keyword:
                    nginx_module_info[module_item_name] = common_menu_context_pickup(module_item)
                elif module_item_name not in direct_retain_keyword:
                    nginx_module_info["directive_info"].append({"direct_name": module_item_name, "direct_desc": common_direct_context_pickup(module_item) })

            print(nginx_module_info)
        time.sleep(requests_interval)
