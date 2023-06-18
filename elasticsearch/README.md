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


## 3. Elasticsearch snapshot

### 1) 개요

- `BM25`방식이 rule-based기 때문에 각자의 서버에서 Elasticsearch 데이터베이스를 만들어도 결과물이 같겠지만, 혹시 모를 상황을 대비해 원본 데이터의 snapshot을 만들어 각 서버에 배포 / snapshot 복원 방법을 정리

### 2) snapshot 생성
- 원본 데이터가 있는 서버에서 진행

#### a. snapshot을 저장할 repository 생성

##### a) repository 경로 추가

```bash
code /etc/elasticsearch/elasticsearch.yml
```

```yaml
# 마지막 줄에 아래 코드 추가
# MY_DIRECTORY = repository를 사용할 디렉터리
path.repo: ["MY_DIRECTORY/elasticsearch/backup"]
```

##### b) 해당 경로에 repository 디렉터리 생성, 수정 권한 변경

```bash
# repository를 사용할 디렉터리로 이동 후,
mkdir elasticsearch
cd elasticsearch
mkdir backup
# MY_DIRECTORY = repository를 사용할 디렉터리
chmod 777 MY_DIRECTORY/elasticsearch MY_DIRECTORY/elasticsearch/backup
```

##### c) Elasticsearch 서버 재시작

```bash
service elasticsearch restart
```

#### b. 백업 repository 등록

##### a) 등록

```bash
# MY_DIRECTORY = repository를 사용할 디렉터리
curl -X PUT "http://localhost:9200/_snapshot/my_backup?pretty" -H 'Content-Type: application/json' -d'
{
 "type": "fs",
 "settings": {
   "location": "MY_DIRECTORY/elasticsearch/backup",
    "compress": true
 }
}'
```

##### b) 확인

```bash
curl -X GET "http://localhost:9200/_snapshot/_all?pretty"
```

#### c. snapshot을 생성할 인덱스 확인

```bash
curl -X GET "http://localhost:9200/_cat/indices"
```

<details>
<summary>확인</summary>

<img width="544" alt="image" src="https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/102800474/71c51bc6-9ca8-4132-a70e-d127b0ca799f">

- 3번째 인자('wiki')가 인덱스 이름

</details>

#### d. snapshot 생성

##### a) 생성
```bash
curl -X PUT "http://localhost:9200/_snapshot/my_backup/MY_SNAPSHOT_NAME?wait_for_completion=true" -H 'Content-Type: application/json' -d'
{
  "indices": "MY_INDEX_NAME",
  "include_global_state": true
}
'
```
- `MY_SNAPSHOT_NAME`에 생성할 snapshot의 이름을 넣기
- `MY_INDEX_NAME`에 생성할 snapshot의 인덱스 이름을 넣기

##### b) 확인

<details>
<summary>아래와 같은 형태로 파일이 생성되었다면 성공</summary>

<img width="401" alt="image" src="https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/102800474/79f5243f-e3da-4b72-af8e-545c5c6d7779">

</details>

- 해당 폴더를 압축하여 snapshot을 불러올 서버로 전송

### 3) snapshot 불러오기
- snapshot을 사용할 서버에서 진행

#### a. snapshot을 불러올 repository 생성

##### a) repository 경로 추가

```bash
code /etc/elasticsearch/elasticsearch.yml
```

```yaml
# 마지막 줄에 아래 코드 추가
# MY_DIRECTORY = repository를 사용할 경로
path.repo: ["MY_DIRECTORY/elasticsearch/backup"]
```

##### b) 해당 경로에 repository 디렉터리 생성, 수정 권한 변경

```bash
# repository를 사용할 디렉터리로 이동 후,
mkdir elasticsearch
cd elasticsearch
mkdir backup
# MY_DIRECTORY = repository를 사용할 디렉터리
chmod 777 MY_DIRECTORY/elasticsearch MY_DIRECTORY/elasticsearch/backup
```

##### c) backup 디렉터리 안에 전송된 snapshot 데이터 압축 풀기

<details>
<summary>확인</summary>

<img width="401" alt="image" src="https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/102800474/79f5243f-e3da-4b72-af8e-545c5c6d7779">

</details>

##### d) Elasticsearch 서버 재시작

```bash
service elasticsearch restart
```

#### b. 백업 repository 등록

##### a) 등록
```bash
curl -X PUT "http://localhost:9200/_snapshot/my_backup?pretty" -H 'Content-Type: application/json' -d'
{
 "type": "fs",
 "settings": {
   "location": "/opt/ml/elasticsearch/backup",
    "compress": true
 }
}'
```

##### b) 확인

```bash
# my_backup repository가 등록되었는지 확인
curl -X GET "http://localhost:9200/_snapshot/_all?pretty"
```

#### c. snapshot 복원

##### a) snapshot 확인

```bash
curl -X GET "http://localhost:9200/_snapshot/my_backup/_all?pretty"
```

<details>
<summary>확인</summary>

<img width="698" alt="image" src="https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/102800474/4ec70f06-8b9d-48ae-b2d4-b433e9765184">

</details>

##### b) snapshot 복원

```bash
# MY_SNAPSHOT_NAME = 복원할 snapshot의 이름
# MY_INDEX_NAME =  복원할 snapshot의 인덱스 이름
curl -XPOST "http://localhost:9200/_snapshot/my_backup/MY_SNAPSHOT_NAME/_restore" -H 'Content-Type: application/json' -d'
{
 "indices": "MY_INDEX_NAME",
 "include_global_state": true
}'
```

<details>
<summary>인덱스 삭제</summary>

- 해당 클러스터에 같은 이름의 인덱스가 존재할 경우 불러와지지 않음
- 클러스터 내 인덱스를 삭제 후 복원하기

```bash
# 삭제
curl -X DELETE "http://localhost:9200/MY_INDEX_NAME"

# 확인
curl -X DELETE "http://localhost:9200/MY_INDEX_NAME"
```

</details>

##### c) 인덱스 확인

```bash
curl -X GET "http://localhost:9200/_cat/indices?pretty"
```

### reference

- https://kay0426.tistory.com/46
- https://gh402.tistory.com/51
