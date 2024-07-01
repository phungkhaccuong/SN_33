import asyncio
import time

import bittensor as bt

from conversationgenome.ConfigLib import c
from conversationgenome.conversation.ConvoLib import ConvoLib
from conversationgenome.llm.LlmLib import LlmLib
from conversationgenome.search.structured_search_engine import StructuredSearchEngine
from conversationgenome.utils.Utils import Utils

index_name = "conversations"


def index_data_if_not_exists(es, conversation):
    doc_id = conversation['guid']
    print(f"[index_data_if_not_exists] guid {doc_id} and tags:{conversation['tags']}")
    try:
        lines = ",".join([f"[{line[0]}, '{line[1]}']" for line in conversation['full_lines']])
        print(f"lines:{lines}")
        if not es.exists(index=index_name, id=doc_id):
            es.index(index=index_name, id=doc_id, body={
                "guid": conversation['guid'],
                "participants": conversation['participants'],
                "lines": lines,  # conversation['lines'],  # Lines as a text string
                "tags": conversation['tags']
            })
            print(f"Document with guid {doc_id} and tags:{conversation['tags']} indexed successfully.")
        else:
            print(f"Document with guid {doc_id} and tags:{conversation['tags']} already exists. Skipping indexing.")
    except Exception as e:
        print(f"Error indexing document with guid {doc_id}: {e}")


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
    return convo


async def index_conversation(elastic):
    try:
        full_conversation = await getConvo()
        if full_conversation is None:
            return

        conversation_guid = str(Utils.get(full_conversation, "guid"))
        num_lines = len(Utils.get(full_conversation, 'lines', []))
        bt.logging.info(
            f"Reserved conversation ID: {conversation_guid} with {num_lines} lines. Sending to {c.get('env', 'LLM_TYPE')} LLM...")

        llml = LlmLib()
        result = await llml.conversation_to_metadata_v1(full_conversation)
        if not result:
            bt.logging.error(f"ERROR:2873226353. No conversation metadata returned. Aborting.")
            return None
        if not Utils.get(result, 'success'):
            bt.logging.error(f"ERROR:2873226354. Conversation metadata failed: {result}. Aborting.")
            return None

        full_conversation['tags'] = result['tags']
        index_data_if_not_exists(elastic.es, full_conversation)
    except Exception as e:
        bt.logging.error(f"[index_conversation] - ERROR::: {e}")


if __name__ == '__main__':
    elastic = StructuredSearchEngine()
    del_index(elastic.es)
    while True:
        asyncio.run(index_conversation(elastic))
        time.sleep(1000)

    # Define a search query for text field mapping
    # query = {
    #     "query": {
    #         "match": {
    #             "lines": "[5, 'That s what you went for.']"
    #         }
    #     }
    # }
    #
    # # Perform the search
    # response = elastic.es.search(index=index_name, body=query)
    # print(f"RESPONSE:{response}")
    # # Check if the index exists
