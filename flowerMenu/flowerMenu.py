import pymel.core as pym


menu_tool = """
import FlowerRigTool.FlowerRigTool
reload(FlowerRigTool.FlowerRigTool)

FlowerRigTool.FlowerRigTool.initCharacterPicker()
"""

menu_clean = """
import MEm.clean.utils as utl
utl.removeAll()
"""

menu_menu = {
    "flowerMenu": {
        "label": "Flower Menu",
        "entries": {
            "tool": {"label": "Flower Tool", "cmd": menu_tool},
            "clean": {"label": "Clean Scene", "cmd": menu_clean}
        }
    }
}


def create():
    for newmenu in menu_menu:
        menus = [m for m in pym.lsUI() if m.name() == "MayaWindow|" + newmenu]
        if menus:
            oMenu = menus[0]
            oMenu.deleteAllItems()
        else:
            oMenu = pym.menu(
                newmenu,
                label=menu_menu[newmenu]["label"], to=True, p='MayaWindow'
            )
        oMenu.makeDefault()
        entries = menu_menu[newmenu]["entries"]
        for entrie in entries:
            label = entries[entrie]["label"]
            cmd = entries[entrie]["cmd"]
            pym.menuItem(entrie, label=label, c=cmd)
