/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2003 The GemRB Project
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
 *
 *
 */

#ifndef AREIMPORTER_H
#define AREIMPORTER_H

#include "MapMgr.h"

#include "Map.h" // proIterator
#include "MapReverb.h"

namespace GemRB {

class Animation;
class AnimationFactory;
class EffectQueue;

class AREImporter : public MapMgr {
private:
	DataStream* str;
	int bigheader;
	ieResRef WEDResRef;
	ieDword LastSave;
	ieDword AreaFlags;
	ieWord  AreaType, WRain, WSnow, WFog, WLightning, WUnknown;
	ieDword ActorOffset, EmbeddedCreOffset, AnimOffset, AnimCount;
	ieDword VerticesOffset;
	ieDword DoorsCount, DoorsOffset;
	ieDword ExploredBitmapSize, ExploredBitmapOffset;
	ieDword EntrancesOffset, EntrancesCount;
	ieDword SongHeader, RestHeader;
	ieWord  ActorCount, VerticesCount, AmbiCount;
	ieWord  ContainersCount, InfoPointsCount, ItemsCount;
	ieDword VariablesCount;
	ieDword ContainersOffset, InfoPointsOffset, ItemsOffset;
	ieDword AmbiOffset, VariablesOffset;
	ieDword SpawnOffset, SpawnCount;
	ieDword TileOffset, TileCount;
	ieDword NoteOffset, NoteCount;
	ieDword TrapOffset, TrapCount;  //only in ToB?
	proIterator piter; //iterator for saving projectiles
	ieDword EffectOffset;
	ieResRef Script;
	ieResRef Dream1, Dream2; //only in ToB
	ieByte AreaDifficulty;
public:
	AREImporter(void);
	~AREImporter(void);
	bool Open(DataStream* stream);
	bool ChangeMap(Map *map, bool day_or_night);
	Map* GetMap(const char* ResRef, bool day_or_night);
	int GetStoredFileSize(Map *map);
	/* stores an area in the Cache (swaps it out) */
	int PutArea(DataStream *stream, Map *map);
private:
	void AdjustPSTFlags(AreaAnimation*);
	void ReadEffects(DataStream *ds, EffectQueue *fx, ieDword EffectsCount);
	CREItem* GetItem();
	int PutHeader(DataStream *stream, const Map *map);
	int PutPoints(DataStream *stream, const std::vector<Point>&);
	int PutPoints(DataStream *stream, const Point *p, size_t count);
	int PutDoors(DataStream *stream, const Map *map, ieDword &VertIndex);
	int PutItems(DataStream *stream, const Map *map);
	int PutContainers(DataStream *stream, const Map *map, ieDword &VertIndex);
	int PutRegions(DataStream *stream, const Map *map, ieDword &VertIndex);
	int PutVertices(DataStream *stream, const Map *map);
	int PutSpawns(DataStream *stream, const Map *map);
	void PutScript(DataStream *stream, const Actor *ac, unsigned int index);
	int PutActors(DataStream *stream, const Map *map);
	int PutAnimations(DataStream *stream, const Map *map);
	int PutEntrances(DataStream *stream, const Map *map);
	int PutVariables(DataStream *stream, const Map *map);
	int PutAmbients(DataStream *stream, const Map *map);
	int PutMapnotes(DataStream *stream, const Map *map);
	int PutEffects( DataStream *stream, const EffectQueue *fxqueue);
	int PutTraps(DataStream *stream, const Map *map);
	int PutExplored(DataStream *stream, const Map *map);
	int PutTiles(DataStream *stream, const Map *map);
	int PutRestHeader(DataStream *stream, const Map *map);
	int PutSongHeader(DataStream *stream, const Map *map);
};

}

#endif
