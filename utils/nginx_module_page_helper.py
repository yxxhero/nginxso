from pyquery import PyQuery as pq


def get_nginx_modules(html):

    d = pq(html)
    nginx_module_location = d("center").filter(lambda i, this: pq(
        this).children('h4').text() == 'Modules reference')
    return [item.attr("href") for item in nginx_module_location.nextAll("ul").find("a").items()]


def get_nginx_module_item(html):

    d = pq(html)
    nginx_module_item = d("a").filter(
        lambda i, this: pq(this).attr("name") is not None)
    return nginx_module_item


def get_nginx_module_variable_info(html):

    d = pq(html)
    nginx_module_variable_info = d("a").filter(
        lambda i, this: pq(this).attr("name") == "variables")
    return nginx_module_variable_info


def get_variable_key_value(dl_html):
    vars_list = []
    dt_list = list(dl_html.children("dt").items())
    dd_list = list(dl_html.children("dd").items())
    for i in range(len(dt_list)):
        vars_list.append({
            "variable_name": dt_list[i].text(),
            "variable_desc": dd_list[i].text()
        })
    return vars_list


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
            vars_info["variables"] = get_variable_key_value(item)
    return vars_info
