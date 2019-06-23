import requests
import os
from utils.log_helper import logger
from utils.config import get_config


def is_menu_item(html):
    if html.is_("a") and html.attr("name") is not None:
        return True
    return False


def get_menu_name(a_html):
    return a_html.attr("name")


def get_request_text(url, timeout):
    r = requests.get(url, timeout=timeout)
    logger.info("get url: {} successfully...".format(url))
    return r.text


def generate_prefix(prefix):
    return os.path.join(get_config("common", "baseprefix"), prefix)

