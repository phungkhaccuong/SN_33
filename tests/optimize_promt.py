import pytest
import random

from conversationgenome.ConfigLib import c
from conversationgenome.utils.Utils import Utils

from conversationgenome.validator.ValidatorLib import ValidatorLib
from conversationgenome.validator.evaluator import Evaluator
from conversationgenome.analytics.WandbLib import WandbLib
from conversationgenome.mock.MockBt import MockBt

verbose = True

bt = None
try:
    import bittensor as bt
except:
    if verbose:
        print("bittensor not installed")
    bt = MockBt()



class MockAxon:
    uuid = "a"
    hotkey = ""

class MockResponse:
    responses = {}
    responses = {}
    cgp_output = None
    axon = None

    def __init__(self):
        self.axon = MockAxon()


@pytest.mark.asyncio
async def test_full():
    wandb_enabled = Utils._int(c.get('env', 'WAND_ENABLED'), 1)
    if wandb_enabled:
        wl = WandbLib()
    # Config variables
    c.set('system', 'mode', 'test')

    batch_num = random.randint(100000, 9999999)

    vl = ValidatorLib()
    el = Evaluator()
    result = await vl.reserve_conversation_v1(batch_num=batch_num)
    (full_conversation, full_conversation_metadata, conversation_windows) = result
    print(f"full_conversation:::::{full_conversation}")
    print(f"//////////////////////////////////////////////////////////////////////////////////////////")
    print(f"full_conversation_metadata:::::{full_conversation_metadata}")
    print(f"//////////////////////////////////////////////////////////////////////////////////////////")
    for window_idx, conversation_window in enumerate(conversation_windows):
        print(f"window_idx::: {window_idx}")
        print(f"conversation_windows:::::{conversation_windows}")
