from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

from .sanity import Sanity
from .exceptions import SanityDependencyError


class SanityStatus(Enum):
    CHECK_FAIL = auto()
    EXECUTION_FAIL = auto()
    PASSED = auto()
    RESOLVED = auto()


@dataclass
class SanityResult:
    result: List[str] = field(default_factory=list)
    status: SanityStatus = None


def run_sanity(sanity: Sanity) -> List[str]:
    result: List[str] = []

    for sanity in sanity.DEPENDENCY:
        result = run_sanity(sanity)
        if result:
            raise SanityDependencyError(sanity.nice_name)
    
    if not result:
        result = sanity.check()

    return result


def get_sanity_run_result(sanity: Sanity) -> SanityResult:
    sanity_result = SanityResult()

    try:
        result = run_sanity(sanity)

        if not result:
            sanity_result.status = SanityStatus.PASSED
            return sanity_result
        
        sanity_result.result = result
        sanity_result.status = SanityStatus.CHECK_FAIL

    except SanityDependencyError as err:
        sanity_result.result = [f"Sanity '{str(err)}' has failed. Can't perform current check."]
        sanity_result.status = SanityStatus.CHECK_FAIL

    except Exception as err:
        sanity_result.result = [f"Execution Failed :\n{str(err)}"]
        sanity_result.status = SanityStatus.EXECUTION_FAIL

    return sanity_result


def get_sanity_result(sanity: Sanity) -> SanityResult:
    sanity_result = SanityResult()

    try:
        result = run_sanity(sanity)

        if not result:
            sanity_result.status = SanityStatus.PASSED
            return sanity_result

        if not sanity.has_fix:
            sanity_result.status = SanityStatus.CHECK_FAIL
            sanity_result.result = result
            return sanity_result

        sanity.fix()
        result = run_sanity(sanity)

        if not result:
            sanity_result.status = SanityStatus.RESOLVED
            return sanity_result
        
        sanity_result.result = result
        sanity_result.status = SanityStatus.CHECK_FAIL

    except SanityDependencyError as err:
        sanity_result.result = [f"Sanity '{str(err)}' has failed. Can't perform current check."]
        sanity_result.status = SanityStatus.CHECK_FAIL

    except Exception as err:
        sanity_result.result = [f"Execution Failed :\n{str(err)}"]
        sanity_result.status = SanityStatus.EXECUTION_FAIL

    return sanity_result
