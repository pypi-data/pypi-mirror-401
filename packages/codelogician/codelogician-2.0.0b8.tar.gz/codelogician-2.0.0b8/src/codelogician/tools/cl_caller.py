#
#   Imandra Inc.
#
#   cl_caller.py
#

import asyncio
from typing import Any

import dotenv
from imandra.u.agents import create_thread_sync, get_remote_graph
from imandra.u.agents.code_logician.command import (
    AgentFormalizerCommand,
    Command,
    EmbedCommand,
    GenFormalizationDataCommand,
    GenModelCommand,
    GenRegionDecompsCommand,
    GenVgsCommand,
    InitStateCommand,
)
from imandra.u.agents.code_logician.graph import GraphState

from codelogician.strategy.cl_agent_state import CLAgentState
from codelogician.util import get_imandra_uni_key, maybe

dotenv.load_dotenv('.env')


async def call_cl_agent(src_code: str, language: str, artifacts: bool = True):
    """
    src_code - source code we'll send to the agent
    language - programming language we should use
    artifacts - should we generate VGs/Decomps from the requests
    """

    graph = get_remote_graph('code_logician', api_key=get_imandra_uni_key())
    create_thread_sync(graph)

    gs = GraphState()

    #
    commands: list[Command] = [
        # Will initialize the state with specified Python source program
        InitStateCommand(src_code=src_code, src_lang=language),
        # Will gather relevant formalization data (required to create the model)
        AgentFormalizerCommand(
            no_gen_model_hitl=True,
            max_tries_wo_hitl=3,
            max_tries=3,
            no_check_formalization_hitl=True,
            no_refactor=False,
        ),
    ]

    # Create a list of commands for CL to execute
    if artifacts:
        more_commands = [GenVgsCommand(), GenRegionDecompsCommand()]
        commands.extend(more_commands)

    gs = gs.add_commands(commands)

    progress: dict[str, str] | None = None
    result: tuple[GraphState, dict[str, Any] | None] | None = None
    async for item in gs.stream(graph):
        if isinstance(item, dict):
            progress = item
            print(f'Currently running: {progress["step_name"]}')
        elif isinstance(item, tuple):
            result = item

    assert result is not None
    assert progress is not None

    gs: GraphState
    gs, _ = result

    return gs.last_fstate


def cl_autoformalize(src_code: str):
    """
    Return the object containing results of running CodeLogician agent
    """

    def mk_agent_state(f):
        return CLAgentState(
            status=f.status,
            src_code=f.src_code,
            iml_code=f.iml_code,
            vgs=f.vgs,
            region_decomps=f.region_decomps,
            opaque_funcs=f.opaque_funcs,
        )

    graph = get_remote_graph('code_logician', api_key=get_imandra_uni_key())
    create_thread_sync(graph)

    gs = GraphState()

    # Create a list of commands for CL to execute
    gs = gs.add_commands(
        [
            InitStateCommand(
                src_code=src_code, src_lang='python'
            ),  # Will initialize the state with specified Python source program
            GenFormalizationDataCommand(),  # Will gather relevant formalization data (required to create the model)
            GenModelCommand(),  # Will attempt to generate the formalized model
        ]
    )

    res = asyncio.run(gs.run(graph))  # Run the agent
    return maybe(mk_agent_state, res[0].last_fstate)


async def calc_search_embeddings(query: str):
    """
    Calculate search querry embeddings
    """
    graph = get_remote_graph('code_logician', api_key=get_imandra_uni_key())
    create_thread_sync(graph)

    gs = GraphState()

    # Create a list of commands for CL to execute
    gs = gs.add_commands(
        [InitStateCommand(src_code='', src_lang='Python'), EmbedCommand(query=query)]
    )
    res = await gs.run(graph)  # Run the agent

    def last_step_embedding(steps) -> list[float]:
        return steps[-1].message['query_embedding']

    return maybe(last_step_embedding, res[0].steps)
