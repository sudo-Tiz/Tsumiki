from fabric.widgets.button import Button


class Power(Button):
    def __init__(self, icon="", **kwargs):
        super().__init__(name="power", style_classes="bar-button", **kwargs)
        self.set_label(icon)
