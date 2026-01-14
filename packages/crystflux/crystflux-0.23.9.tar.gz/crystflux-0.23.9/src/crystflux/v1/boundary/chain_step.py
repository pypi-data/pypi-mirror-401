"""Structural trace step for method-chain observation.

This is a *trace*, not an executable plan:
- Do not store raw values, call arguments, or evaluated results here.
- Keep the data small and stable to support logging/serialization/debugging.

`op` is intentionally free-form. Projects may choose to standardize it (e.g., "get", "at",
"to_array", "map", "filter", "call:<method_name>"), but this module does not enforce a vocabulary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ChainStep:
    """
    A single step in a method-chain trace.

      This is a *structural trace*, not an executable plan:
      - Do NOT store raw values, call arguments, or evaluated results here.
      - Keep it stable for logging/serialization/debugging.

      Fields:
      - tag:
          "spawn" = a normal chain step produced by the outer shell's spawn().
          "bump"  = a post-VOID step produced by a VoidSentinel.bump() (still void).
      - op:
          A canonical operation label (symbolic), not a Python callable name.
          Recommended fixed vocabulary:
            "get", "at", "to_array", "map", "filter", "call:<method_name>"
          Use "call:<method_name>" for dream/unknown method access.
          Avoid adding new ad-hoc labels unless you also update the vocabulary docs/tests.
    """

    tag: Literal["spawn", "bump"]
    op: str


__all__ = ["ChainStep"]
