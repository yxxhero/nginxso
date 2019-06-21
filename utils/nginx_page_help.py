from pyquery import PyQuery as pq
from utils.tools import is_menu_item, get_menu_name


class NginxPage(object):

    def __init__(self, html):
        self.d = pq(html)

    def get_module_names(self):

        # 获取nginx的所有模块
        nginx_module_locations = self.d("center").filter(lambda i, this: pq(
            this).children('h4').text() == 'Modules reference')
        return [item.attr("href") for item in nginx_module_locations.nextAll("ul").find("a").items()]


class NginxModulePage(object):

    def __init__(self, html):
        self.d = pq(html)

    def get_module_menus(self):
        nginx_module_table_a = self.d("table").find("a")
        return [item.attr("href").replace("#", '') for item in nginx_module_table_a.items()]

