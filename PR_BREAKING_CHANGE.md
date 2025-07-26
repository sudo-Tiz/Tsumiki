🚀 Add CustomButtonGroup Widget

### Summary
Adds a new `custom_button_group` widget that allows users to create a group of customizable buttons for executing shell commands directly from the panel.

**⚠️ Important:** This is a new feature with no breaking changes to existing configurations.

### Features
- **Configurable buttons**: Define multiple buttons with custom commands, icons, labels, and tooltips
- **Flexible layout**: Buttons display in a horizontal group with customizable spacing
- **Full customization**: Each button supports:
  - Custom shell commands
  - Nerd Font icons
  - Labels and tooltips
  - Style classes

### Configuration Example
```json
"custom_button_group": {
  "buttons": [
    {
      "command": "firefox",
      "icon": "󰈹",
      "label_text": "Firefox",
      "tooltip_text": "Open Firefox Browser",
      "show_icon": true,
      "label": false,
      "tooltip": true
    }
  ],
  "spacing": 4
}
```

### Changes
✅ New CustomButtonGroup widget class
✅ JSON schema validation
✅ Default configuration
✅ Example configuration
✅ Documentation updates
✅ Following project conventions

### Testing
☑️ Widget loads correctly
☑️ Buttons execute commands
☑️ Configuration validation works
☑️ Follows code style guidelines

Ready for review! 🎉
