class AuditTrail:
    def __init__(self):
        self.events = []

    def record(self, message: str) -> None:
        self.events.append(message)
