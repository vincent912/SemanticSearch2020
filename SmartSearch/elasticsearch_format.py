import json

# Takes a json of scraped data, and interleaves it with:
# {"index":{}}
# On every other line so it can be loaded into elasticsearch with:
# curl -H "Content-Type: application/x-ndjson" -X POST http://localhost:9200/INDEX_NAME/_bulk --data-binary @FILENAME
# curl -H "Content-Type: application/x-ndjson" -X POST http://localhost:9200/test_index_5/_bulk --data-binary @FILENAME
def elasticsearchreadable(in_file, out_file):

    data = []
    with open(in_file) as f:
        for line in f:
            data.append(json.loads(line))

    o = open(out_file, 'w')

    for d in data:
        o.write("{\"index\":{}}\n")
        line = json.dumps(dict(d)) + "\n"
        o.write(line)


elasticsearchreadable("sem_title_w_snippet.jl", "es_output_title_w_snippet.jl")
