"""Custom button widgets for executing shell commands."""

from fabric.utils import exec_shell_command_async
from fabric.widgets.label import Label
from loguru import logger

from shared.widget_container import ButtonWidget, WidgetGroup
from utils.widget_utils import nerd_font_icon


class CustomButtonWidget(ButtonWidget):
    """A widget that executes a custom bash command when clicked."""

    def __init__(
        self,
        widget_name: str = "custom_button",
        config: dict | None = None,
        **kwargs
    ):
        """Initialize the custom button widget.

        Args:
            widget_name: The name of the widget instance
            config: An optional configuration dictionary. If None, config is
                loaded from the global scope.
            **kwargs: Additional arguments passed to the parent
        """
        super().__init__(name=widget_name, **kwargs)

        if config is not None:
            self.config = config

        # Get command from config
        self.command = self.config.get("command", "")

        if not self.command:
            raise ValueError(
                f"Custom button '{widget_name}' requires a 'command' in config"
            )

        # Setup icon if specified
        if self.config.get("show_icon", True):
            icon = self.config.get("icon", "")
            if icon:
                self.icon = nerd_font_icon(
                    icon=icon,
                    props={"style_classes": "panel-font-icon"},
                )
                self.box.add(self.icon)

        # Setup label if specified
        if self.config.get("label", True):
            label_text = self.config.get("label_text", "Button")
            self.label = Label(
                label=label_text,
                style_classes="panel-text"
            )
            self.box.add(self.label)

        # Connect click handler
        self.connect("clicked", self.on_clicked)

        # Setup tooltip
        if self.config.get("tooltip", True):
            tooltip_text = self.config.get("tooltip_text", f"Execute: {self.command}")
            self.set_tooltip_text(tooltip_text)

    def on_clicked(self, *_):
        """Execute the custom command when button is clicked."""
        if self.command:
            exec_shell_command_async(
                self.command,
                lambda _: None  # No callback needed
            )


class CustomButtonGroupWidget(WidgetGroup):
    """A widget group that displays custom buttons defined in configuration."""

    def __init__(self, **kwargs):
        """Initialize the custom button group.

        Args:
            **kwargs: Additional arguments passed to the parent
        """
        widget_name = kwargs.get("name", "custom_button_group")
        super().__init__(name=widget_name, **kwargs)

        # Get buttons configuration from config
        buttons_config = self.config.get("buttons", [])

        if not buttons_config:
            return

        # Create custom buttons from configuration
        for i, button_config in enumerate(buttons_config):
            button = self._create_custom_button(button_config, i)
            if button:
                self.add(button)

    def _create_custom_button(self, button_config: dict, index: int):
        """Create a single custom button from configuration.

        Args:
            button_config: Configuration dictionary for the button
            index: Index of the button in the list

        Returns:
            CustomButtonWidget instance or None if invalid config
        """
        command = button_config.get("command", "")
        if not command:
            logger.warning(f"Custom button at index {index} has no command")
            return None

        # Create a temporary config for this button
        temp_config = {
            "command": command,
            "show_icon": button_config.get("show_icon", True),
            "icon": button_config.get("icon", ""),
            "label": button_config.get("show_label", True),
            "label_text": button_config.get("label", "Button"),
            "tooltip": button_config.get("show_tooltip", True),
            "tooltip_text": button_config.get("tooltip", f"Execute: {command}")
        }

        # Create a custom button widget
        button = CustomButtonWidget(config=temp_config)

        # Add custom style classes if specified
        style_classes = button_config.get("style_classes", [])
        if style_classes:
            for style_class in style_classes:
                button.add_style_class(style_class)

        return button
