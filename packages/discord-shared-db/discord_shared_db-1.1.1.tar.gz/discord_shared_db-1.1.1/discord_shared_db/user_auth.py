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

from sqlalchemy import Enum as SQEnum
from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger, Column, ForeignKey, DateTime, String, UniqueConstraint

from discord_shared_db.base import Base
from discord_shared_db.auth_enums import AuthProviders


class UserAuth(Base):
    __tablename__ = "user_auth"


    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)

    provider = Column(SQEnum(AuthProviders), nullable=False)
    provider_account_id = Column(String, nullable=False)

    linked_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="auth_methods")

    __table_args__ = (
        UniqueConstraint("provider", "provider_account_id"),
    )


'''
user_auth
---------
user_id
provider      -- "steam" | "discord"
provider_id   -- SteamID64 or Discord user ID
linked_at

'''