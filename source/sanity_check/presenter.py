from typing import Dict, List

from .sanity import Sanity
from .sanity_runner import get_run_sanity_result
from .sanity_interface import MainUI, ToCheckLine


class SanityPresenter:
    def __init__(self, sanitys: Dict[str, List[Sanity]], main_ui: MainUI, check_ui:ToCheckLine) -> None:
        pass

    def populate_main_ui(self) -> None:
        pass

    def create_listeners(self) -> None:
        pass

    def run_sanity_callback(self) -> None:
        pass

    def fix_sanity_callback(self) -> None:
        pass

    def run_all_sanitys_callback(self) -> None:
        pass

    def fix_all_sanitys_callback(self) -> None:
        pass
