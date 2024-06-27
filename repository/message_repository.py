import pickle


class MessageRepository:
    def __init__(self, connection):
        self.connection = connection
        self.namespace = "messages"

    def save(self, message):
        message_key = self.__key(message)
        message_bytes = pickle.dumps(message)
        self.connection.set(message_key, message_bytes)
        return message_key


    def get(self, message_key):
        message_bytes = self.connection.get(message_key)
        if message_bytes:
            return pickle.loads(message_bytes)
        elif not message_bytes:
            return False

    def __key(self, message):
        return (
            self.namespace
            + ":"
            + message.sender
            + "_"
            + message.created_at.strftime("%Y-%m-%d %H:%M:%S.%M")
        )
