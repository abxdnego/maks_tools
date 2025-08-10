# MAKS Tools

A collection of rigging and pipeline tools for Autodesk Maya, built with PySide6.

## Tools Included
- Orienter: interactively orient joints with control over Aim/Up axes, world-up
  direction, auto-orient secondary axis, manual tweaks and
  visibility control for selected or all joints in the scene.
- Colorizer: apply viewport override index colors to selected shape
  nodes, restore defaults on either selected or all shapes in the scene.

## Requirements
- Autodesk Maya (tested with versions that ship PySide6 and maya.cmds)
- Python environment inside Maya (no standalone support)

## Installation

1. [Download MAKS Tools](https://github.com/abxdnego/maks_tools/releases/download/v0.1.0a/MAKS_Tools_v0.1.0a.zip)
2. Extract the contents to "C:/Users/{username}/maya/scripts/" 
3. In userSetup.mel, add the following line:

```mel
python("import maks_tools_loader");
```

## Usage (inside Maya)
- From the Script Editor (Python):

```python
from maks_tools.main import MainToolsWidget
MainToolsWidget.show_dialog()
```

- Or to run individual tools:

```python
from maks_tools.tools.orienter import OrienterWidget
OrienterWidget.show_dialog()

from maks_tools.tools.colorizer import ColorizerWidget
ColorizerWidget.show_dialog()
```

You can also add the above snippets to a Maya shelf button for quick access.

## Notes
- These tools are tested and only compatible with Maya 2025/2026. 