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
    ) -> Optional[Any]:
        """Unified resolution by type - all widgets follow the same pattern."""
        resolvers = {
            "widget": lambda: self._create_simple_widget(identifier),
            "custom_button": lambda: self._create_custom_button(identifier, context),
            "group": lambda: self._create_widget_group(identifier, context),
            "collapsible": lambda: self._create_collapsible_group(identifier, context),
        }

        resolver = resolvers.get(widget_type)
        return resolver() if resolver else None

    def _create_simple_widget(self, widget_name: str) -> Optional[Any]:
        """Create normal widget - same pattern as custom button."""
        widget_class = self.widgets_list.get(widget_name)
        return widget_class() if widget_class else None

    def _create_custom_button(
        self, identifier: str, context: Dict[str, Any]
    ) -> Optional[CustomButtonWidget]:
        """Create custom button - unified pattern."""
        try:
            index = int(identifier)
            config = context.get("config", {})
            buttons = (
                config.get("widgets", {})
                .get("custom_button_group", {})
                .get("buttons", [])
            )

            # Validate bounds before access
            if not isinstance(buttons, list) or not (0 <= index < len(buttons)):
                logger.error(
                    f"Custom button index {index} out of range "
                    f"(0-{len(buttons)-1})"
                )
                return None

            return CustomButtonWidget(
                widget_name=f"custom_button_{index}",
                config=buttons[index]
            )
        except (ValueError, IndexError, TypeError) as e:
            logger.error(f"Invalid custom button index: {identifier} - {e}")
            return None

    def _create_widget_group(
        self, identifier: str, context: Dict[str, Any]
    ) -> Optional[Any]:
        """Create widget group - unified pattern."""
        try:
            from shared.widget_container import WidgetGroup

            index = int(identifier)
            config = context.get("config", {})
            groups = config.get("widget_groups", [])

            if not isinstance(groups, list) or not (0 <= index < len(groups)):
                logger.error(f"Widget group index {index} out of range")
                return None

            group_config = groups[index]
            return WidgetGroup.from_config(
                group_config,
                self.widgets_list,
                main_config=config,
            )
        except (ValueError, IndexError, TypeError) as e:
            logger.error(f"Invalid widget group index: {identifier} - {e}")
            return None

    def _create_collapsible_group(
        self, identifier: str, context: Dict[str, Any]
    ) -> Optional[Any]:
        """Create collapsible group - unified pattern."""
        try:
            from shared.collapsible_group import CollapsibleGroupWidget

            index = int(identifier)
            config = context.get("config", {})
            groups = config.get("collapsible_groups", [])

            if not isinstance(groups, list) or not (0 <= index < len(groups)):
                logger.error(f"Collapsible group index {index} out of range")
                return None

            group_config = groups[index]
            collapsible_group = CollapsibleGroupWidget()
            collapsible_group.update_config(group_config)
            collapsible_group.widgets_config = group_config.get("widgets", [])
            collapsible_group.set_context(config, self.widgets_list)

            return collapsible_group
        except (ValueError, IndexError, TypeError) as e:
            logger.error(f"Invalid collapsible group index: {identifier} - {e}")
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
        return [
            widget
            for spec in widget_specs
            if (widget := self.resolve_widget(spec, context))
        ]
