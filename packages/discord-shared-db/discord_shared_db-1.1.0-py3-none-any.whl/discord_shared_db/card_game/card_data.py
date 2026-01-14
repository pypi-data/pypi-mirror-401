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
from sqlalchemy import JSON, BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String

from discord_shared_db.base import Base

class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)

    raw_card_id = Column(String, ForeignKey("raw_cards.id"), nullable=False)

    pull_number = Column(Integer, nullable=False)
    modifiers = Column(JSON, default=list)  # foils, alt-art, buffs, etc.
    obtained_at = Column(DateTime, nullable=False)

    used_in_deck = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="cards")

