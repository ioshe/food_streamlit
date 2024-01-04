from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

client = Elasticsearch('http://localhost:9200')

# def search_index(index_name, field_name, match_name):
#     s = Search(index=index_name).using(client).query("match", fields=field_name, query=match_name)
#     print(s.to_dict())
#     response = s.execute()
#     return response

def search_index(index_name, field_name, match_name):
    query = Q("query_string", fields=[field_name], query="*"+match_name+"*")
    s = Search(index=index_name).using(client).query(query)
    s = s.source(['식품코드' ,'식품명', '에너지(kcal)', '수분(g)', '단백질(g)', '지방(g)', '탄수화물(g)', '당류(g)', '식이섬유(g)', '나트륨(mg)'])  # 필요한 필드만 지정
    print(s.to_dict())  
    response = s.execute()
    return response

def search_index_with_date_range(index_name, field_name, match_name, start_date, end_date):
    s = Search(index=index_name).using(client).query("multi_match", fields=field_name, query=match_name)
    s = s.filter('range', timestamp={'gte': start_date, 'lte': end_date})
    response = s.execute()
    return response

