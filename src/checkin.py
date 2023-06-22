from rich.console import RenderableType
from textual import events
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer,Horizontal
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static,Checkbox
from rich.text import Text, TextType
from rich.style import Style
from rich.color import Color

import git

class MyCheckbox(Checkbox):
    BUTTON_LEFT  = '['
    BUTTON_RIGHT = ']'
    BUTTON_INNER = 'X'

    def on_mount(self) -> None:
        self.watch_value(self.value)

    def watch_value(self, v):
        #self.BUTTON_INNER = 'X' if v else '.'
        pass

class FileEntry(Static):
    fname=""
    status=""
    def compose(self):
        yield Checkbox()

    def on_mount(self):
        cb:Checkbox = self.query_one(Checkbox)
        cb._label = Text.from_markup(f"{self.fname} [i]{self.status}[/i]")



class PendingChangesList(Static):
    def compose(self):
        yield Horizontal(
            Button("Include selected", id="include"),
            Button("Include all", id="includeall"))
        yield ScrollableContainer(id="scrollwin1")

    async def on_mount(self):
        container = self.query_one("#scrollwin1")
        container.styles.height = "auto"
        async for f in git.status():
            fe=FileEntry()
            fe.fname = f[3:]
            fe.status= f[:2]
            container.mount(fe)

class CheckinList(Static):
    def compose(self):
        yield Horizontal(
            Button("Check in", id="checkin"),
            Button("Exclude selected", id="exclude"),
            Button("Exclude all", id="excludeall"))
        yield ScrollableContainer(id="scrollwin2")

    def on_mount(self):
        container = self.query_one("#scrollwin2")
        container.styles.height = "auto"


class CheckinApp(App):
    CSS_PATH = "checkin.css"

    #BINDINGS = [
    #    ("d", "toggle_dark", "Toggle dark mode"),
    #    ("a", "add_stopwatch", "Add"),
    #    ("r", "remove_stopwatch", "Remove"),
    #]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        yield CheckinList(id="checkinList")
        yield PendingChangesList(id="pendigList")



if __name__ == "__main__":
    app = CheckinApp()
    app.run()
