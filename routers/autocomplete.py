from fastapi import APIRouter
from utils.elasticsearch_helper import ElasticSearch
from utils.config import get_config
from utils.log_helper import logger

router = APIRouter()

@router.get("/", tags=["autocomplete"])
async def autocomplete(keyword : str = "allkeyword"):
    keyword_query_body = {
        "query": {
            "term": {
                "keyword": {
                    "value": keyword
                }
            }
        }
    }
    try:
        es_ins = ElasticSearch(ips=get_config("elasticsearch", "ips"), port=get_config("elasticsearch", "port"))

        keywords = es_ins.get_data_by_body(index_name="keyword", query_body=keyword_query_body)
    except Exception:
        logger.error(str(e))
        return {"error": 1, "msg": "内部错误,详情请看日志"}
    else:
        if keywords["hits"]["total"]["value"]:
            return {"code": 0, "data":keywords["hits"]["hits"][0]["_source"]["module_name"]}
        else:
            return {"code": 2, "data":[], "msg": "关键词列表为空"}

