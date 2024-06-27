import pickle
from repository.message_repository import MessageRepository
from model.timeline import Timeline, TimelineType


class TimelineRepository:
    def __init__(self, connection):
        self.connection = connection
        self.namespace = "timelines"
        self.message_repository = MessageRepository(connection)

    def post_message(self, message):
        message_key = self.message_repository.save(message)
        self.__add_to_timeline(message, TimelineType.INBOX, message_key)
        self.__add_to_timeline(message, TimelineType.SENT, message_key)

    def get(self, owner, type, date):
        timeline_key = self.__key(owner, type, date)
        timeline_bytes = self.connection.get(timeline_key)
        if timeline_bytes is None:
            return Timeline(owner, type)

        return pickle.loads(timeline_bytes)

    def __add_to_timeline(self, message, type, message_key):
        is_inbox = type == TimelineType.INBOX
        owner = message.recipient if is_inbox else message.sender

        timeline_key = self.__key(owner, type, message.created_at)

        timeline = self.get(owner, type, message.created_at)
        timeline.messages.append(message_key)
        timeline_bytes = pickle.dumps(timeline)

        self.connection.set(timeline_key, timeline_bytes)

    def __key(self, owner, type, date):
        return (
            self.namespace
            + ":"
            + owner
            + "_"
            + type.name
            + "_"
            + date.strftime("%Y-%m-%d")
        )
