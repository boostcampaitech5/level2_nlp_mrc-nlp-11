# Elasticsearch

## 1. Elasticsearch 설치

### 0) root 계정으로 전환

```bash
su -
```

### 1) sudo, gpg 설치

```bash
# apt-get 업데이트
apt-get update

# sudo 설치
apt-get install sudo

# gph 설치
sudo apt-get install gpg
```

### 2) 자바 설치

#### a. 설치

```bash
# 자바 설치
sudo apt-get install openjdk-8-jdk

# 자바 설치 확인
java -version
javac -version
```

#### b. 환경 변수 설정

```bash
# ./profile 실행
code ~/.profile
```

```bash
# 아래 내용 추가
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
export PATH=$PATH:$JAVA_HOME/bin
```

```bash
# .profile 적용
source ~/.profile

# 환경 변수 확인
echo $JAVA_HOME
```

### 3) Elasticsearch 설치

```bash
# Elasticsearch public GPG 키 추가
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

# 소스 리스트 추가
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

# apt 업데이트
sudo apt update

# Elasticsearch 설치
sudo apt install elasticsearch
```

### 4) Elasticsearch 설정

#### a. network host 수정

```bash
code /etc/elasticsearch/elasticsearch.yml
```

```yaml
# network.host: 192.168.0.1 ->
network.host: localhost
```

### 5) Elasticsearch 업데이트

```bash
# 실행 여부 확인
service elasticsearch start

# 실행 완료 -> 서버 중지
service elasticsearch stop

# sudo apt-get install apt-transport-https
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt-get update && sudo apt-get install elasticsearch

# 실행 여부 확인 -> 정상 실행까지 반복
service elasticsearch start
service elasticsearch start
# ...
```

### 6) security 설정 변경

```bash
code /etc/elasticsearch/elasticsearch.yml
```

```yaml
# 가장 아래 2줄 추가 -> security 제거
xpack.security.transport.ssl.enabled: false
xpack.security.enabled: false
```

```bash
service elasticsearch restart
```

### 7) plugin 설치

```bash
# Korean (nori) analysis plugin
sudo bin/elasticsearch-plugin install analysis-nori
```

### reference

- https://pinggoopark.tistory.com/54
- https://backendcode.tistory.com/262
- https://leftday.tistory.com/94
- https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-nori.html#analysis-nori-install


## 2. Elasticsearch Python Client

### 1) 사전작업

#### a. `elasticsearch` 연결 확인

```bash
curl -XGET localhost:9200
```

#### b. `elasticsearch` 패키지 설치

```bash
# jupyter 깔고 vscode 확장 프로그램도 설치할 것
pip install jupyter
pip install elasticsearch
```

#### c. `charset-normalizer` 설치

```bash
!pip install -U --force-reinstall charset-normalizer
```

### 2) Python Client 연결

#### a. 필요한 라이브러리 불러오기

```python
from tqdm import tqdm
import json
from pprint import pprint
from elasticsearch import Elasticsearch
```

#### b. 클라이언트 연결

```python
try:
    es.transport.close()
except:
    pass
es = Elasticsearch("http://localhost:9200")
```

#### c. 연결 확인

```python
# should be True
es.ping()
```

```python
# ObjectApiResponse
es.info()
```

### (Optional) Wikipedia 데이터로 Elasticsearch Indexing

#### a. 검색 말뭉치 이름, 인덱싱 방식 지정

```python
INDEX_NAME = "wiki"

INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "filter": {
                "my_shingle": {
                    "type": "shingle"
                }
            },
            "analyzer": {
                "my_analyzer": {
                    "type": "custom",
                    "tokenizer": "nori_tokenizer",
                    "decompound_mode": "mixed",
                    "filter": ["my_shingle"]
                }
            },
            "similairty": {
                "my_similarity": {
                    "type": "BM25"
                }
            }
        }
    },

    "mappings": {
        "properties": {
            "text": {
                "type": "text",
                "analyzer": "my_analyzer"
            }
        }
    }
} 

es.indices.create(index=INDEX_NAME, body=INDEX_SETTINGS)
```

#### b. 위키 데이터 불러오기

```python
dataset_path = "./data/wikipedia_documents.json"
with open(dataset_path, "r") as f:
    wiki = json.load(f)
    
print(len(wiki))
print(type(wiki))
```

```python
wiki_texts = [{"text":text} for text in list(dict.fromkeys(v["text"] for v in wiki.values()))]
```

- 전처리 수행 가능(개행문자, 공백문자 치환, 문서 제목 넣기 등)

#### c. Indexing

```python
# 10분 정도 소요
for i, text in enumerate(tqdm(wiki_texts)):
    try:
        es.index(index=INDEX_NAME, id=i, document=text)
    except Exception as e:
        print(e)
        print(f"Unable to load document {i}.")
```

```python
# 문서 id로 반환 가능한지 확인
es.get(index=INDEX_NAME, id=0)
```

```python
# analyze 메서드로 입력 쿼리, 문서의 토큰화 확인 가능
es.indices.analyze(index=INDEX_NAME, analyzer="my_analyzer", text="백남준이 태어난 해가 언제야?",)
```

### 3) 검색

```python
query = {
    "match": {"text" : "마오리언어와 영어, 뉴질랜드 수화를 공식 언어로 사용하는 나라는?"}
}
topk = 5
response = es.search(index=INDEX_NAME, query=query, size=5)
```

```python
# 검색된 목록 반환
response['hits']
```

### reference

- https://github.com/thejungwon/search-engine-tutorial
