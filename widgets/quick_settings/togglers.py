from shared.button_toggle import CommandSwitcher


class QuickSettingToggler(CommandSwitcher):
    """A button widget to toggle a command."""

    def __init__(self, command, name, enabled_icon, disabled_icon, **kwargs):
        super().__init__(
            command,
            enabled_icon,
            disabled_icon,
            name,
            label=True,
            tooltip=False,
            interval=1000,
            style_classes="quicksettings-toggler",
            **kwargs,
        )


class HyprIdleQuickSetting(QuickSettingToggler):
    """A button to toggle the hyper idle mode."""

    def __init__(self, **kwargs):
        super().__init__(
            command="hypridle",
            enabled_icon="",
            disabled_icon="",
            name="quicksettings-togglebutton",
        )


class HyprSunsetQuickSetting(QuickSettingToggler):
    """A button to toggle the hyper idle mode."""

    def __init__(self, **kwargs):
        super().__init__(
            command="hyprsunset -t 2800k",
            enabled_icon="󱩌",
            disabled_icon="󰛨",
            name="quicksettings-togglebutton",
        )
