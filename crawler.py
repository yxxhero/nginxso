#!/usr/bin/env python3
import time

from retry.api import retry_call

from utils.log_helper import logger
from utils.nginx_page_helper import NginxModulePage, NginxPage
from utils.tools import get_menu_name, get_request_text
from utils.elasticsearch_helper import ElasticSearch
from utils.config import get_config

nginx_doc_url = "http://nginx.org/en/docs/"
requests_timeout = 10
requests_interval = 10
requests_retry = 3
direct_retain_keyword = ["endpoints", "arguments", "summary", "issues", "example", "directives", "compatibility",
                         "definitions", "protocol", "variables", "commands", 'data', 'compatibility', 'properties']
keyword_map = {
    "mappings": {
        "properties": {
            "keyword": {
                "type": "text"
            },
            "module_name": {
                "type": "text"
            }
        }

    }
}

module_map = {
    "mappings": {
        "properties": {
            "module_name": {
                "type": "text"
            },
            "compatibility": {
                "type": "text"
            },
            "properties": {
                "type": "text"
            },
            "arguments": {
                "type": "text"
            },
            "definitions": {
                "type": "text"
            },
            "protocol": {
                "type": "text"
            },
            "commands": {
                "type": "text"
            },
            "data": {
                "type": "text"
            },
            "summary": {
                "type": "text"
            },
            "variables": {
                "type": "object"
            },
            "issues": {
                "type": "text"
            },
            "example": {
                "type": "text"
            },
            "endpoints": {
                "type": "nested"
            },
            "directives": {
                "type": "text"
            },
            "directive_info": {
                "type": "nested"
            }
        }

    }
}


def main():

    logger.info("初始化es实例")
    es_ins = ElasticSearch(ips=get_config("elasticsearch", "ips"), port=get_config("elasticsearch", "port"))

    # 创建es索引
    es_ins.create_index("keyword", keyword_map)
    es_ins.create_index("module", module_map)

    logger.info("Start get url {}".format(nginx_doc_url))

    nginx_module_index_page_html = retry_call(
        get_request_text, fargs=[nginx_doc_url, requests_timeout], tries=requests_retry)

    nginxpage_ins = NginxPage(nginx_module_index_page_html)
    nginx_module_origin_info = nginxpage_ins.get_module_names()

    # 存储变量和配置名称的相关数据，为搜索添加数据支撑
    keyword_info = []

    for item in nginx_module_origin_info:
        module_name = item.split("/")[-1].split(".")[0]
        if module_name.startswith("ngx_") and "http_api" not in module_name:
            # 初始化菜单结构
            nginx_module_info = {
                "module_name": module_name, "directive_info": []}

            # 获取具体模块的html内容
            nginx_module_content = retry_call(get_request_text, fargs=[
                                              nginx_doc_url + item, requests_timeout], tries=requests_retry)

            nginxmodulepage_ins = NginxModulePage(nginx_module_content)

            # 根据获取的模块页面的导航内容初始化模块详情的json结构
            for direct in nginxmodulepage_ins.get_module_menus():
                if direct in direct_retain_keyword:
                    if direct not in nginx_module_info:
                        if direct == "directives":
                            nginx_module_info[direct] = []
                        else:
                            nginx_module_info[direct] = ""
                else:
                    # 不在保留字中即为具体指令名称
                    nginx_module_info["directives"].append(direct)
                    for i in nginx_module_info["directives"]:
                        keyword_info.append(
                            {"keyword": i, "module_name": module_name})

            variable_info = nginxmodulepage_ins.get_module_variable_location()
            if variable_info:
                nginx_module_info["variables"] = nginxmodulepage_ins.get_module_variables(
                    variable_info)
                for j in nginx_module_info["variables"]["var_names"]:
                    keyword_info.append(
                        {"keyword": j, "module_name": module_name})

            # 获取具体模块的a标签的位置
            for module_item in nginxmodulepage_ins.get_module_item_location().items():
                module_item_name = get_menu_name(module_item)
                if module_item_name not in ["directives", "variables"] and module_item_name in direct_retain_keyword:
                    nginx_module_info[module_item_name] = nginxmodulepage_ins.common_menu_context_pickup(
                        module_item)
                elif module_item_name not in direct_retain_keyword:
                    nginx_module_info["directive_info"].append(
                        {"direct_name": module_item_name, "direct_desc": nginxmodulepage_ins.common_direct_context_pickup(module_item)})

            module_query_body = {
                "query": {
                    "term": {
                        "module_name": {
                            "value": module_name,
                            "boost": 1.0
                        }
                    }
                }
            }
            es_ins.delete_index_data_by_query("module", module_query_body)
            es_ins.insert_one_index_data("module", nginx_module_info)
            time.sleep(requests_interval)

    allkeyword = list(set([item["keyword"] for item in keyword_info]))
    keyword_info.append({
        "keyword": "allkeyword",
        "module_name": allkeyword
        })
    es_ins.insert_mul_index_data("keyword", keyword_info)


if __name__ == "__main__":
    main()
