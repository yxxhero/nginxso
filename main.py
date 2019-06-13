#!/usr/bin/env python3
from pyquery import PyQuery as pq

nginx_doc_url = "http://nginx.org/en/docs/"
d = pq(url=nginx_doc_url)
nginx_module_location = d("center").filter(lambda i, this: pq(this).children('h4').text() == 'Modules reference')
module_uris = [item.attr("href") for item in nginx_module_location.nextAll("ul").find("a").items()]
print(module_uris)
