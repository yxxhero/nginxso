from pyquery import PyQuery as pq
from utils.tools import is_menu_item
from utils.log_helper import logger


class NginxBase(object):
    def __init__(self, html):
        self.d = pq(html)


class NginxPage(NginxBase):
    def get_module_names(self):

        # 获取nginx的所有模块
        logger.info("获取所有模块页面列表")
        nginx_module_locations = self.d("center").filter(
            lambda i, this: pq(this).children("h4").text() == "Modules reference"
        )
        return [
            item.attr("href")
            for item in nginx_module_locations.nextAll("ul").find("a").items()
        ]


class NginxModulePage(NginxBase):
    def get_module_menus(self):
        nginx_module_table_a = self.d("table").find("a")
        return [
            item.attr("href").replace("#", "") for item in nginx_module_table_a.items()
        ]

    def get_module_item_location(self):

        # 获取每个菜单指令的a标签，方便定位操作

        logger.info("获取每个菜单指令的a标签，方便定位操作")
        nginx_module_item = self.d("a").filter(
            lambda i, this: pq(this).attr("name") is not None
        )
        return nginx_module_item

    def get_module_variable_location(self):

        # 获取variables指令的a标签，方便定位操作
        logger.info("获取variables指令的a标签，方便定位操作")
        nginx_module_variable_info = self.d("a").filter(
            lambda i, this: pq(this).attr("name") == "variables"
        )
        return nginx_module_variable_info

    def get_variable_key_value(self, dl_html):
        var_list = []
        var_name_list = []
        dt_list = list(dl_html.children("dt").items())
        dd_list = list(dl_html.children("dd").items())
        for i in range(len(dt_list)):
            var_list.append(
                {"variable_name": dt_list[i].text(), "variable_desc": dd_list[i].text()}
            )
            var_name_list.append(dt_list[i].text())
        return var_list, var_name_list

    def get_module_variables(self, vars_location):
        vars_info = {"summary": ""}
        for item in vars_location.nextAll().items():
            if item.is_("center"):
                continue
            elif item.is_("p") and item.text():
                vars_info["summary"] += item.text()
            elif item.is_("dl"):
                vars_info["variables_info"], vars_info[
                    "var_names"
                ] = self.get_variable_key_value(item)
            elif is_menu_item(item):
                break

        return vars_info

    def common_menu_context_pickup(self, menu_location):
        available_label_list = []
        for item in menu_location.nextAll().items():
            if is_menu_item(item):
                break
            elif item.is_("center"):
                continue
            elif item.is_("blockquote"):
                code_content = item.text().split(";")
                available_label_list.append(";\n".join(code_content))
            else:
                available_label_list.append(item.text())
        return "".join(available_label_list)

    def common_direct_context_pickup(self, direct_location):
        available_label_list = []
        for item in direct_location.nextAll().items():
            if is_menu_item(item):
                break
            elif item.is_("center"):
                continue
            elif item.is_("blockquote"):
                code_content = item.text().split(";")
                available_label_list.append(";\n".join(code_content))
            else:
                available_label_list.append(item.text())
        return "".join(available_label_list)
