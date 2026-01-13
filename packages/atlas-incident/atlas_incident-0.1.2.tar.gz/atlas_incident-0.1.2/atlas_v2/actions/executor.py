class ActionExecutor:
    def __init__(self):
        self.performed = []

    def execute(self, action_name: str) -> None:
        # mock side-effect
        self.performed.append(action_name)
