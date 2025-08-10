# MAKS Tools

A suite of PySide6-based tools designed for Autodesk Maya that provides an intuitive interface for streamlined joint
orientation and viewport color management workflows. (More to come...)

## Tools Included
- Orienter: interactively orient joints with control over Aim/Up axes, world-up
  direction, auto-orient secondary axis, manual tweaks and
  visibility control for selected or all joints in the scene.
- Colorizer: apply viewport override index colors to selected shape
  nodes, restore defaults on either selected or all shapes in the scene.

## Features
- Clean and intuitive user interface designed for an efficient workflow.
- Dockable windows that can be integrated into Maya's workspace.
- Interactive controls including scrollable spin boxes for precise manual tweaking.

## Requirements
- Autodesk Maya 2025 or later.

## Installation

1. [Click Here to Download MAKS Tools](https://github.com/abxdnego/maks_tools/releases/download/v0.1.0a/MAKS_Tools_v0.1.0-alpha.zip)
2. Extract the contents to:
    - Windows: "C:/Users/{username}/maya/scripts/"
    - macOS: "/Users/{username}/Library/Preferences/Autodesk/maya/scripts/"
    - Linux: "/home/{username}/maya/scripts/"
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

- Known Issue: There is currently a bug to resolve. Avoid running a script on the individual tool after loading the MainToolsWidget, if an error occurs, restart Maya and try running the preferred individual tool script again. 
- These tools are tested and only compatible with Maya 2025/2026 as there are maya.cmds functions that are not available
  in earlier versions. No PySide2 version will be developed to ensure future-proofing and compatibility with modern Maya
  versions.

