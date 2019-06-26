from fastapi import APIRouter
from utils.elasticsearch_helper import ElasticSearch
from utils.config import get_config
from utils.log_helper import logger
import traceback

router = APIRouter()


@router.get("/", tags=["autocomplete"])
async def autocomplete(keyword: str):
    keyword_query_body = {
        "size": 10000,
        "query": {"wildcard": {"keyword": "".join(["*", keyword, "*"])}},
    }
    try:
        es_ins = ElasticSearch(
            ips=get_config("elasticsearch", "ips"),
            port=get_config("elasticsearch", "port"),
        )

        keywords = es_ins.get_data_by_body(
            index_name="keyword", query_body=keyword_query_body
        )
    except Exception:
        logger.error(traceback.format_exc())
        return {"error": 1, "msg": "内部错误,详情请看日志"}
    else:
        if keywords["hits"]["total"]["value"]:
            return {
                "code": 0,
                "data": [
                    item["_source"]["keyword"] for item in keywords["hits"]["hits"]
                ],
            }
        else:
            return {"code": 2, "data": [], "msg": "关键词列表为空"}
