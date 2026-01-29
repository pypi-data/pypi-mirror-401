import context
from agentspeak import LinkedList, Literal

from a2a.utils import new_agent_text_message

from a2a.server.events import EventQueue


from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.agent.server_utils import run_server
from a2a_acl.protocol.acl_message import ACLMessage, Illocution

from a2a_agentspeak.content_codecs import cold_repository_codec
from a2a_agentspeak.content_codecs.common import (
    python_agentspeak_codec_id,
    cold_repository_down_codec_id,
    cold_repository_up_codec_id, atom_codec_id,
)

from a2a_acl.interface.interface import SkillDeclaration, ACLAgentCard
from a2a_agentspeak.build_server import build_and_run
from a2a_acl.protocol.send_acl_message import (
    spawn_send_acl_message, extract_text_from_message, extract_text_from_task,
)

from a2a_acl.a2a_utils.card_holder import download_card
from cold_repository import codec
from a2a_acl.utils.url import build_url


# We first define an agent that will receive the pong messages from the spawned agent.

my_skill_1 = SkillDeclaration(Illocution.TELL, "pong", 0, "Receive a pong reply.")
my_skill_2 = SkillDeclaration(
    Illocution.TELL, "selected", 2, "Receive a cold agent."
)
my_skills = [my_skill_1, my_skill_2]

class ClientAgentExecutor(ACLAgentExecutor):

    def __init__(self, host, port):
        super().__init__(host,port)
        self.codec_objects[cold_repository_down_codec_id]= cold_repository_codec.down_codec_object

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        res = m.content
        print("Incoming message: " + res)
        print("TEST " + ("OK" if res == "pong" else "KO"))
        await output_event_queue.enqueue_event(
            new_agent_text_message("MESSAGE RECEIVED")
        )

my_url = context.client_url


def decode_and_spawn(res:str):
        """ Decode a message from a cold repository,
            then spawn the agent described in that message,
            and send a achieve:ping message to that agent.
        """
        (filename, holes) = codec.decode_cold_descr(res)

        build_and_run(
            context.path_to_sample_agents + filename, context.host, context.free_port
        )

        spawn_send_acl_message(
            build_url(context.host, context.free_port),
            "achieve",
            "ping",
            my_url,
            atom_codec_id,
        )


async def main() -> None:

    # 1) start an a2a server to receive asynchronous answers
    my_card = ACLAgentCard(
        "Client Agent",
        "A client agent",
        my_skills,
        [cold_repository_down_codec_id, python_agentspeak_codec_id, atom_codec_id],
    )

    run_server(ClientAgentExecutor(my_card, my_url), context.host, context.client_port)

    # 2) query the repository

    try:
        repository_card = await download_card(context.repository_url)
    except Exception:
        print("Repository not available. Cannot continue.")
        exit(-1)

    test_skill = Literal("mandatory_skill", (Literal("achieve"), Literal("ping"), 0))
    lst = LinkedList(test_skill, [])
    request = str(Literal("cold_by_skills", (lst,)))

    print("Sending a request to the repository.")
    spawn_send_acl_message(
        repository_card, "ask", request, my_url,
        codec = cold_repository_up_codec_id,
        message_processor=lambda message: decode_and_spawn(extract_text_from_message(message)),
        task_processor=lambda message: decode_and_spawn(extract_text_from_task(message))
    )



if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
