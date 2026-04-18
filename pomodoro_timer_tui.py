import random

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.theme import Theme
from textual.widget import Widget
from textual.widgets import Header, Footer, Button, Static, Input, Digits, ProgressBar
from textual.containers import Vertical, Horizontal
from textual.binding import Binding
from rich.text import Text


MONO_DARK = Theme(
    name="mono-dark",
    primary="#9a9a9a",
    secondary="#707070",
    accent="#bdbdbd",
    foreground="#c8c8c8",
    background="#000000",
    success="#d0d0d0",
    warning="#a8a8a8",
    error="#8a8a8a",
    surface="#0d0d0d",
    panel="#171717",
    dark=True,
)


THEMES = {
    "classic": {
        "name": "classic pomodoro 🍅",
        "sesh": "⏰", "focus": "📖", "brk": "✅",
        "tagline": "welcome to pomodoro timer!",
        "textual_theme": "monokai",
        "particles": ["●", "•", "◦", "○"],
        "particle_color": "red",
        "particle_speed": (0.25, 0.55),
    },
    "soft": {
        "name": "soft and dreamy study 🌸",
        "sesh": "🎀", "focus": "🧸", "brk": "🌷",
        "tagline": "soft cozy study mode, get yourself ready to grind!",
        "textual_theme": "catppuccin-latte",
        "particles": ["✿", "❀", "✼", "❁", "✻"],
        "particle_color": "magenta",
        "particle_speed": (0.15, 0.4),
    },
    "cozy": {
        "name": "cozy desk energy 🎧",
        "sesh": "🍪", "focus": "🎧", "brk": "📓",
        "tagline": "cozy desk vibes loading... get your caffeine!",
        "textual_theme": "rose-pine",
        "particles": ["♪", "♫", "♬", "♩"],
        "particle_color": "yellow",
        "particle_speed": (0.2, 0.5),
    },
    "late": {
        "name": "late night coder 🌙",
        "sesh": "🌙", "focus": "🍵", "brk": "💻",
        "tagline": "late night grind time. the future is yours tonight. ^^",
        "textual_theme": "tokyo-night",
        "particles": ["✦", "✧", "★", "·", "˚"],
        "particle_color": "cyan",
        "particle_speed": (0.1, 0.3),
    },
    "focus": {
        "name": "focus + productive 🌿",
        "sesh": "🌿", "focus": "🧠", "brk": "🌱",
        "tagline": "focus mode. no excuses diva!",
        "textual_theme": "nord",
        "particles": ["❀", "✿", "❋", "✤"],
        "particle_color": "green",
        "particle_speed": (0.2, 0.45),
    },
    "mono": {
        "name": "monochrome / minimalistic 🖥️",
        "sesh": "🤍", "focus": "🖥️", "brk": "✦",
        "tagline": "minimal mode activated. seize it!",
        "textual_theme": "mono-dark",
        "particles": ["·", "•", "○", "◦"],
        "particle_color": "grey70",
        "particle_speed": (0.2, 0.5),
    },
}

PRESETS = {
    "25_5": (25 * 60, 5 * 60),
    "30_5": (30 * 60, 5 * 60),
    "50_10": (50 * 60, 10 * 60),
}


class FallingParticles(Widget):
    DEFAULT_CSS = """
    FallingParticles {
        layer: bg;
        width: 100%;
        height: 100%;
        background: transparent;
    }
    """

    def __init__(self, particles, color, speed_range, **kwargs):
        super().__init__(**kwargs)
        self._particles = particles
        self._color = color
        self._lo, self._hi = speed_range
        self._drops = []
        self._handle = None

    def on_mount(self) -> None:
        self._handle = self.set_interval(0.18, self._step)

    def on_unmount(self) -> None:
        if self._handle is not None:
            self._handle.stop()

    def _seed(self, w: int, h: int) -> None:
        n = max(10, w // 5)
        self._drops = []
        for _ in range(n):
            self._drops.append([
                random.randint(0, max(0, w - 1)),
                random.uniform(-h, h),
                random.choice(self._particles),
                random.uniform(self._lo, self._hi),
            ])

    def _step(self) -> None:
        w = self.size.width
        h = self.size.height
        if w <= 0 or h <= 0:
            return
        if not self._drops or len(self._drops) != max(10, w // 5):
            self._seed(w, h)
        for d in self._drops:
            d[1] += d[3]
            if d[1] >= h:
                d[0] = random.randint(0, max(0, w - 1))
                d[1] = random.uniform(-6, -1)
                d[2] = random.choice(self._particles)
                d[3] = random.uniform(self._lo, self._hi)
        self.refresh()

    def render(self):
        w = max(1, self.size.width)
        h = max(1, self.size.height)
        rows = [[" "] * w for _ in range(h)]
        for x, y, ch, _ in self._drops:
            iy = int(y)
            ix = int(x)
            if 0 <= iy < h and 0 <= ix < w:
                rows[iy][ix] = ch
        return Text("\n".join("".join(r) for r in rows), style=f"{self._color} dim")


class TimeInput(Input):
    DEFAULT_CSS = """
    TimeInput {
        width: 9;
        height: 3;
        text-align: center;
        text-style: bold;
        border: tall $accent;
        content-align: center middle;
    }
    TimeInput:focus {
        border: tall $success;
    }
    """

    def __init__(self, max_value: int = 99, initial: int = 0, **kwargs) -> None:
        super().__init__(
            value=f"{initial:02}",
            restrict=r"[0-9]{0,2}",
            max_length=2,
            **kwargs,
        )
        self._max = max_value

    @property
    def numeric(self) -> int:
        try:
            v = int(self.value or 0)
        except ValueError:
            return 0
        return max(0, min(self._max, v))


class TimePicker(Horizontal):
    DEFAULT_CSS = """
    TimePicker {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 0;
        content-align: center middle;
    }
    TimePicker .col {
        width: 9;
        height: auto;
        align: center middle;
    }
    TimePicker .colon {
        width: 3;
        height: 3;
        content-align: center middle;
        text-style: bold;
    }
    TimePicker .unit {
        width: 9;
        content-align: center middle;
        color: $text-muted;
    }
    """

    def __init__(self, prefix: str, hh_initial: int = 0, mm_initial: int = 25) -> None:
        super().__init__()
        self._prefix = prefix
        self._hh_init = hh_initial
        self._mm_init = mm_initial

    def compose(self) -> ComposeResult:
        with Vertical(classes="col"):
            yield TimeInput(max_value=23, initial=self._hh_init, id=f"{self._prefix}-hh")
            yield Static("hours", classes="unit")
        yield Static(":", classes="colon")
        with Vertical(classes="col"):
            yield TimeInput(max_value=59, initial=self._mm_init, id=f"{self._prefix}-mm")
            yield Static("minutes", classes="unit")

    @property
    def total_seconds(self) -> int:
        hh = self.query_one(f"#{self._prefix}-hh", TimeInput).numeric
        mm = self.query_one(f"#{self._prefix}-mm", TimeInput).numeric
        return hh * 3600 + mm * 60


class ParticleScreen(Screen):
    def _add_particles(self) -> None:
        theme = THEMES.get(getattr(self.app, "theme_key", "classic"), THEMES["classic"])
        self.mount(FallingParticles(
            particles=theme["particles"],
            color=theme["particle_color"],
            speed_range=theme["particle_speed"],
        ))

    def on_mount(self) -> None:
        self._add_particles()


class ThemeScreen(ParticleScreen):
    BINDINGS = [Binding("q", "app.quit", "quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Vertical(id="box"):
            yield Static("🍅  pomodoro timer", id="title")
            yield Static("what kind of theme would you prefer?", classes="subtitle")
            for key, theme in THEMES.items():
                yield Button(theme["name"], id=f"theme-{key}", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id or ""
        if bid.startswith("theme-"):
            key = bid.split("-", 1)[1]
            self.app.theme_key = key
            self.app.theme = THEMES[key]["textual_theme"]
            self.app.push_screen(TimerScreen())


class TimerScreen(ParticleScreen):
    BINDINGS = [Binding("escape", "app.pop_screen", "back")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        theme = THEMES[self.app.theme_key]
        with Vertical(id="box"):
            yield Static(theme["tagline"], classes="subtitle")
            yield Static("[⌛] choose your preferred timer:", classes="subtitle")
            yield Button("25 minutes work / 5 minutes break", id="preset-25_5", variant="primary")
            yield Button("30 minutes work / 5 minutes break", id="preset-30_5", variant="primary")
            yield Button("50 minutes work / 10 minutes break", id="preset-50_10", variant="primary")
            yield Button("custom", id="preset-custom", variant="warning")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id or ""
        if bid == "preset-custom":
            self.app.push_screen(CustomScreen())
        elif bid.startswith("preset-"):
            key = bid.split("-", 1)[1]
            study, brk = PRESETS[key]
            self.app.study_seconds = study
            self.app.break_seconds = brk
            self.app.push_screen(SessionScreen())


class CustomScreen(ParticleScreen):
    BINDINGS = [Binding("escape", "app.pop_screen", "back")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Vertical(id="box"):
            yield Static("⏱  set your custom timer", id="title")
            yield Static("study time", classes="section-title")
            yield TimePicker("study", hh_initial=0, mm_initial=25)
            yield Static("break time", classes="section-title")
            yield TimePicker("brk", hh_initial=0, mm_initial=5)
            yield Static("type a value or use ▲ ▼ / arrow keys", classes="hint")
            yield Static("", id="err")
            yield Button("continue", id="go", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "go":
            return
        err = self.query_one("#err", Static)
        pickers = list(self.query(TimePicker).results())
        study_secs = pickers[0].total_seconds
        break_secs = pickers[1].total_seconds
        if study_secs <= 0 or break_secs <= 0:
            err.update("⚠️  study and break durations must be greater than zero.")
            return
        self.app.study_seconds = study_secs
        self.app.break_seconds = break_secs
        self.app.push_screen(SessionScreen())


class SessionScreen(ParticleScreen):
    BINDINGS = [Binding("escape", "app.pop_screen", "back")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        theme = THEMES[self.app.theme_key]
        with Vertical(id="box"):
            yield Static(f"{theme['sesh']}  how many sessions today?", classes="subtitle")
            yield Input(placeholder="number of sessions (e.g., 4)", id="n")
            yield Static("", id="err")
            yield Button("start", id="go", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "go":
            return
        err = self.query_one("#err", Static)
        try:
            n = int(self.query_one("#n", Input).value)
            if n <= 0:
                raise ValueError
        except ValueError:
            err.update("⚠️  please enter a positive integer.")
            return
        self.app.session_count = n
        self.app.push_screen(RunningScreen())


class RunningScreen(ParticleScreen):
    BINDINGS = [
        Binding("space", "toggle_pause", "pause/resume"),
        Binding("s", "skip", "skip"),
        Binding("q", "quit_run", "menu"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        theme = THEMES[self.app.theme_key]
        self._paused = False
        self._session_idx = 0
        self._phase = "prep"
        self._remaining = 10
        self._phase_total = 10
        self._finished = False
        with Vertical(id="box"):
            yield Static(theme["tagline"], classes="subtitle")
            yield Static("", id="status")
            yield Digits("00:00", id="clock")
            yield ProgressBar(total=100, show_eta=False, show_percentage=True, id="bar")
            yield Static("", id="hint")
            yield Button("back to menu", id="menu", variant="warning")

    def on_mount(self) -> None:
        self._advance_label()
        self._update_clock()
        self._timer_handle = self.set_interval(1.0, self._tick)

    def _tick(self) -> None:
        if self._paused or self._finished:
            return
        self._remaining -= 1
        self._update_clock()
        if self._remaining <= 0:
            self._next_phase()

    def _update_clock(self) -> None:
        secs = self._remaining if self._remaining > 0 else 0
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        if h > 0:
            txt = f"{h:02}:{m:02}:{s:02}"
        else:
            txt = f"{m:02}:{s:02}"
        self.query_one("#clock", Digits).update(txt)
        bar = self.query_one("#bar", ProgressBar)
        total = self._phase_total if self._phase_total > 0 else 1
        bar.update(total=total, progress=total - secs)

    def _advance_label(self) -> None:
        theme = THEMES[self.app.theme_key]
        sess = self._session_idx + 1
        total = self.app.session_count
        status = self.query_one("#status", Static)
        hint = self.query_one("#hint", Static)
        if self._phase == "prep":
            status.update(f"session {sess} of {total}  —  get ready! ♡")
            hint.update("grab your belongings: books, headphones, pens. lock in!")
            self._phase_total = 10
        elif self._phase == "focus":
            status.update(f"{theme['focus']}  session {sess}/{total}  —  focus time 𝜗𝜚")
            hint.update("you got this ✫   [space] pause   [s] skip   [q] menu")
            self._phase_total = self.app.study_seconds
        else:
            status.update(f"{theme['brk']}  session {sess}/{total}  —  break time!")
            hint.update("don't vanish pls   [space] pause   [s] skip   [q] menu")
            self._phase_total = self.app.break_seconds

    def _next_phase(self) -> None:
        if self._phase == "prep":
            self._phase = "focus"
            self._remaining = self.app.study_seconds
        elif self._phase == "focus":
            self._phase = "break"
            self._remaining = self.app.break_seconds
        else:
            self._session_idx += 1
            if self._session_idx >= self.app.session_count:
                self._finish()
                return
            self._phase = "prep"
            self._remaining = 10
        self._advance_label()
        self._update_clock()

    def _finish(self) -> None:
        self._finished = True
        self._timer_handle.stop()
        self.query_one("#status", Static).update("✏️  all done! proud of you ♡")
        self.query_one("#hint", Static).update("press [q] to head back to the menu.")
        self.query_one("#clock", Digits).update("00:00")
        bar = self.query_one("#bar", ProgressBar)
        bar.update(total=1, progress=1)

    def action_toggle_pause(self) -> None:
        if self._finished:
            return
        self._paused = not self._paused
        hint = self.query_one("#hint", Static)
        if self._paused:
            hint.update("⏸  paused  —  [space] resume")
        else:
            self._advance_label()

    def action_skip(self) -> None:
        if self._finished:
            return
        self._remaining = 0

    def action_quit_run(self) -> None:
        self._timer_handle.stop()
        while len(self.app.screen_stack) > 2:
            self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "menu":
            self.action_quit_run()


class PomodoroApp(App):
    CSS = """
    Screen {
        align: center middle;
        layers: bg overlay;
    }
    #box {
        layer: overlay;
        border: round $accent;
        padding: 1 2;
        width: 78;
        height: auto;
        background: $surface;
    }
    #title {
        content-align: center middle;
        text-style: bold;
        color: $success;
        padding-bottom: 1;
    }
    .subtitle, .section-title, .hint {
        content-align: center middle;
        padding-bottom: 1;
    }
    .section-title { text-style: bold; padding-top: 1; color: $accent; }
    .hint { color: $text-muted; }
    #box Button { width: 100%; margin-bottom: 1; }
    Input { margin-bottom: 1; }
    #clock {
        content-align: center middle;
        width: 100%;
        height: 5;
        color: $success;
        text-style: bold;
    }
    #bar { width: 100%; margin-bottom: 1; }
    #status, #hint { content-align: center middle; padding: 1 0; }
    #hint { color: $text-muted; }
    #err { content-align: center middle; color: $error; padding-bottom: 1; }
    """

    TITLE = "pomodoro timer"
    SUB_TITLE = "study. break. repeat."

    theme_key = "classic"
    study_seconds = 25 * 60
    break_seconds = 5 * 60
    session_count = 1

    def on_mount(self) -> None:
        self.register_theme(MONO_DARK)
        self.theme = THEMES[self.theme_key]["textual_theme"]
        self.push_screen(ThemeScreen())


if __name__ == "__main__":
    PomodoroApp().run()
