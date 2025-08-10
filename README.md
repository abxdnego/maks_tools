# MAKS Tools

A suite of PySide6-based tools designed for Autodesk Maya that provides an intuitive interface for streamlined joint
orientation and viewport color management workflows. (More to come...)

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
- Avoid running individual tools after loading the main tools dialog, if an error occurs, restart Maya and try running the preferred script again.