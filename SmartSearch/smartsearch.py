import tensorflow_hub as hub
from elasticsearch import Elasticsearch

def embed_usi():
    return hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


# Returns a list of 512 elements that represents the semantics of string s
def get_sem_vector(s, e):
    return e([s])[0].numpy().tolist()


es = Elasticsearch()

embed = embed_usi()

query_vector = get_sem_vector("how to claim access point", embed)


res = es.search(index="test_index_4", body=
    { "query":
        {
            "script_score": {
                "query": {"match_all": {}}, "script": {
                    "source": "cosineSimilarity(params.query_vector, 'snippet_vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }
)

print(res["hits"]["hits"][0]["_source"]["url"])
