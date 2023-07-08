import json
import os
import pandas as pd
from datasets import load_dataset, load_from_disk, concatenate_datasets, Dataset, DatasetDict
import random
from tqdm.auto import tqdm
from typing import List, Optional, Tuple
from elasticsearch import Elasticsearch


def get_relevant_doc_es(query: str, k: Optional[int] = 1, client: Optional[Elasticsearch] = None) -> Tuple[List]:
    """
    Arguments:
        query (str):
            하나의 Query를 받습니다.
        k (Optional[int]): 1
            상위 몇 개의 Passage를 반환할지 정합니다.
    """

    q = {"match": {"text": query}}
    response = client.search(index="wiki", query=q, size=k)

    doc_score = [i['_score'] for i in response['hits']['hits']]
    doc_texts = [i['_source']['text'] for i in response['hits']['hits']]
    doc_ids = [int(i["_id"]) for i in response['hits']['hits']]
    return doc_score, doc_texts, doc_ids


def is_right_answer(dataset):
    context = dataset['context']
    answers = dataset['answers']
    return all(i[j['answer_start'][0]:j['answer_start'][0] + len(j['text'][0])] == j['text'][0] for i, j in zip(context, answers))


def add_wiki_id_to_data():
    dataset = load_from_disk('../data/train_dataset')
    ids = make_wiki_ids()
    def change_document_id(example):
        example['document_id'] = ids[example['document_id']]
    dataset = dataset.map(change_document_id)
    dataset.save_to_disk("../data/train_dataset_2")
    print("wiki id 수정 완료")


def make_wiki_ids():
    dataset_path = "../data/wikipedia_documents.json"
    assert os.path.exists("../data/wikipedia_documents.json"), "원본 WikiPedia 데이터 필요"
    with open(dataset_path, "r") as f:
        wiki = json.load(f)
    wiki_sets = {}
    wiki_ids = []
    for v in wiki.values():
        if v['text'] in wiki_sets:
            wiki_ids.append(wiki_sets[v['text']])
        else:
            wiki_sets[v['text']] = len(wiki_ids)
            wiki_ids.append(len(wiki_ids))
    return wiki_ids


def negative_sampling(source_data='KorQuad'):
    data = load_from_disk('../data/train_dataset')
    if source_data == 'KorQuad':
        aug_data = load_dataset('KETI-AIR/korquad','v1.0')
        aug_data_concat = concatenate_datasets([aug_data["train"].flatten_indices(), aug_data["dev"].flatten_indices()])
        val = data['validation'].remove_columns(["document_id", "__index_level_0__"])
        new_features = val.features.copy()
        aug_data_concat = aug_data_concat.cast(new_features)
        data = DatasetDict({"train":aug_data_concat, "validation":val})

    df = pd.DataFrame(data['train'])
    negative_sampled = pd.DataFrame(data['train'])

    unique_title = df['title'].unique()
    for title in tqdm(unique_title, desc="negative sampling"):
        possi_df = df[df['title'] == title] #title이 같은 곳에서 변경
        unique_context = possi_df['context'].unique()
        if len(unique_context) >= 2: # unique 개수가 2 이상일 때 진행
            for pos, start, id in zip(possi_df['context'], possi_df['answers'], possi_df['id']):
                false_list = []
                for context in unique_context: #각각의 context에 대해 진행
                    if context != pos:
                        false_list.append(context)
                #2개 뽑아오기
                chosen_false = random.sample(false_list, min(2, len(false_list)))
                for i, v in enumerate(chosen_false):
                    r = random.randint(1,2) #랜덤하게 수 지정하기
                    s = 0
                    # 11 -> FFT, 12 -> FTF, 21 -> FTF, 22 -> TFF
                    if r == 1:
                        pos = v + pos
                        s = s + len(v)
                    else: #TF
                        pos = pos + v
                negative_sampled.loc[negative_sampled['id']==id, 'context'] = pos
                negative_sampled[negative_sampled['id']==id].iloc[0, 4]['answer_start'] = [x+s for x in start['answer_start']]
    dataset = Dataset.from_pandas(negative_sampled)
    dataset.save_to_disk(f'../data/negative_sampled_{source_data}')
    print('저장 완료')
    print(f'저장 경로: ../data/negative_sampled_{source_data}')


def negative_sampling_hard(client=None):
    assert os.path.exists("../data/train_dataset"), "원본 데이터 필요"
    if not os.path.exists("../data/train_dataset_2"):
        add_wiki_id_to_data()
    dataset = load_from_disk('../data/train_dataset_2')
    assert isinstance(client, Elasticsearch), "적절한 Elasticsearch client가 필요합니다."
    assert client.ping(), "Elasticsearch client 연결 불가"
    def add_negative(example):
        _, doc_texts, doc_ids = get_relevant_doc_es(example['question'], 20, client)
        if example['document_id'] in doc_ids:
            idx = doc_ids.index(example['document_id'])
            doc_texts[idx] = example['context']
        else:
            doc_texts.append(example['context'])
            idx = len(doc_ids)
        doc_len = [len(text) + 1 for text in doc_texts[:idx]]
        offset = sum(doc_len)
        example['context'] = " ".join(doc_texts)
        example['answers']['answer_start'][0] += offset
        return example
    
    dataset = dataset.map(add_negative)
    dataset.save_to_disk("../data/klue_hard_negative_dataset")
    print("hard negative spampled data 저장 완료")
    print("저장 경로: ../data/klue_hard_negative_dataset")



if __name__ == '__main__':
    negative_sampling('KorQuad')
    es = Elasticsearch("http://localhost:9200")
    negative_sampling_hard(es)
