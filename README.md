# MAKS Tools

A collection of rigging and pipeline tools for Autodesk Maya, built with PySide6.

## Tools Included
- Orienter: interactively orient joints with control over Aim/Up axes, world-up
  direction, auto-orient secondary axis, and manual local-axis tweaks with freeze.
- Colorizer: apply legacy viewport override index colors (0–31) to selected shape
  nodes, restore defaults, or reset all meshes.

## Requirements
- Autodesk Maya (tested with versions that ship PySide6 and maya.cmds)
- Python environment inside Maya (no standalone support)

## Installation
1. Clone or copy the `maks_tools` folder to a location accessible by Maya (e.g., a
   pipeline tools directory added to your PYTHONPATH or Maya scripts path).
2. Ensure the folder `C:/dev/maks_tools` (or your chosen location) is on `sys.path`
   within Maya. For example, in Maya's Script Editor (Python tab):

```python
import sys
sys.path.append(r"C:/dev")
```

## Usage (inside Maya)
- From the Script Editor (Python):

```python
from maks_tools.main import MainToolsWidget
w = MainToolsWidget()
w.show(dockable=True)
```

- Or to run individual tools:

```python
from maks_tools.tools.orienter import OrienterWidget
OrienterWidget().show(dockable=True)

from maks_tools.tools.colorizer import ColorizerWidget
ColorizerWidget().show(dockable=True)
```

You can also add the above snippets to a Maya shelf button for quick access.

## Notes
- These tools operate directly on the Maya scene via `maya.cmds` and are intended
  for use within Maya only.
- The Colorizer uses Maya's legacy index colors (0–31). Color appearance may vary
  depending on Maya theme and viewport settings.
