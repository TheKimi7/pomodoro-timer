from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Digits, ProgressBar
from textual.reactive import reactive

class PomodoroApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    #timer {
        text-align: center;
        text-style: bold;
    }
    """

    time_left = reactive(25 * 60)
    running = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Digits("25:00", id="timer")
        yield ProgressBar(total=25 * 60, id="progress")
        yield Button("Start", id="start")
        yield Button("Reset", id="reset")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.running = not self.running
            event.button.label = "Pause" if self.running else "Resume"
        elif event.button.id == "reset":
            self.running = False
            self.time_left = 25 * 60

    def watch_time_left(self, value: int) -> None:
        mins, secs = divmod(value, 60)
        self.query_one("#timer", Digits).update(f"{mins:02}:{secs:02}")
        self.query_one("#progress", ProgressBar).advance(0)

    def on_mount(self) -> None:
        self.set_interval(1, self.tick)

    def tick(self) -> None:
        if self.running and self.time_left > 0:
            self.time_left -= 1
        elif self.running and self.time_left == 0:
            self.running = False
            self.notify("Pomodoro done! Take a break.")

if __name__ == "__main__":
    PomodoroApp().run()
