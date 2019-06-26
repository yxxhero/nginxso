#!/usr/bin/env python3
from utils.nginx_page_helper import NginxModulePage
from utils.tools import get_menu_name, get_request_text
from utils.init_helper import BaseInit
from utils.config import get_config
from retry.api import retry_call


class NginxModule(object):
    def __init__(self, item):
        self.item = item
        self.module_name = self.get_module_name()
        self.nginx_module_info = {"module_name": self.module_name, "directive_info": []}
        self.nginx_module_content = self.get_nginx_module_page_content()
        self.nginxmodulepage_ins = NginxModulePage(self.nginx_module_content)
        self.baseinit_ins = BaseInit()
        self.keyword_info = []

    def get_module_name(self):
        return self.item.split("/")[-1].split(".")[0]

    def get_nginx_module_page_content(self):
        return retry_call(
            get_request_text,
            fargs=[
                get_config("common", "nginx_doc_url") + self.item,
                int(get_config("common", "timeout")),
            ],
            tries=int(get_config("common", "retry")),
        )

    def handle_module_direct_info(self):
        # 根据获取的模块页面的导航内容初始化模块详情的json结构
        for direct in self.nginxmodulepage_ins.get_module_menus():
            if direct in self.baseinit_ins.direct_retain_keyword:
                if direct not in self.nginx_module_info:
                    if direct == "directives":
                        self.nginx_module_info[direct] = []
                    else:
                        self.nginx_module_info[direct] = ""
            else:
                # 不在保留字中即为具体指令名称
                self.nginx_module_info["directives"].append(direct)
        direct_list = [
            {"keyword": i, "module_name": self.module_name}
            for i in self.nginx_module_info["directives"]
        ]
        self.keyword_info.extend(direct_list)

    def handle_module_vars_info(self):

        variable_info = self.nginxmodulepage_ins.get_module_variable_location()
        if variable_info:
            self.nginx_module_info[
                "variables"
            ] = self.nginxmodulepage_ins.get_module_variables(variable_info)
            vars_list = [
                {"keyword": i, "module_name": self.module_name}
                for i in self.nginx_module_info["variables"]["var_names"]
            ]
            self.keyword_info.extend(vars_list)

        # 获取具体模块的a标签的位置
        for module_item in self.nginxmodulepage_ins.get_module_item_location().items():
            module_item_name = get_menu_name(module_item)
            if (
                module_item_name not in ["directives", "variables"]
                and module_item_name in self.baseinit_ins.direct_retain_keyword
            ):
                self.nginx_module_info[
                    module_item_name
                ] = self.nginxmodulepage_ins.common_menu_context_pickup(module_item)
            elif module_item_name not in self.baseinit_ins.direct_retain_keyword:
                self.nginx_module_info["directive_info"].append(
                    {
                        "direct_name": module_item_name,
                        "direct_desc": self.nginxmodulepage_ins.common_direct_context_pickup(
                            module_item
                        ),
                    }
                )

    def save_module_info_to_es(self):
        module_query_body = {
            "query": {
                "term": {"module_name": {"value": self.module_name, "boost": 1.0}}
            }
        }
        self.baseinit_ins.es_ins.delete_index_data_by_query("module", module_query_body)
        self.baseinit_ins.es_ins.insert_one_index_data("module", self.nginx_module_info)
