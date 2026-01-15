from abc import abstractmethod
from typing import Any, Iterator

from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import DataTable, Input

from azure_explorer.widgets.components.windows.base import Window
from azure_explorer.widgets.utils import CachedIterator


class Browser(Window):

    BINDINGS = [
        Binding("home", "top_row", "Top row", show=False, priority=True),
        Binding("end", "bottom_row", "Bottom row", show=False, priority=True),
        Binding("up", "previous_row", "Previous row", show=False, priority=True),
        Binding("down", "next_row", "Next row", show=False, priority=True),
        Binding("pageup", "previous_page", "Previous page", show=True, priority=True),
        Binding("pagedown", "next_page", "Next page", show=True, priority=True),
        Binding("tab", "autocomplete", "Autocomplete", show=False, priority=True),
        Binding("ctrl+r", "refresh", "Refresh", show=True, priority=True),
    ]

    COLUMN_NAMES: list[str] = ...

    def __init__(self):
        self.search_filter = ""
        self.current_page = 0
        self.rows = None
        self.items_per_page = None
        self.filtered_rows = None

        super().__init__()

    def compose(self) -> ComposeResult:
        input_ = Input(placeholder="Search...")
        yield input_

        data_table = DataTable(cursor_type="row")
        data_table.can_focus = False
        yield data_table

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action may run."""
        if action == "previous_page":
            if self.current_page == 0:
                return None
        elif action == "next_page":
            if not self.filtered_rows.done:
                return True
            num_rows = len(self.filtered_rows)
            last_page = (num_rows - 1) // self.items_per_page
            if self.current_page >= last_page:
                return None
        return True

    def action_previous_row(self):
        table = self.query_one(DataTable)
        table.action_cursor_up()

    def action_next_row(self):
        table = self.query_one(DataTable)
        table.action_cursor_down()

    def action_previous_page(self):
        self.current_page -= 1
        self.populate_table()

    def action_next_page(self):
        self.current_page += 1
        self.populate_table()

    def action_top_row(self):
        table = self.query_one(DataTable)
        table.action_scroll_top()

    def action_bottom_row(self):
        table = self.query_one(DataTable)
        table.action_scroll_bottom()

    def action_autocomplete(self):
        self.get_highlighted_item()
        input = self.query_one(Input)
        input.value = self.get_highlighted_item()

    def action_refresh(self):
        self.set_rows()
        self.set_filtered_rows()
        self.current_page = 0
        self.populate_table()

    def set_rows(self):
        self.rows = CachedIterator(self.iter_rows())

    def set_filtered_rows(self):
        self.filtered_rows = CachedIterator(self.iter_filtered_rows())

    def get_highlighted_item(self) -> Any:
        table = self.query_one(DataTable)
        if table.cursor_row is None:
            return None

        if not table.is_valid_coordinate(table.cursor_coordinate):
            return None

        selected_id = table.coordinate_to_cell_key(
            table.cursor_coordinate
        ).row_key.value
        return selected_id

    def _on_mount(self):
        self.items_per_page = self.app.size.height - 6

        self.set_rows()
        self.set_filtered_rows()

        table = self.query_one(DataTable)
        table.add_columns(*self.COLUMN_NAMES)

        self.populate_table()
        self.query_one(Input).focus()

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        selected_id = event.row_key.value

        try:
            widget = self.get_item_widget(selected_id)
        except Exception as exc:
            self.notify(str(exc), severity="error")
            return

        if widget is None:
            return

        self.open_child_window(widget)

    def on_input_changed(self, event: Input.Changed):
        self.search_filter = event.value.lower()
        self.set_filtered_rows()
        self.current_page = 0
        self.populate_table()

    def on_input_submitted(self):
        self.query_one(DataTable).action_select_cursor()

    def on_resize(self, event: events.Resize) -> None:
        self.items_per_page = self.app.size.height - 6
        self.current_page = 0
        self.populate_table()

    def populate_table(self):
        table = self.query_one(DataTable)
        table.clear()

        items_per_page = self.items_per_page
        start = self.current_page * items_per_page
        end = start + items_per_page

        for id_, item in self.filtered_rows[start:end]:
            table.add_row(*item, key=id_)

        self.refresh_bindings()

    def iter_filtered_rows(self) -> Iterator[tuple[str]]:
        search_filter = self.query_one(Input).value.lower()
        for id_, item in self.rows:
            valid = False
            for col in item:
                if search_filter in str(col).lower():
                    valid = True
            if valid:
                yield id_, item

    @abstractmethod
    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        ...

    @abstractmethod
    def get_item_widget(self, id_: str) -> "Window":
        ...
