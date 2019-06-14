from pyquery import PyQuery as pq


def get_modules_menu(html):

    d = pq(html)
    nginx_module_content = d("table").find("a")
    return [item.attr("href").replace("#", '') for item in nginx_module_content.items()]


if __name__ == "__main__":
    print(get_modules_menu("http://nginx.org/en/docs/ngx_core_module.html"))
