from pyquery import PyQuery as pq


def get_nginx_modules(html):

    d = pq(html)
    nginx_module_location = d("center").filter(lambda i, this: pq(
        this).children('h4').text() == 'Modules reference')
    return [item.attr("href") for item in nginx_module_location.nextAll("ul").find("a").items()]
