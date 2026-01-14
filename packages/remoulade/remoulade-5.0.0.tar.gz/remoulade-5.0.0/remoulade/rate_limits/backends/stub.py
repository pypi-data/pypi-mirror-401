# This file is a part of Remoulade.
#
# Copyright (C) 2017,2018 CLEARTYPE SRL <bogdan@cleartype.io>
#
# Remoulade is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# Remoulade is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from limits.storage import MemoryStorage

from ..backend import RateLimitBackend
from .utils import build_limiter


class StubBackend(RateLimitBackend):
    """In-memory backend using ``limits`` MemoryStorage."""

    def __init__(self, *, strategy: str = "sliding_window"):
        super().__init__()

        self.limiter = build_limiter(MemoryStorage(), strategy=strategy)

    def hit(self, limit, key: str) -> bool:
        return bool(self.limiter.hit(limit, key))
