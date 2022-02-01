from textual import events
from textual.app import App
from textual.widgets import Placeholder, Footer


class DAW(App):
    async def on_load(self, event: events.Load) -> None:
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        await self.view.dock(Footer(), edge="bottom")
