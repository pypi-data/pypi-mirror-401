import a2a

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

host = "127.0.0.1"
specification = "A function that says hello."
code_to_analyse = 'def hello(name): print("hello " + name + ".")'


def handle_status_update(event, t):
    match type(t):
        case a2a.types.TaskStatusUpdateEvent:
            m = t.status.message
            print("(status update: " + str(t.status.state) + ")")
            match t.status.state:
                case TaskState.working:
                    print(
                        "(working update message: "
                        + (m.parts[0].root.text if m is not None else "-")
                        + ")"
                    )
                case TaskState.completed:
                    print("(receveived : task completed)")
                case other:
                    print("(other update:" + other + ")")
        case other:
            print("(status update ignored: " + other + ")")


async def main() -> None:
    target_agent_url = build_url(host, context.advisor_port)

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
        specification,
        "",
        "nl",
        message_processor=(
            lambda m: print("Message event: " + extract_text_from_message(m))
        ),
        task_processor=(
            lambda t: print("Task artifact event: " + extract_text_from_task(t))
        ),
        status_update_processor=handle_status_update,
    )
    print("[Tell-Message sent to advisor agent.]")

    await asyncio.sleep(0.5)

    def task_processor(t):
        print("Task artifact: ")
        print("**************************************************************")
        print(extract_text_from_task(t))
        print("**************************************************************")

    spawn_send_acl_message(
        target_agent_card,
        "upload",
        code_to_analyse,
        "",
        "nl",
        message_processor=(lambda m: print("Message: " + str(m))),
        task_processor=task_processor,
        status_update_processor=handle_status_update,
    )
    print("[Propose-Message sent to advisor agent.]")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    input("Press Enter to exit.\n")
