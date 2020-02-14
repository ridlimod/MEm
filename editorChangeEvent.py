import pymel.core as pm

# Get all model editors in Maya and reset the editorChanged event
for item in pm.lsUI(editors=True):
   if isinstance(item, pm.ui.ModelEditor):
       pm.modelEditor(item, edit=True, editorChanged="")
