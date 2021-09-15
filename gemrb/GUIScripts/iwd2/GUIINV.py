# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003-2004 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#


# GUIINV.py - scripts to control inventory windows from GUIINV winpack

###################################################

import GemRB
import GUICommon
import GUICommonWindows
import InventoryCommon
from GUIDefines import *
from ie_stats import *
from ie_slots import *
from ie_spells import *
from ie_restype import RES_BAM

InventoryWindow = None

def InitInventoryWindow (Window):
	global InventoryWindow

	Window.AddAlias("WIN_INV")
	InventoryWindow = Window
	Window.SetVar("TopIndex", 0)

	#ground items scrollbar
	ScrollBar = Window.GetControl (66)
	ScrollBar.SetEvent (IE_GUI_SCROLLBAR_ON_CHANGE, RefreshInventoryWindow)

	# Ground Items (6)
	for i in range (5):
		Button = Window.GetControl (i+68)
		Button.SetEvent (IE_GUI_MOUSE_ENTER_BUTTON, InventoryCommon.MouseEnterGround)
		Button.SetEvent (IE_GUI_MOUSE_LEAVE_BUTTON, InventoryCommon.MouseLeaveGround)
		Button.SetVarAssoc ("Button", i + 68)
		Button.SetFont ("NUMFONT")

	Button = Window.GetControl (81)
	Button.SetTooltip (12011)
	Button.SetVarAssoc ("ItemButton", 6 + 81)
	Button.SetFont ("NUMFONT")
	Button.SetFlags (IE_GUI_BUTTON_ALIGN_RIGHT | IE_GUI_BUTTON_ALIGN_BOTTOM | IE_GUI_BUTTON_PICTURE, OP_OR)
	
	#major & minor clothing color
	Button = Window.GetControl (62)
	Button.SetFlags (IE_GUI_BUTTON_PICTURE,OP_OR)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, InventoryCommon.MajorPress)
	Button.SetTooltip (12007)

	Button = Window.GetControl (63)
	Button.SetFlags (IE_GUI_BUTTON_PICTURE,OP_OR)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, InventoryCommon.MinorPress)
	Button.SetTooltip (12008)

	#hair & skin color
	Button = Window.GetControl (82)
	Button.SetFlags (IE_GUI_BUTTON_PICTURE,OP_OR)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, InventoryCommon.HairPress)
	Button.SetTooltip (37560)

	Button = Window.GetControl (83)
	Button.SetFlags (IE_GUI_BUTTON_PICTURE,OP_OR)
	Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, InventoryCommon.SkinPress)
	Button.SetTooltip (37559)

	# paperdoll
	Button = Window.GetControl (50)
	Button.SetState (IE_GUI_BUTTON_LOCKED)
	Button.SetFlags (IE_GUI_BUTTON_NO_IMAGE | IE_GUI_BUTTON_PICTURE, OP_SET)
	Button.SetAction (InventoryCommon.OnAutoEquip, IE_ACT_DRAG_DROP_DST)

	# portrait
	Button = Window.GetControl (84)
	Button.SetState (IE_GUI_BUTTON_LOCKED)
	Button.SetFlags (IE_GUI_BUTTON_NO_IMAGE | IE_GUI_BUTTON_PICTURE, OP_SET)

	# armor class
	Label = Window.GetControl (0x10000038)
	Label.SetTooltip (17183)

	# hp current
	Label = Window.GetControl (0x10000039)
	Label.SetTooltip (17184)

	# hp max
	Label = Window.GetControl (0x1000003a)
	Label.SetTooltip (17378)

	# info label, game paused, etc
	# this is useless to us, message window is still visible
	Label = Window.GetControl (0x1000003f)
	Window.RemoveSubview(Label, True)
	# resize the win to hide the baked in BG for this useless control
	width, height = Window.GetSize()
	height -= 167 # read from the chu
	Window.SetSize(width, height)

	SlotCount = GemRB.GetSlotType (-1)["Count"]
	for slot in range (SlotCount):
		SlotType = GemRB.GetSlotType (slot+1)
		if SlotType["ID"]:
			Button = Window.GetControl (SlotType["ID"])
			Button.SetEvent (IE_GUI_MOUSE_ENTER_BUTTON, InventoryCommon.MouseEnterSlot)
			Button.SetEvent (IE_GUI_MOUSE_LEAVE_BUTTON, InventoryCommon.MouseLeaveSlot)
			Button.SetVarAssoc ("ItemButton", slot+1)
			Button.SetFont ("NUMFONT")
	
	for i in range (4):
		Button = Window.GetControl (109+i)
		Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, ChangeWeaponPressed)
		Button.SetVarAssoc("Equipped", i)
		Button.SetFlags (IE_GUI_BUTTON_RADIOBUTTON, OP_OR)
		#Why they mess up .chu's i don't know
		Button.SetSprites("INVBUT3", i, 0, 1, 2, 3)

	return

def ChangeWeaponPressed ():
	pc = GemRB.GameGetSelectedPCSingle ()
	Equipped = GemRB.GetVar ("Equipped")
	GemRB.SetEquippedQuickSlot (pc, Equipped, -1)
	return

#complete update
def UpdateInventoryWindow (Window = None):
	if Window == None:
		Window = GemRB.GetView("WIN_INV")

	pc = GemRB.GameGetSelectedPCSingle ()
	Container = GemRB.GetContainer (pc, 1)
	ScrollBar = Window.GetControl (66)
	Count = Container['ItemCount']
	if Count<1:
		Count=1
	ScrollBar.SetVarAssoc ("TopIndex", Count)
	Equipped = GemRB.GetEquippedQuickSlot (pc, 1)
	GemRB.SetVar ("Equipped", Equipped)
	for i in range (4):
		Button = Window.GetControl (109+i)
		Button.SetVarAssoc("Equipped", i)
	RefreshInventoryWindow ()
	# populate inventory slot controls
	SlotCount = GemRB.GetSlotType (-1)["Count"]
	for i in range (SlotCount):
		InventoryCommon.UpdateSlot (pc, i)
	return

InventoryCommon.UpdateInventoryWindow = UpdateInventoryWindow

ToggleInventoryWindow = GUICommonWindows.CreateTopWinLoader(2, "GUIINV", GUICommonWindows.ToggleWindow, InitInventoryWindow, UpdateInventoryWindow)
OpenInventoryWindow = GUICommonWindows.CreateTopWinLoader(2, "GUIINV", GUICommonWindows.OpenWindowOnce, InitInventoryWindow, UpdateInventoryWindow)

def RefreshInventoryWindow ():
	Window = InventoryWindow

	pc = GemRB.GameGetSelectedPCSingle ()

	# name
	Label = Window.GetControl (0x10000032)
	Label.SetText (GemRB.GetPlayerName (pc, 0))

	# paperdoll
	Button = Window.GetControl (50)
	Button.SetFlags (IE_GUI_BUTTON_CENTER_PICTURES, OP_OR)
	pdoll = GUICommonWindows.GetActorPaperDoll (pc)+"G11"
	if GemRB.HasResource (pdoll, RES_BAM):
		pal = [GemRB.GetPlayerStat (pc, c) for c in range(IE_METAL_COLOR, IE_HAIR_COLOR + 1)]
		Button.SetAnimation (pdoll, 0, 0, pal)

	# portrait
	Button = Window.GetControl (84)
	Button.SetPicture (GemRB.GetPlayerPortrait (pc, 0)["Sprite"])

	# encumbrance
	GUICommon.SetEncumbranceLabels (Window, 0x10000042, None, pc)

	# armor class
	ac = GemRB.GetPlayerStat (pc, IE_ARMORCLASS)
	Label = Window.GetControl (0x10000038)
	Label.SetText (str (ac))

	# hp current
	hp = GemRB.GetPlayerStat (pc, IE_HITPOINTS)
	Label = Window.GetControl (0x10000039)
	Label.SetText (str (hp))

	# hp max
	hpmax = GemRB.GetPlayerStat (pc, IE_MAXHITPOINTS)
	Label = Window.GetControl (0x1000003a)
	Label.SetText (str (hpmax))

	# party gold
	Label = Window.GetControl (0x10000040)
	Label.SetText (str (GemRB.GameGetPartyGold ()))

	Button = Window.GetControl (62)
	Color = GemRB.GetPlayerStat (pc, IE_MAJOR_COLOR, 1) & 0xFF
	Button.SetBAM ("COLGRAD", 0, 0, Color)

	Button = Window.GetControl (63)
	Color = GemRB.GetPlayerStat (pc, IE_MINOR_COLOR, 1) & 0xFF
	Button.SetBAM ("COLGRAD", 0, 0, Color)

	Button = Window.GetControl (82)
	Color = GemRB.GetPlayerStat (pc, IE_HAIR_COLOR, 1) & 0xFF
	Button.SetBAM ("COLGRAD", 0, 0, Color)

	Button = Window.GetControl (83)
	Color = GemRB.GetPlayerStat (pc, IE_SKIN_COLOR, 1) & 0xFF
	Button.SetBAM ("COLGRAD", 0, 0, Color)

	# update ground inventory slots
	TopIndex = Window.GetVar ("TopIndex")
	for i in range (6):
		if i<5:
			Button = Window.GetControl (i+68)
		else:
			Button = Window.GetControl (i+76)

		if GemRB.IsDraggingItem ()==1:
			Button.SetState (IE_GUI_BUTTON_FAKEPRESSED)
		else:
			Button.SetState (IE_GUI_BUTTON_ENABLED)
		Button.SetAction (InventoryCommon.OnDragItemGround, IE_ACT_DRAG_DROP_DST)

		Slot = GemRB.GetContainerItem (pc, i+TopIndex)
		if Slot == None:
			Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, None)
			Button.SetEvent (IE_GUI_BUTTON_ON_RIGHT_PRESS, None)
			Button.SetEvent (IE_GUI_BUTTON_ON_SHIFT_PRESS, None)
		else:
			Button.SetAction(InventoryCommon.OnDragItemGround, IE_ACT_DRAG_DROP_CRT)
			Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, InventoryCommon.OnDragItemGround)
			Button.SetEvent (IE_GUI_BUTTON_ON_RIGHT_PRESS, InventoryCommon.OpenGroundItemInfoWindow)
			Button.SetEvent (IE_GUI_BUTTON_ON_SHIFT_PRESS, InventoryCommon.OpenGroundItemAmountWindow)

		InventoryCommon.UpdateInventorySlot (pc, Button, Slot, "ground")

	#if actor is uncontrollable, make this grayed
	GUICommon.AdjustWindowVisibility (Window, pc, False)
	return

###################################################
# End of file GUIINV.py
