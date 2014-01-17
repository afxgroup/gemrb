/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2014 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 */

#include "TextContainer.h"

#include "Font.h"
#include "Palette.h"
#include "System/String.h"

namespace GemRB {

TextSpan::TextSpan(const String& string, Font* fnt, Palette* pal)
	: text(string)
{
	font = fnt;

	pal->acquire();
	palette = pal;
}

TextSpan::TextSpan(const String& string, Font* fnt, Palette* pal, const Region& /*rgn*/)
	: text(string)
{
	font = fnt;

	pal->acquire();
	palette = pal;
}



TextSpan::~TextSpan()
{
	palette->release();
}


TextContainer::TextContainer(Region& frame, Font* font, Palette* pal)
	: frame(frame), font(font)
{
	pal->acquire();
	pallete = pal;

}

TextContainer::~TextContainer()
{
	std::list<TextSpan*>::iterator it = spans.begin();
	for (; it != spans.end(); ++it) {
		delete *it;
	}
	pallete->release();
}

void TextContainer::AppendText(const String& text)
{
	AppendSpan(new TextSpan(text, font, pallete));
}

void TextContainer::AppendSpan(TextSpan* span)
{
	spans.push_back(span);
}

}
