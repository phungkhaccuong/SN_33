from elasticsearch.helpers import bulk

from conversationgenome.search.structured_search_engine import StructuredSearchEngine

index_name = "conversations"

# Function to prepare data
def prepare_text_data(conversations):
    actions = []
    for conversation in conversations:
        lines = " ".join([f"[{line[0]}, '{line[1]}']" for line in conversation['lines']])
        action = {
            "_index": index_name,
            "_source": {
                "guid": conversation['guid'],
                "participants": conversation['participants'],
                "lines": lines
            }
        }
        actions.append(action)
    return actions


# Example data
data = [
    {
        'guid': 2293692782,
        'participants': ['"SPEAKER_00"', '"SPEAKER_02"', '"SPEAKER_01"', '"None"'],
        'lines': [
            [0, 'Let s get it on!'],
            [0,'Welcome back to New Heights, ladies and gentlemen, presented by Wayne Sports and- You re the one that s going to have to bring the energy today.'],
            [1, 'I want to go to a dark room and not have to interact with anybody for three days.'],
            [0, 'Welcome back to New Heights, presented by Wayne Sports and Entertainment and- We need more energy.'],
            [1, 'Come on, you re in the playoffs still.'],
            [1, 'I need more.'],
            [1, 'You re going to be good cop, I m bad cop today.'],
            [0, 'Good cop, good cop.'],
            [0, 'I m the good cop.'],
            [0, 'I know, that s what I m saying.'],
            [0, 'Hey, I just did my first desk pop.'],
            [0,
             'Welcome back to New Heights, ladies and gentlemen, presented by Wave Sports and Entertainment and brought to you by the all new Experience Smart Money Debit Card, the debit card that builds credit without the debt.'],
            [0, 'That s right.']
        ]
    }
]

if __name__ == '__main__':
    elastic = StructuredSearchEngine()
    # Index the data
    bulk(elastic.es, prepare_text_data(data))

    # Define a search query for text field mapping
    query = {
        "query": {
            "match": {
                "lines": "[0, 'I m the good cop.']"
            }
        }
    }

    # Perform the search
    response = elastic.es.search(index=index_name, body=query)

    # response = elastic.es.search(
    #     index=index_name,
    #     body={
    #         "query": {
    #             "match_all": {}
    #         }
    #     },
    #     scroll='2m',  # keep the search context alive for 2 minutes
    #     size=1000  # number of documents to return in each batch
    # )
    print(f"RESPONSE:{response}")
