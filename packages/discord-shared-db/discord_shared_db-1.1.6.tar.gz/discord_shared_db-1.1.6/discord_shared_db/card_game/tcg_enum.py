# This file is part of discord-shared-db
#
# Copyright (C) 2026 CouchComfy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from enum import Enum

class Rarity(Enum):
    COMMON = 'common'
    UNCOMMON = 'uncommon'
    RARE = 'rare'

class CardModifiers(Enum):
    RAINBOW = 'rainbow'
    INVERTED = 'inverted'

class ManaType(Enum):
    MUSIC = 'music'
    ART = 'art'
    PROGRAMMING = 'programming'
    DESIGN = 'design'
    ANY = 'any'

class ActionCardType(Enum):
    INSTANT = 'instant'
    EQUIPMENT = 'equipment'