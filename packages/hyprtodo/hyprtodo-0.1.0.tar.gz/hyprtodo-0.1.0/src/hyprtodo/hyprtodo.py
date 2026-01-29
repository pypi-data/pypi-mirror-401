from pathlib import Path

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import (
    Button,
    Header,
    Input,
    RichLog,
    SelectionList,
)
from textual.widgets.selection_list import Selection


class StartingScreen(Screen):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("j", "down", "Down"),
        ("k", "up", "Up"),
        ("ctrl", "c", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.selection_list = SelectionList[int](id="selection_list")
        self.x = 0
        self.input = False
        self.directory = Path.home() / ".config" / "hypr" / "hyprtodo"
        self.file_name = self.directory / "todo.txt"

        # Code that may not be able to be trusted

    def on_mount(self) -> None:
        self.selection_list.focus()

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="buttons"):
            yield Input(
                placeholder="What to do?",
                classes="input",
            )
            yield Button("Commit", id="CommitButton")

        self.populate_selection_list()
        yield RichLog()

    def populate_selection_list(self):
        """
        Make the files if they are not already there.
        Read in from the file and populate the selection list
        This function is error prone if the file already exists.
        """

        # I think that exists ok flag may be better. I wonder if it is just a different way to skin the cat
        if not self.directory.exists():
            self.directory.mkdir(parents=True)  # not system dependent
            # subprocess.run(["mkdir", "-p", self.directory])
        if not self.file_name.exists():
            self.file_name.touch()
            # subprocess.run(["touch", self.file_name])

        with open(self.file_name, "r") as file:
            lines = file.readlines()
            self.mount(self.selection_list)
            for line in lines:
                self.selection_list.add_option(Selection(line.strip(), self.x, True))
                self.x += 1

    def remove_selected(self):
        """make a new list and assign it to the main selectionlist"""
        cleaned_selection_list = SelectionList[int]()
        for i in self.selection_list.selected:
            option = self.selection_list.get_option_at_index(i)
            text = str(option.prompt)
            cleaned_selection_list.add_option(Selection(text, self.x, True))
            self.x += 1

        self.selection_list.remove()
        self.selection_list = cleaned_selection_list
        self.mount(self.selection_list)

        return

    def commit(self):
        """
        The todo list starts as selected and you unselect files. Logic was easier this way.
        Commit the options that are selected to the text file.
        """
        with open(self.file_name, "w") as file:
            for i in self.selection_list.selected:
                option = self.selection_list.get_option_at_index(i)
                text = option.prompt
                file.write(str(text) + "\n")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Textual on decorator to handle the event of the button being pressed"""

        if self.x == 0:
            self.mount(self.selection_list)

        if event.button.id == "NewTodoButton" and not self.input:
            self.input = True
            self.mount(
                Input(
                    placeholder="What do to do?",
                    classes="input",
                )
            )

        elif event.button.id == "CommitButton":
            """iterate throught the list and clear the options that are selected"""
            self.x = 0  # reset to 0 to make sure the indices are correct
            self.commit()
            self.remove_selected()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """add options to the selection list"""
        self.selection_list.add_option(Selection(event.value, self.x, True))
        self.x += 1
        event.input.clear()
        self.commit()
        return

    def on_key(self, event: events.Key) -> None:
        if event.key == "j":
            self.selection_list.action_cursor_down()  # Move down in the list
        if event.key == "k":
            self.selection_list.action_cursor_up()  # Move up in the list
        if event.key == "escape":
            focused = self.screen.focused
            if focused:
                focused.blur()

        return


class TodoApp(App):
    # CSS_PATH = "V4AyuDark.tcss"  # or whatever you named the CSS file
    DARK_MODE = True
    BINDINGS = [("q", "quit", "Quit"), ("ctrl", "c", "Quit")]

    def __init__(self):
        super().__init__()

        # Give a user editable css so they may edit the color schemes
        default_css = Path(__file__).parent / "css" / "default.tcss"
        user_css = Path.home() / ".config" / "hyprtodo" / "custom.tcss"

        if not user_css.exists():
            user_css.parent.mkdir(parents=True, exist_ok=True)
            user_css.write_text(default_css.read_text())

        self.css_path = [str(user_css)]

    def on_mount(self) -> None:
        """Support for more screens in the future. namely integratioin with the google API"""
        self.push_screen(StartingScreen())


def main():
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
