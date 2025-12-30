from typing import List

from sanity_check.sanity import SanityFailLevel
from ..sanity import Sanity


class PassNoFixSanity(Sanity):
    def check(self) -> List[str]:
        """Return an empty list for a pass sanity."""
        return []


class FailNoFixSanity(Sanity):
    def check(self) -> List[str]:
        return ["FAILED EXEMPLE SANITY"]


class FailAndFailingFixSanity(Sanity):
    def check(self) -> List[str]:
        return ["FAILED EXEMPLE SANITY"]

    def fix(self) -> None:
        print("TRYING TO FIX SANITY...")
        return

class FailAndFixSanity(Sanity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._has_run = False

    def check(self) -> List[str]:
        if not self._has_run:
            self._has_run = True
            return ["FAILED TRY TO FIX SANITY"]

        self._has_run = False
        return []

    def fix(self) -> None:
        print("FIXING SANITY...")
        return

