from enum import Enum


class TimelineType(Enum):
    INBOX = 1
    SENT = 2


class Timeline:
    def __init__(self, owner, type):
        self.owner = owner
        self.type = type
        self.messages = []
