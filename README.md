# Open-Domain Question Answering
> Boostcamp AI Tech 5기 Level 2 죠죠의 기묘한 모험

## Leader Board

<img src="https://img.shields.io/badge/Private-6th-green"/>

![image](https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/95160680/a3462e23-b732-4127-8f73-2e6b8d9e7856)




## Outline

: **Linking MRC and Retrieval**

![image](https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/95160680/1fe5ad53-d143-487d-a260-029c60343539)


- **ODQA:** 질의가 들어왔을 때 답변해 주는 질의응답 시스템으로 사전에 구축된 Knowledge Source에서 질의와 관련된 문서를 찾아주는 Retriever 단계와 전달된 문서를 읽고 적절한 답변을 찾거나 만들어 주는 Reader 단계로 구성된다.
- Query(input): 서울의 GDP는 세계 몇 위야?
→ Retriever Model → 질의와 관련된 A, B, C … 문서 → Reader Model →
Answer(output): 세계 4위입니다.

### A. 평가 지표

- 평가 지표로는 EM과 F1 Score가 있으며 주 지표로는 EM을 보조 지표로 F1 Score를 사용하였다.
- **Exact Match (EM)**: 모델의 예측과 실제 답이 정확하게 일치할 때만 점수를 준다. 즉 모든 질문은 0점 아니면 1점으로 처리된다. 실제 답이 두 개 이상일 경우 하나라도 일치하면 정답으로 간주한다.
- **F1 Score**: EM과 다르게 부분 점수를 제공한다. 예를 들어, 정답은 "Barack Obama"지만 예측이 "Barak Hussein Obama II"일 때, EM의 경우 0점을 받겠지만 F1 Score는 겹치는 단어를 고려해 부분 점수를 부여한다.

### B. 멤버

|전민수|조민우|조재관|진정민|홍지호|
|:-:|:-:|:-:|:-:|:-:|
|<img src='https://github.com/boostcampaitech5/level2_klue-nlp-11/assets/102800474/e1fd55d4-617a-436e-9ab0-e18eaeda685c' height=125 width=125></img>|<img src='https://github.com/boostcampaitech5/level2_klue-nlp-11/assets/102800474/1060e554-e822-4bac-9d7e-ddafdbf7d9c1' height=125 width=125></img>|<img src='https://github.com/boostcampaitech5/level2_klue-nlp-11/assets/102800474/5038030e-b30c-43e1-a930-3c63a1332843' height=125 width=125></img>|<img src='https://github.com/boostcampaitech5/level2_klue-nlp-11/assets/102800474/f871e7ea-7b41-494d-a858-2e6b2df815b9' height=125 width=125></img>|<img src='https://github.com/boostcampaitech5/level2_klue-nlp-11/assets/102800474/f5914167-bf44-40b6-8c78-964a8fb90b10' height=125 width=125></img>|
|[<img src='https://img.shields.io/badge/GitHub-181717?style&logo=github&logoColor=white' ></img>](https://github.com/line1029)|[<img src='https://img.shields.io/badge/GitHub-181717?style&logo=github&logoColor=white' ></img>](https://github.com/Minwoo0206)|[<img src='https://img.shields.io/badge/GitHub-181717?style&logo=github&logoColor=white' ></img>](https://github.com/jaekwanyda)|[<img src='https://img.shields.io/badge/GitHub-181717?style&logo=github&logoColor=white' ></img>](https://github.com/wjdals3406)|[<img src='https://img.shields.io/badge/GitHub-181717?style&logo=github&logoColor=white' ></img>](https://github.com/jiho-hong)|

### C. 역할

| 이름   | 역할  |
| --- | --- |
| 전민수 | Elasticsearch 서버 및 BM25 구현, Hard Negative Sampling |
| 조민우 | BM25+CE, Negative Sampling  |
| 조재관 | Negative Sampling, KorQuad 전처리 및 Fine-tuning |
| 진정민 | 실험 환경 세팅, Curriculum Learning 구현 및 Fine-tuning |
| 홍지호 | Elasticsearch 서버 및 BM25 구현, Fine-tuning 실험 |

### D. Skill

- PyTorch
- Hugging Face
- Elasticsearch

## Structure

```
level2_nlp_mrc-nlp-11
|-- README.md
|-- code
|   |-- arguments.py
|   |-- config.yaml
|   |-- curriculum_learning.py
|   |-- evaluation.py
|   |-- inference.py
|   |-- negative_sampling.py
|   |-- retrieval.py
|   |-- sweep.py
|   |-- sweep.yaml
|   |-- train.py
|   |-- trainer_qa.py
|   `-- utils_qa.py
|-- data
|-- elasticsearch
|   `-- README.md
`-- requirements.txt
```

- yaml 파일을 활용해 인자값을 변경한 후, 학습을 위해서는 train.py를, 평가 및 예측을 위해서는 inference.py를 실행시킨다.

## Data (EDA)

### A. **데이터 구성**

| 분류 | 세부 분류(샘플 수) | 용도 | 공개 여부 |
| --- | --- | --- | --- |
| train dataset | train(3952)<br> validation(240) | 학습용 | 모든 정보 공개<br>(id, question, context, answers, document_id, title) |
| test_dataset | public(240)<br> private(360) | 제출용 | id, question만 공개 |

### B. Context Length 분포

![image](https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/95160680/10f13527-7cbd-4189-9f13-589483bf0846)

### C. Question Length 분포

![image](https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/95160680/773b8ca9-71f1-40ab-addf-45787286ed2a)


### D. Answers Length 분포

![image](https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/95160680/db86e37c-2c59-4007-8b28-ac9025a2b78a)


## Retrieval Model

### A. Baseline: TF-IDF

- 여러 문서로 이루어진 문서 군이 있을 때 어떤 단어가 특정 문서 내에서 얼마나 중요한 것인지를 나타내는 수치
- TF-IDF는 TF와 IDF를 곱한 값으로 점수가 높은 단어일수록 다른 문서에는 많지 않고 해당 문서에서 자주 등장하는 단어를 의미한다.
- Term Frequency (TF): 단어의 빈도
- Inverse Document Frequency (IDF): 문서의 빈도의 역수

### B. Elasticsearch BM25

- [Elasticsearch](https://www.elastic.co/kr/elasticsearch/)란 Apache Lucene에 기반한 검색 및 분석 엔진으로, Okapi BM25, DFR 등의 유사도 점수 기반 검색 기능을 제공한다. 이 중 속도가 빠르고, 성능이 어느 정도 보장된 BM25를 사용했다.

- **BM25**
    - TF-IDF의 개념을 바탕으로, 문서의 길이까지 고려하여 점수화
    - TF 값에 한계를 지정해 두어 일정한 범위를 유지
    - 평균적인 문서의 길이보다 더 작은 문서에서 단어가 매칭된 경우 그 문서에 대해 가중치 부여

### C. Performance check

#### Hit@k

- k개의 검색 결과 중 Positive Passage가 존재할 경우 1, 아닌 경우 0으로 판단하여 계산한다.

![image](https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/95160680/21fb00ee-2ddd-472a-b07f-33ddcbd81777)

![image](https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/95160680/5415207f-469b-4958-ae87-6ed3de93b2e1)

## Reader Model

Reader 모델의 성능평가는 Retrieval 모델까지 이어 붙인 상태에서 진행되었으며, 하이퍼파라미터인 top-k는 10으로 고정하였다.

### A. Model Selection

다양한 모델로 실험을 진행한 결과 klue/roberta-large의 성능이 가장 좋아 해당 모델을 베이스 모델로 가져가게 되었다.

| 모델 | EM | F1 | Retrieval Model |
| --- | --- | --- | --- |
| klue/bert-base | 35.4200 | 48.4100 | TF-IDF |
| klue/roberta-large | 42.0800 | 53.1700 | TF-IDF |
| xlm-roberta-large | 35.4200 | 44.0600 | TF-IDF |
| monologg/koelectra-base-v3-finetuned-korquad | 37.5000 | 42.2600 | TF-IDF |

단일 모델만으로는 성능 향상의 한계가 있어서 다양한 방법의 학습 전략을 시도해 보았다. 

### B. Training Strategy

#### **1) KorQuad Fine-tuning**

- KorQuad 데이터를 통해 data augmentation 및 negative sampling을 하고자 하였다. KorQuad의 여러 버전 중 v1.0이 training dataset 의 구조와 비슷했기 때문에 v1.0을 선택하였다.
- 하지만 기존의 KLUE 데이터와 KorQuad를 병합해서 학습을 진행했을 때 오히려 성능이 떨어졌다.
    
    
    |  | EM(lb) | F1(lb) | retrieval |
    | --- | --- | --- | --- |
    | Baseline | 46.2505 | 55.3097 | BM25 |
    | Baseline(Augmentation) | 45.8333 | 53.7075 | BM25 |
- 떨어진 이유를 분석해 본 결과 두 데이터의 context 길이 분포가 많이 다르다는 것을 알 수 있었다.
    
  ![image](https://github.com/boostcampaitech5/level2_nlp_mrc-nlp-11/assets/95160680/2a3ff0bc-0cb4-4f8e-b311-409ff852e200)

    
- 그래서 생각해 낸 방법이 서로 분포가 다른 데이터를 순차적으로 학습 시켜주는 것이었다. 데이터의 양이 훨씬 많은 KorQuad로 1차 Fine-tuning을 거친 후 기존의 Train 데이터로 다시 Fine-tuning 해준다면 더 성능이 오를 것이라는 생각이 들었다.
    
    
    |  | EM | F1 | retrieval |
    | --- | --- | --- | --- |
    | Baseline(1차 finetuning) | 50.0 | 59.4816 | BM25 |
    | Baseline(2차 fientuning) | 56.25 | 64.7707 | BM25 |

#### 2) Curriculum Learning

- curriculum learning은 인간이 학습하는 프로세스를 모방하여 낮은 난이도의 데이터를 먼저 학습하고, 점차 어려운 데이터를 학습하는 학습 전략을 채택하여 모델의 학습 수렴 속도와 성능에서 성과를 보이는 연구 분야이다.
- 점진적으로 학습 난이도를 상향해 줌으로써 모델이 더 빠르게 정보를 습득할 수 있을 것이라는 기대감에 시도해 보았다.
- curriculum dataset 구축 및 학습
    - KLUE 데이터를 난이도별로 분류하기 위해서 KorQuad로 학습한 Reader 모델로 각 Train 데이터 샘플의 F1 Score를 평가하였다.
    - 데이터를 F1 Score에 따라 내림차순으로 정렬한 후 5개의 집합으로 분류하였다.
    - 낮은 난이도부터 높은 난이도의 데이터로 순차적으로 학습이 진행되도록 5개의 데이터 집합을 순차적으로 학습하였다.
        
        
        |  | EM | F1 |
        | --- | --- | --- |
        | 1차 KorQuad<br>2차 KLUE | 59.1667 | 67.1318 |
        | 1차 KorQuad<br>2차 Curriculum | 56.25 | 63.5327 |

#### 3) Negative Sampling

- DPR(Dense Passage Retrieval) 모델에서는 정답 문서와 유사하지만, 실제로는 정답이 존재하지 않는 다른 문서를 구별하기 위해서 Hard Negative Sampling을 사용해 검색 성능을 올렸다.
- 위 아이디어에서 착안해, Hard Negative Sampling을 Reader 모델에 다른 방식으로 적용해 보고자 했다. 이를 위해 정답 문서와 유사한 문서를 추출한 뒤 정답 데이터와 붙여 넣은 데이터를 학습 데이터로 활용하였다. 유사한 문서를 추출한 방법은 다음과 같다.
- KorQuad: 같은 title 내 다른 context들을 추출
- KLUE: BM25를 활용하여 20개의 hard negative context들을 추출
    
    
    |  | EM | F1 |
    | --- | --- | --- |
    | 1차: KorQuad<br>2차: KLUE<br>3차: KLUE(negative) | 63.3300 | 73.6100 |
    | 1차: KorQuad(negative) <br>2차: KLUE <br>3차: KLUE(negative) | 61.6667 | 70.4874 |

### C. Hyperparmeter Tuning

wandb의 sweep을 이용해 최적의 hyperparameter 탐색을 수행했다.

#### 1) Hyperparameter list

- learning rate
- epochs
- batch size
- warmup ratio

### D. Ensemble

모델 결과의 일반화 성능을 높이기 위해서 예측 답과 예측 답의 확률을 활용해서 hard voting 및 soft voting을 진행했다. 그중 soft voting의 리더보드 EM Score가 제일 높은 것으로 확인되었다.

## Result

리더보드 최종 결과

|  | EM | F1 |
| --- | --- | --- |
| Public Score | 67.0800 | 77.0000 |
| Private Score | 65.8300 | 77.8700 |

## 시도해 보려 했으나 하지 못했던 것

### A. BM25 + CE

- 논문 [BEIR(Takur et al., 2021)](https://arxiv.org/pdf/2104.08663.pdf)에 따르면 BM25에 Cross Encoder를 추가하여 Re-ranking을 진행했을 때 Retriever 모델의 성능이 가장 좋았다.
- 예를 들어, BM25에서 하나의 쿼리에 대해 $k_x$개의 문서를 추출한 뒤 Cross Encoder를 활용하여 Re-ranking을 진행한 후 최종적으로 $k_y\ \ (y < x)$개의 문서를 Reader Model에 전달한다.
- Cross Encoder의 Fine-tuning을 진행하기 전 BM25 + CE 모델의 Hit@k 성능이 BM25 단독 모델보다 낮았고, BM25 단독 모델의 성능이 높다고 판단되어 모델 정교화를 시도하지 않았다.

## 팀 회고

### A. 좋았던 점

- 모든 팀원이 각자 업무를 나누어서 진행하고 완료 후 다른 업무로 전환하는 과정이 자원의 손실 없이 잘 이루어졌다.
- 소스 코드와 저장소 관리가 잘 되었다. 시간이 조금 더 걸렸지만, 팀원이 함께 베이스라인 코드를 분석하고, 리팩토링을 거쳐 유지 보수가 용이하도록 하였다. 소스 코드에서 각자 맡은 부분을 수정하고 검증을 마친 부분을 공통으로 사용하는 저장소에 업데이트하면서 어려움 없이 최신 상태의 소스 코드로 실험할 수 있었다. 그 과정에서 서로의 코드를 리뷰하면서 버그를 찾아내며 완성도를 높여 나갔다.
- Pytorch 혹은 PytorchLightning을 통해 Train을 항상 진행하다가 처음으로 Huggingface를 통해 학습 및 추론을 진행하며 새로운 툴에 익숙해질 수 있었다. 또한, 모델을 정교화하는 시간을 통해 Huggingface의 trainer의 source code를 뜯어보며 이해할 수 있었다.

### B. 개선할 점

- 실험 결과 정리가 미흡하였다. 바쁘게 진행되는 프로젝트 동안 빨리 다음 단계로 나아가기 위해 결과 정리를 소홀히 하게 되어 시간이 불필요하게 소요되는 일이 있었다. 효율적인 결과 공유나 시간을 더 아끼기 위해서 정해진 포맷을 모든 팀원이 확인할 수 있도록 결과를 기록하는 과정이 필요하겠다.
- 실험 과정이나 소스 코드에서 발생한 이슈가 적절하게 공유되지 못했던 부분이 있었다. 업무를 분담하여 진행하다 보니 담당 팀원을 제외하고는 즉각적으로 이슈를 인지하기 어려웠다. 협업 도구의 효과적인 활용이나 상세한 주석, 커밋 메시지 등의 기본적인 부분에 더 노력을 기울여야 하겠다.
- 시간 분배에 있어 더 철저한 계획이 필요할 것 같다. Dense Retrieval Model, ODQA Task의 다른 SOTA모델 구현 등 해보고 싶은 계획이 많았는데 실행하지 못한 계획이 많았다. 프로젝트 로드맵이나 대략적인 시간 계획을 미리 세워 프로젝트를 진행해 보면 좋을 것 같다.

## Reference

[1] Bengio, Y., Louradour, J., Collobert, R., & Weston, J. (2009, June). Curriculum learning. In Proceedings of the 26th annual international conference on machine learning

[2] Kedia, A., Zaidi, M. A., & Lee, H. (2022). FiE: Building a Global Probability Space by Leveraging Early Fusion in Encoder for Open-Domain Question Answering. *arXiv preprint arXiv:2211.10147*.

[3] Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., & Gurevych, I. (2021). BEIR: A heterogenous benchmark for zero-shot evaluation of information retrieval models. *arXiv preprint arXiv:2104.08663*.

