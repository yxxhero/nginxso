from pyquery import PyQuery as pq


def get_modules_content(html):

    d = pq(html)
    nginx_module_content = d("table").find("a")
    print(nginx_module_content)
    return [item.attr("href") for item in nginx_module_content.items()]


if __name__ == "__main__":
    print(get_modules_content("http://nginx.org/en/docs/ngx_core_module.html"))
