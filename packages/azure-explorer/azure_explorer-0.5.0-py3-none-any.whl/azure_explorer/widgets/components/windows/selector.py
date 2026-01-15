from abc import abstractmethod
from typing import Iterator

from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option

from azure_explorer.widgets.components.windows.base import Window


class Selector(Window):
    """Window representing a selector of options"""

    def compose(self) -> ComposeResult:
        options = []
        for id_, label in self.iter_options():
            options.append(Option(label, id=id_))

        option_list = OptionList(*options)

        option_list.focus()

        yield option_list

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        selected_id = event.option_id

        try:
            widget = self.get_option_widget(selected_id)
        except Exception as exc:
            self.notify(str(exc), severity="error")
            return

        if widget is None:
            return

        self.open_child_window(widget)

    @abstractmethod
    def iter_options(self) -> Iterator[tuple[str, str]]:
        ...

    @abstractmethod
    def get_option_widget(self, id_: str) -> "Window":
        ...
