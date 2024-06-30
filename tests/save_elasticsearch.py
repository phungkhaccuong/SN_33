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
    {'guid': 2029571757,
     'participants': ['"SPEAKER_01"', '"SPEAKER_00"'],
     'lines': [
         [0, 'The following is a conversation with Chris Urmson.'],
         [0, 'He was the CTO of the Google self-driving car team, a key engineer and leader behind the Carnegie Mellon University autonomous vehicle entries in the DARPA Grand Challenges and the winner of the DARPA Urban Challenge.'], [0, 'Today, he s the CEO of Aurora Innovation, an autonomous vehicle software company he started with Sterling Anderson, who was the former director of Tesla Autopilot, and Drew Bagnell, Uber s former autonomy and perception lead.'],
         [0, 'Chris is one of the top roboticists and autonomous vehicle experts in the world, and a longtime voice of reason in a space that is shrouded in both mystery and hype.'],
         [0, 'He both acknowledges the incredible challenges involved in solving the problem of autonomous driving and is working hard to solve it.'],
         [0, 'This is the Artificial Intelligence Podcast.'],
         [0, 'If you enjoy it, subscribe on YouTube, give it five stars on iTunes, support it on Patreon, or simply connect with me on Twitter at LexFriedman, spelled F-R-I-D-M-A-N.'],
         [0, 'And now, here s my conversation with Chris Armisen.'],
         [0, 'You were part of both the DARPA Grand Challenge and the DARPA Urban Challenge teams at CMU with Red Whitaker.'],
         [0, 'What technical or philosophical things have you learned from these races?'],
         [1, 'I think the high order bit was that it could be done.'],
         [1, 'I think that was the thing that was incredible about the first, the Grand Challenges.'],
         [1, 'that I remember you know I was a grad student at Carnegie Mellon and there we it was kind of this dichotomy of'],
         [1, 'It seemed really hard, so that would be cool and interesting.'],
         [1, 'But at the time, we were the only robotics institute around.'],
         [1, 'And so if we went into it and fell on our faces, that would be embarrassing.']
            ]
     }
]

if __name__ == '__main__':
    elastic = StructuredSearchEngine()
    # Index the data
    # bulk(elastic.es, prepare_text_data(data))
    #
    # # Define a search query for text field mapping
    # query = {
    #     "query": {
    #         "match": {
    #             "lines": "there we it was kind of this dichotomy of"
    #         }
    #     }
    # }
    #
    # # Perform the search
    # response = elastic.es.search(index=index_name, body=query)
    # print(f"RESPONSE:{response}")
    # Check if the index exists
    if elastic.es.indices.exists(index=index_name):
        # Delete the index
        elastic.es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted successfully.")
    else:
        print(f"Index '{index_name}' does not exist.")
