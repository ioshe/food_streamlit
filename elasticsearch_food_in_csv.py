import pandas as pd
from elasticsearch import Elasticsearch
def index_csv_to_elasticsearch(csv_file, index_name):
    # CSV 파일을 DataFrame으로 읽기 (NaN 값은 None으로 처리)
    df = pd.read_csv(csv_file, encoding='euc-kr', na_filter=True)
    # Elasticsearch 서버에 연결
    es = Elasticsearch("http://localhost:9200")
    # Elasticsearch에 인덱스 생성 (이미 존재하는 경우 덮어쓰기를 방지)
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
    # DataFrame의 각 행을 순회하며 Elasticsearch에 색인
    for _, row in df.iterrows():
        # NaN 값을 None으로 변환
        doc = row.where(pd.notnull(row), None).to_dict()
        es.index(index=index_name, document=doc)
# 사용 예시
index_csv_to_elasticsearch(r'C:\ITStudy\03_ELK\python-elk\food\전국통합식품영양성분정보(음식)표준데이터.csv', 'food_index')