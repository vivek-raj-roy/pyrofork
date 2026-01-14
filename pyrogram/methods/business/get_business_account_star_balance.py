#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

import pyrogram
from pyrogram import raw


class GetBusinessAccountStarBalance:
    async def get_business_account_star_balance(
        self: "pyrogram.Client",
        business_connection_id: str,
    ) -> int:
        """
        Return the amount of Telegram Stars owned by a managed business account.

        Requires the `can_view_gifts_and_stars` business bot right.

        Parameters:
            business_connection_id (``str``):
                Unique identifier of business connection.

        Returns:
            ``int``: Stars balance.
        """

        # -----------------------------------------
        # Step 1: Resolve business connection info
        # -----------------------------------------
        connection_info = await self.get_business_connection(
            business_connection_id
        )

        # -----------------------------------------
        # Step 2: TEMPORARILY set business context
        # (this is the REAL FIX)
        # -----------------------------------------
        _old_bc: Optional[str] = getattr(
            self, "business_connection_id", None
        )

        self.business_connection_id = business_connection_id

        try:
            # -----------------------------------------
            # Step 3: Invoke MTProto request
            # -----------------------------------------
            r = await self.invoke(
                raw.functions.payments.GetStarsStatus(
                    peer=await self.resolve_peer(
                        connection_info.user.id
                    ),
                )
            )

        finally:
            # -----------------------------------------
            # Step 4: Restore previous context safely
            # -----------------------------------------
            if _old_bc is None:
                try:
                    delattr(self, "business_connection_id")
                except AttributeError:
                    pass
            else:
                self.business_connection_id = _old_bc

        # -----------------------------------------
        # Step 5: Return stars balance
        # -----------------------------------------
        return r.balance.amount
