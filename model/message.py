import datetime


class Message:
    def __init__(self, sender, recipient, text):
        self.sender = sender
        self.recipient = recipient
        self.created_at = datetime.datetime.now()
        self.text = text
