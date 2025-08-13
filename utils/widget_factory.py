"""Widget factory system for creating widgets in a type-safe and extensible manner."""

from typing import Any, Dict, Optional

from loguru import logger

from shared.custom_button import CustomButtonWidget


class WidgetResolver:
    """Universal widget resolver with unified handling for all widget types."""

    def __init__(self, widgets_list: Dict[str, type]):
        """Initialize the widget resolver.

        Args:
            widgets_list: Dictionary mapping widget names to widget classes
        """
        self.widgets_list = widgets_list

    def resolve_widget(
        self, widget_spec: str, context: Dict[str, Any]
    ) -> Optional[Any]:
        """Unified method to resolve ALL widget types.

        Args:
            widget_spec: Widget specification (e.g., "battery", "@custom_button:0")
            context: Context containing config and other data needed for resolution

        Returns:
            Widget instance or None if resolution fails
        """
        try:
            # Unified pattern: extract type and identifier
            if widget_spec.startswith("@"):
                widget_type, identifier = self._parse_reference(widget_spec)
                return self._resolve_by_type(widget_type, identifier, context)
            else:
                # Normal widget: treated as special "widget" type
                return self._resolve_by_type("widget", widget_spec, context)

        except Exception:
            logger.exception(f"Failed to resolve widget '{widget_spec}'")
            return None

    def _parse_reference(self, widget_spec: str) -> tuple[str, str]:
        """Parse @type:identifier format."""
        parts = widget_spec[1:].split(":", 1)
        return parts[0], parts[1] if len(parts) > 1 else ""

    def _resolve_by_type(
        self, widget_type: str, identifier: str, context: Dict[str, Any]
    ):
        """Unified resolution by type - all widgets follow the same pattern."""
        resolvers = {
            "widget": lambda: self._create_simple_widget(identifier),
            "custom_button": lambda: self._create_custom_button(identifier, context),
        }

        resolver = resolvers.get(widget_type)
        return resolver() if resolver else None

    def _create_simple_widget(self, widget_name: str):
        """Create normal widget - same pattern as custom button."""
        widget_class = self.widgets_list.get(widget_name)
        return widget_class() if widget_class else None

    def _create_custom_button(self, identifier: str, context: Dict[str, Any]):
        """Create custom button - unified pattern."""
        try:
            index = int(identifier)
            buttons = (
                context.get("config", {})
                .get("widgets", {})
                .get("custom_button_group", {})
                .get("buttons", [])
            )

            if 0 <= index < len(buttons):
                return CustomButtonWidget(
                    widget_name=f"custom_button_{index}",
                    config=buttons[index]
                )
            return None
        except (ValueError, IndexError):
            logger.error(f"Invalid custom button index: {identifier}")
            return None

    def batch_resolve(
        self, widget_specs: list[str], context: Dict[str, Any]
    ) -> list[Any]:
        """Resolve multiple widgets efficiently.

        Args:
            widget_specs: List of widget specifications to resolve
            context: Context containing config and other data

        Returns:
            List of successfully created widget instances
        """
        widgets = []
        for spec in widget_specs:
            widget = self.resolve_widget(spec, context)
            if widget:
                widgets.append(widget)
        return widgets
