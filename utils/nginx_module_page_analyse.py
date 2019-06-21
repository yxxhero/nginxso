from utils.nginx_module_page_helper import is_menu_item


def common_menu_context_pickup(menu_location):
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


def common_direct_context_pickup(direct_location):
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
