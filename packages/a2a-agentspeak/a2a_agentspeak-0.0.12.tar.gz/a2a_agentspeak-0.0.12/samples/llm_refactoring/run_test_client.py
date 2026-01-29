import a2a
import a2a_acl.utils.strings
from a2a_acl.content_codecs.common import natural_language_id

import context

from a2a.types import (
    AgentCard,
    TaskState,
)

from a2a_acl.protocol.send_acl_message import (
    spawn_send_acl_message,
    extract_text_from_task,
    extract_text_from_message,
)
from a2a_acl.a2a_utils.card_holder import download_card


from a2a_acl.utils.url import build_url

from a2a_agentspeak.content_codecs.common import python_agentspeak_codec_id

host = "127.0.0.1"
code_to_analyse = context.code


async def main() -> None:
    target_agent_url = build_url(host, context.manager_port)

    # Fetch Public Agent Card and Initialize Client
    target_agent_card: AgentCard | None = None

    try:
        target_agent_card = await download_card(target_agent_url)

    except Exception:
        print("Client failed to fetch the public agent card. Cannot continue.")
        exit(-1)

    spawn_send_acl_message(
        target_agent_card,
        "tell",
        "spec(" + a2a_acl.utils.strings.neutralize_str(context.specification) + ")",
        "",
        python_agentspeak_codec_id
    )

    print("[Tell-Message sent to advisor agent.]")

    await asyncio.sleep(1)

    spawn_send_acl_message(
        target_agent_card,
        "upload",
        code_to_analyse,
        "",
        natural_language_id
    )
    print("[Tell-Message sent to agent.]")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    input("Press Enter to exit.\n")
