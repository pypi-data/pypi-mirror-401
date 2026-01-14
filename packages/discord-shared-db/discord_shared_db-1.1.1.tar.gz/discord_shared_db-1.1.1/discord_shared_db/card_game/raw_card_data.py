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

from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQEnum
from sqlalchemy import JSON, Column, ForeignKey, Integer, String

from discord_shared_db.base import Base
from discord_shared_db.card_game.tcg_enum import ActionCardType, ManaType, Rarity

class RawCard(Base):
    __tablename__ = "raw_cards"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    collect_number = Column(Integer, nullable=False)
    rarity = Column(SQEnum(Rarity), nullable=False)
    image_path = Column(String, nullable=False)
    flavor_text = Column(String)
    
    amount_pulled = Column(Integer, default=0)

    card_type = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": card_type,
        "polymorphic_identity": "base",
    }

class RawMove(Base):
    __tablename__ = "raw_moves"

    id = Column(Integer, primary_key=True)
    card_id = Column(String, ForeignKey("raw_cards.id"), nullable=False)

    name = Column(String, nullable=False)
    mana_cost = Column(JSON, nullable=False)
    effect_text = Column(String, nullable=False)
    effect_code = Column(String, nullable=False)

    card = relationship("RawCharacterCard", back_populates="moves")

 
class RawCharacterCard(RawCard):
    __tablename__ = "raw_character_cards"

    id = Column(String, ForeignKey("raw_cards.id"), primary_key=True)

    total_energy = Column(Integer, nullable=False)
    mana_type = Column(SQEnum(ManaType), nullable=False)

    moves = relationship(
        "RawMove",
        back_populates="card",
        cascade="all, delete-orphan",
    )

    __mapper_args__ = {
        "polymorphic_identity": "character",
    }

class RawActionCard(RawCard):
    __tablename__ = "raw_action_cards"

    id = Column(String, ForeignKey("raw_cards.id"), primary_key=True)

    action_card_type = Column(SQEnum(ActionCardType), nullable=False)
    mana_cost = Column(JSON)
    effect_text = Column(String)
    effect_code = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "action",
    }


class RawLocationCard(RawCard):
    __tablename__ = "raw_location_cards"

    id = Column(String, ForeignKey("raw_cards.id"), primary_key=True)

    mana_cost = Column(JSON)
    effect_text = Column(String)
    effect_code = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "location",
    }
    


