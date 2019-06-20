from pyquery import PyQuery as pq


def get_nginx_modules(html):

    # 获取nginx的所有模块
    d = pq(html)
    nginx_module_location = d("center").filter(lambda i, this: pq(
        this).children('h4').text() == 'Modules reference')
    return [item.attr("href") for item in nginx_module_location.nextAll("ul").find("a").items()]


def get_nginx_module_item_location(html):

    # 获取每个菜单指令的a标签，方便定位操作
    d = pq(html)
    nginx_module_item = d("a").filter(
        lambda i, this: pq(this).attr("name") is not None)
    return nginx_module_item


def get_nginx_module_variable_location(html):

    d = pq(html)
    nginx_module_variable_info = d("a").filter(
        lambda i, this: pq(this).attr("name") == "variables")
    return nginx_module_variable_info


def get_variable_key_value(dl_html):
    var_list = []
    var_name_list = []
    dt_list = list(dl_html.children("dt").items())
    dd_list = list(dl_html.children("dd").items())
    for i in range(len(dt_list)):
        var_list.append({
            "variable_name": dt_list[i].text(),
            "variable_desc": dd_list[i].text()
        })
        var_name_list.append(dt_list[i].text())
    return var_list, var_name_list


def is_menu_item(html):
    if html.is_("a") and html.attr("name") is not None:
        return True
    return False


def get_menu_name(a_html):

    return a_html.attr("name")


def get_modules_variables(vars_location):
    vars_info = {
        "summary": ""
    }
    for item in vars_location.nextAll().items():
        if item.is_("center"):
            continue
        elif item.is_("p") and item.text():
            vars_info["summary"] += item.text()
        elif item.is_("dl"):
            vars_info["variables_info"], vars_info["var_names"] = get_variable_key_value(item)
        elif is_menu_item(item):
            break

    return vars_info
