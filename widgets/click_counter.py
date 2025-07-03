from shared.widget_container import ButtonWidget


class ClickCounterWidget(ButtonWidget):
    """A widget to count the number of clicks."""

    def __init__(self, **kwargs):
        super().__init__(name="click_counter", **kwargs)

        self.count = self.config.get("count", 0)
        self.set_label(f"{self.count}")

        self.connect("button-press-event", self.on_button_press)

        if self.config.get("tooltip", True):
            self.set_tooltip_text("Left-click to increment, right-click to reset")

    def increment(self, *_):
        self.count = self.count + 1
        self.set_label(f"{self.count}")

    def reset(self, *_):
        self.count = 0
        self.set_label(f"{self.count}")

    def on_button_press(self, _, event):
        if event.button == 1:
            self.increment()
        else:
            self.reset()
