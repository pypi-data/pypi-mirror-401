"""
Output Styles Module for PraisonAI Agents.

Provides configurable output formatting:
- Predefined styles (concise, detailed, technical, etc.)
- Custom formatting rules
- Markdown/plain text/JSON output
- Response length control

Zero Performance Impact:
- All imports are lazy loaded via __getattr__
- Styles only applied when configured
- No overhead when not in use

Usage:
    from praisonaiagents.output import OutputStyle, OutputFormatter
    
    # Use predefined style
    style = OutputStyle.concise()
    
    # Apply to agent
    agent = Agent(
        instructions="...",
        output_style=style
    )
    
    # Or format manually
    formatter = OutputFormatter(style)
    formatted = formatter.format(response)
"""

__all__ = [
    # Core classes
    "OutputStyle",
    "OutputFormatter",
    # Style presets
    "StylePreset",
    # Configuration
    "OutputConfig",
    # Actions mode
    "ActionsSink",
    "enable_actions_mode",
    "disable_actions_mode",
    "is_actions_mode_enabled",
    "get_actions_sink",
]


def __getattr__(name: str):
    """Lazy load module components to avoid import overhead."""
    if name == "OutputStyle":
        from .style import OutputStyle
        return OutputStyle
    
    if name == "OutputFormatter":
        from .formatter import OutputFormatter
        return OutputFormatter
    
    if name == "StylePreset":
        from .style import StylePreset
        return StylePreset
    
    if name == "OutputConfig":
        from .config import OutputConfig
        return OutputConfig
    
    # Actions mode
    if name == "ActionsSink":
        from .actions import ActionsSink
        return ActionsSink
    
    if name == "enable_actions_mode":
        from .actions import enable_actions_mode
        return enable_actions_mode
    
    if name == "disable_actions_mode":
        from .actions import disable_actions_mode
        return disable_actions_mode
    
    if name == "is_actions_mode_enabled":
        from .actions import is_actions_mode_enabled
        return is_actions_mode_enabled
    
    if name == "get_actions_sink":
        from .actions import get_actions_sink
        return get_actions_sink
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
