from dataclasses import dataclass
from enum import StrEnum

from a2a.server.agent_execution import RequestContext


class Illocution(StrEnum):
    """Illocutions that are used in messages.
    * TELL, ACHIEVE, ASK are basic illocutions inspired by KQML.
    * PROPOSE is suited for artitration or consensus.
    * UPLOAD is suited for file transfer.
    """

    TELL = "tell"
    ACHIEVE = "achieve"
    ASK = "ask"
    PROPOSE = "propose"
    UPLOAD = "upload"


@dataclass
class ACLMessage:
    illocution: Illocution
    content: str
    sender: str
    codec: str


@dataclass
class ACLIncomingMessage(ACLMessage):
    task_id: str
    origin: RequestContext
