import logging

from textual.binding import Binding
from textual.widget import Widget

logging.basicConfig(
    filename="azure_explorer.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="a",
)


class Window(Widget):

    BINDINGS = [
        Binding("escape", "go_to_parent_window", "Go Back", show=True, priority=True),
    ]

    def __init__(self):
        """Widget representing a window in a stack of windows,
        meaning it is possible to (1) go back to the parent window
        or (2) open a child window.
        """
        self.parent_window = None
        super().__init__()

    def check_valid(self) -> bool:
        return True

    def action_go_to_parent_window(self):
        if self.parent_window is not None:
            self.remove()
            self.app.mount(self.parent_window)

    def open_child_window(self, window: "Window"):
        try:
            window.check_valid()
        except Exception as exc:
            self.app.notify(str(exc), severity="error")
            return

        window.parent_window = self
        self.remove()
        self.app.mount(window)
