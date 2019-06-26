#!/usr/bin/env python3
from utils.nginx_page_helper import NginxPage
import time

from retry.api import retry_call

from utils.tools import get_request_text
from utils.log_helper import logger
from utils.init_helper import BaseInit
from utils.config import get_config
from utils.nginx_module_helper import NginxModule


def main():

    baseinit_ins = BaseInit()
    baseinit_ins.es_index_init()

    nginx_doc_url = get_config("common", "nginx_doc_url")
    timeout = int(get_config("common", "timeout"))
    retry = int(get_config("common", "retry"))
    interval = int(get_config("common", "interval"))

    logger.info("Start get url {}".format(nginx_doc_url))
    nginx_module_index_page_html = retry_call(
        get_request_text, fargs=[nginx_doc_url, timeout], tries=retry
    )

    nginxpage_ins = NginxPage(nginx_module_index_page_html)
    nginx_module_names_info = nginxpage_ins.get_module_names()

    # 存储变量和配置名称的相关数据，为搜索添加数据支撑
    keyword_info = []

    for item in nginx_module_names_info:
        module_name = item.split("/")[-1].split(".")[0]
        if module_name.startswith("ngx_") and "http_api" not in module_name:
            nginx_module_ins = NginxModule(item)
            nginx_module_ins.handle_module_direct_info()
            nginx_module_ins.handle_module_vars_info()
            nginx_module_ins.save_module_info_to_es()
            keyword_info.extend(nginx_module_ins.keyword_info)
            time.sleep(interval)

    baseinit_ins.es_ins.insert_mul_index_data("keyword", keyword_info)


if __name__ == "__main__":
    main()
