from utils.config import get_config
from utils.elasticsearch_helper import ElasticSearch

if __name__ == "__main__":
    es_ins = ElasticSearch(get_config("elasticsearch", "ips"), port=get_config("elasticsearch", "port"))
    es_ins.delete_index("keyword")
    es_ins.delete_index("module")
