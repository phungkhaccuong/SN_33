import time

from elasticsearch.helpers import bulk

from conversationgenome.ConfigLib import c
from conversationgenome.conversation.ConvoLib import ConvoLib
from conversationgenome.llm.LlmLib import LlmLib
from conversationgenome.search.structured_search_engine import StructuredSearchEngine
from conversationgenome.utils.Utils import Utils
import bittensor as bt
import asyncio

index_name = "conversations"


def prepare_data(conversations):
    actions = []
    for conversation in conversations:
        lines = " ".join([f"[{line[0]}, '{line[1]}']" for line in conversation['lines']])
        print(f"lines:{lines}")
        action = {
            "_index": index_name,
            "_id": conversation['guid'],
            "_source": {
                "guid": conversation['guid'],
                "participants": conversation['participants'],
                "lines": lines,
                "tags": conversation.get('tags', None)  # Ensure 'tags' is included
            }
        }
        actions.append(action)
    return actions


def index_data_if_not_exists(es, conversation):
    doc_id = conversation['guid']
    try:
        lines = ",".join([f"[{line[0]}, '{line[1]}']" for line in conversation['full_lines']])
        print(f"lines:{lines}")
        if not es.exists(index=index_name, id=doc_id):
            es.index(index=index_name, id=doc_id, body={
                "guid": conversation['guid'],
                "participants": conversation['participants'],
                "lines": lines,  # conversation['lines'],  # Lines as a text string
                "tags": conversation.get('tags', None)  # Ensure 'tags' is included
            })
            print(f"Document with guid {doc_id} indexed successfully.")
        else:
            print(f"Document with guid {doc_id} already exists. Skipping indexing.")
    except Exception as e:
        print(f"Error indexing document with guid {doc_id}: {e}")


# Example data
data = [
    {'guid': 2029571757,
     'participants': ['"SPEAKER_01"', '"SPEAKER_00"'],
     'lines': [
         [0, 'The following is a conversation with Chris Urmson.'],
         [0,
          'He was the CTO of the Google self-driving car team, a key engineer and leader behind the Carnegie Mellon University autonomous vehicle entries in the DARPA Grand Challenges and the winner of the DARPA Urban Challenge.'],
         [0,
          'Today, he s the CEO of Aurora Innovation, an autonomous vehicle software company he started with Sterling Anderson, who was the former director of Tesla Autopilot, and Drew Bagnell, Uber s former autonomy and perception lead.'],
         [0,
          'Chris is one of the top roboticists and autonomous vehicle experts in the world, and a longtime voice of reason in a space that is shrouded in both mystery and hype.'],
         [0,
          'He both acknowledges the incredible challenges involved in solving the problem of autonomous driving and is working hard to solve it.'],
         [0, 'This is the Artificial Intelligence Podcast.']
     ],
     'tags': None
     }
]



def del_index(es):
    if es.indices.exists(index=index_name):
        # Delete the index
        es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted successfully.")
    else:
        print(f"Index '{index_name}' does not exist.")


async def getConvo():
    cl = ConvoLib()
    convo = await cl.get_conversation_v1(None)
    print(f"=================================================================START =============================================================")
    print(f"convo.line:{convo.get('lines')}")
    return convo


async def reserve_conversation(elastic):
    full_conversation = await getConvo()
    if full_conversation:
        conversation_guid = str(Utils.get(full_conversation, "guid"))
        num_lines = len(Utils.get(full_conversation, 'lines', []))
        bt.logging.info(
            f"Reserved conversation ID: {conversation_guid} with {num_lines} lines. Sending to {c.get('env', 'LLM_TYPE')} LLM...")

    # Do overview tagging and generate base participant profiles
    llml = LlmLib()
    result = await llml.conversation_to_metadata_v1(full_conversation)
    print(f"result:{result}")
    if not result:
        bt.logging.error(f"ERROR:2873226353. No conversation metadata returned. Aborting.")
        return None
    if not Utils.get(result, 'success'):
        bt.logging.error(f"ERROR:2873226354. Conversation metadata failed: {result}. Aborting.")
        return None

    full_conversation['tags'] = result['tags']
    print(
        f"=================================================================START1111111 =============================================================")
    print(f"convo.line:{full_conversation.get('tags')}")

    index_data_if_not_exists(elastic.es, full_conversation)





if __name__ == '__main__':
    elastic = StructuredSearchEngine()
    # Index the data
    while True:
        asyncio.run(reserve_conversation(elastic))
        time.sleep(10)
    # index_data_if_not_exists(elastic.es, data[0])
    #
    # # Define a search query for text field mapping
    # query = {
    #     "query": {
    #         "match": {
    #             "lines": "Intelligence Podcast"
    #         }
    #     }
    # }
    #
    # # Perform the search
    # response = elastic.es.search(index=index_name, body=query)
    # print(f"RESPONSE:{response}")
    # # Check if the index exists
