# GemRB - Infinity Engine Emulator
# Copyright (C) 2003 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#
#character generation, import (GUICG24)
import GemRB

ImportWindow = 0

def OnLoad():
	global ImportWindow

	ImportWindow = GemRB.LoadWindow(24, "GUICG")
	ImportWindow.SetFlags (WF_ALPHA_CHANNEL, OP_OR)

	TextAreaControl = ImportWindow.GetControl(0)
	TextAreaControl.SetText(53605)

	FileButton = ImportWindow.GetControl(1)
	FileButton.SetText(53604)

	SavedGameButton = ImportWindow.GetControl(2)
	SavedGameButton.SetText(53602)

	CancelButton = ImportWindow.GetControl(3)
	CancelButton.SetText(13727)
	CancelButton.MakeEscape()

	FileButton.OnPress (FilePress)
	SavedGameButton.OnPress (GamePress)
	CancelButton.OnPress (CancelPress)
	ImportWindow.ShowModal(MODAL_SHADOW_GRAY)
	return

def FilePress():
	if ImportWindow:
		ImportWindow.Close ()
	GemRB.SetNextScript("ImportFile")
	return
	
def GamePress():
	if ImportWindow:
		ImportWindow.Close ()
	GemRB.SetNextScript("ImportGame")
	return

def CancelPress():
	if ImportWindow:
		ImportWindow.Close ()
	GemRB.SetNextScript("CharGen")
	return
