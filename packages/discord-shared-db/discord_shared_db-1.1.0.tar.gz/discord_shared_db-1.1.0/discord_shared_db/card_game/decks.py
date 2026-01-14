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

from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String

from discord_shared_db.base import Base

class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"))
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)

    user = relationship("User", back_populates="decks")
    cards = relationship("DeckCard", cascade="all, delete-orphan")


class DeckCard(Base):
    __tablename__ = "deck_cards"

    deck_id = Column(Integer, ForeignKey("decks.id"), primary_key=True)
    user_card_id = Column(Integer, ForeignKey("user_cards.id"), primary_key=True)

    deck = relationship("Deck", back_populates="cards")
    user_card = relationship("UserCard")

