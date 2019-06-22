import requests

def is_menu_item(html):
    if html.is_("a") and html.attr("name") is not None:
        return True
    return False


def get_menu_name(a_html):
    return a_html.attr("name")


def get_request_text(url, timeout):
    r = requests.get(url, timeout=timeout)
    return r.text

