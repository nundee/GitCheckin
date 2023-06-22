from rich.console import RenderableType
from textual import events
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static,Checkbox
from rich.text import Text, TextType
from rich.style import Style
from rich.color import Color

import git

class MyCheckbox(Checkbox):
    BUTTON_LEFT  = '['
    BUTTON_RIGHT = ']'
    BUTTON_INNER = ' '

    def on_mount(self) -> None:
        self.watch_value(self.value)

    def watch_value(self, v):
        self.BUTTON_INNER = 'X' if v else ' '

class FileEntry(Static):
    fname=""
    status=""
    def compose(self):
        yield MyCheckbox()

    def on_mount(self):
        cb:Checkbox = self.query_one(Checkbox)
        cb._label = Text.from_markup(f"{self.fname} [i]{self.status}[/i]")

class FileList(Static):
    def compose(self):
        yield ScrollableContainer(id="scrollwin")

    async def on_mount(self):
        container = self.query_one("#scrollwin")
        files=await git.status()
        for f in files:
            fe=FileEntry()
            fe.fname = f[3:]
            fe.status= f[:2]
            container.mount(fe)

class CheckinApp(App):
    #CSS_PATH = "stopwatch.css"

    #BINDINGS = [
    #    ("d", "toggle_dark", "Toggle dark mode"),
    #    ("a", "add_stopwatch", "Add"),
    #    ("r", "remove_stopwatch", "Remove"),
    #]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        yield FileList(id="files")



if __name__ == "__main__":
    app = CheckinApp()
    app.run()
