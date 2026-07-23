from app.utils.helper import get_rules
class Smrules:
    def __init__(self) -> None:
        self.repository = None

    def show_rules(self) -> dict[str, str]:
        return get_rules()
