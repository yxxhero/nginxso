# nginxso
nginx direct search by python3 

# nginx模块页面结构:
## 1.导航类型
* summary
* issues
* example
* directives
* variables

# es config
--- 
https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html 

# docker config
--- 
```shell
docker run -d --name elasticsearch --net=host -e "discovery.type=single-node" -e "http.cors.enabled=true" -e "http.cors.allow-origin=*" -e "http.cors.allow-headers=X-Requested-With,X-Auth-Token,Content-Type,Content-Length,Authorization" -e "http.cors.allow-credentials=true" docker.elastic.co/elasticsearch/elasticsearch-oss:7.1.1
```
