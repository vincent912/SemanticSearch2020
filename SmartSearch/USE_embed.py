import tensorflow_hub as hub
import json


def embed_use():
    return hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


# Adds the snippet_vector field to each entry in data
# Takes a json of scraped data, and interleaves it with:
# {"index":{}}
# On every other line so it can be loaded into elasticsearch with:
# curl -H "Content-Type: application/x-ndjson" -X POST http://localhost:9200/INDEX_NAME/_bulk --data-binary @FILENAME
# curl -H "Content-Type: application/x-ndjson" -X POST http://localhost:9200/test_index_6/_bulk --data-binary @items_es_ready.jl
def create_semantic_vectors(in_file, out_file):
    data = []

    with open(in_file) as f:
        for line in f:
            data.append(json.loads(line))

    embed = embed_use()
    o = open(out_file, "w")

    for i in range(len(data)):
        # title_and_snippet = data[i]["title"]
        # if data[i]["title"] is not "Null":
        #     title_and_snippet = data[i]["snippet"]
        data[i]["snippet_vector"] = embed([data[i]["snippet"]])[0].numpy().tolist()
        line = json.dumps(dict(data[i])) + "\n"
        o.write(line)

    o.close()


create_semantic_vectors("items_filtered.jl", "items_es_ready.jl")
