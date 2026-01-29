import asyncio

from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState, Part, TextPart
from a2a.utils import new_task, new_agent_text_message

from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.content_codecs.common import natural_language_id

from a2a_acl.protocol.acl_message import ACLMessage, Illocution, ACLIncomingMessage
from a2a_acl.a2a_utils.send_message import sync_reply

from a2a_acl.interface import asi_parser
from a2a_acl.protocol.send_acl_message import spawn_send_acl_message
from sample_agents.llm_refactoring_advice.prompts import ask_llm_for_refactoring

my_card = asi_parser.read_file("advisor.asi").add_codecs([natural_language_id])


def decode_python(llm_answer: str):

    tag1 = "```python"
    tag2 = "```"
    if tag1 in llm_answer:
        (a, b) = llm_answer.split(tag1)
        if tag2 in b:
            (b, c) = b.split(tag2)
            return (a, b, c)
    raise ValueError(llm_answer)


class LLMAdvisor(ACLAgentExecutor):

    def __init__(self, url):
        super().__init__(agentcard=my_card, my_url=url)
        print(
            "Warning: launching a pure python A2A agent,"
            " unable to check .asi interface against python body."
        )

        self.spec = "A function that does nothing."

    async def execute_tell(
        self,
        m: ACLIncomingMessage,
        output_event_queue: EventQueue,
    ):
        self.spec = m.content
        await sync_reply(output_event_queue, "ack")
        print("Received a new specification to consider.")

    async def execute_on_upload(
        self,
        m: ACLIncomingMessage,
        output_event_queue: EventQueue,
    ):

        print("(creating a new task)")
        task = new_task(m.origin.message)
        await output_event_queue.enqueue_event(task)
        updater = TaskUpdater(output_event_queue, task.id, task.context_id)

        await asyncio.sleep(1)

        await updater.update_status(
            TaskState.working,
            new_agent_text_message("start working", context_id=m.origin.context_id),
        )

        await asyncio.sleep(1)

        print("(consult llm)")
        res = ask_llm_for_refactoring(
            self.spec,
            m.content,
        )
        (a, code, c) = decode_python(res)
        await updater.update_status(
            TaskState.working,
            new_agent_text_message(
                "LLM first comment:" + a, context_id=m.origin.context_id
            ),
        )
        await updater.update_status(
            TaskState.working,
            new_agent_text_message(
                "LLM second comment (possibly truncated):" + c,
                context_id=m.origin.context_id,
            ),
        )

        await asyncio.sleep(1)

        await updater.add_artifact(
            [Part(root=TextPart(text=code))], name="Final response."
        )

        await asyncio.sleep(1)

        await updater.complete()

        await asyncio.sleep(1)

        spawn_send_acl_message(m.sender, "upload", code, "", natural_language_id)

        return
