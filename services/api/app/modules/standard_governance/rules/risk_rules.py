"""标准治理只读约束层：风险分级口径
Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/07_风险分级口径.md
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple


class RiskLevel(str, Enum):
    """risk_level"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKING = "blocking"


RISK_LEVEL_VALUES = [item.value for item in RiskLevel]

HIGH_RISK_KEYWORDS: Tuple[str, ...] = (
    "变更",
    "签证",
    "收款",
    "付款",
    "投诉",
    "质量",
    "返工",
    "赔偿",
    "延期",
    "承诺",
    "结算",
    "金额",
    "尾款",
)

BLOCKING_RISK_KEYWORDS: Tuple[str, ...] = (
    "阻断",
    "禁止入链",
)

RISK_KEYWORD_MAPPING: Dict[str, List[str]] = {
    "none": [],
    "low": [],
    "medium": [],
    "high": list(HIGH_RISK_KEYWORDS),
    "blocking": list(BLOCKING_RISK_KEYWORDS),
}


@dataclass(frozen=True)
class RiskKeywordMatch:
    blocking_risks: List[str]
    high_risks: List[str]
    risk_level: str
    risk_hints: List[str]


def match_risk_keywords(text: str) -> RiskKeywordMatch:
    blocking_risks = [keyword for keyword in BLOCKING_RISK_KEYWORDS if keyword in text]
    high_risks = [keyword for keyword in HIGH_RISK_KEYWORDS if keyword in text]
    if blocking_risks:
        return RiskKeywordMatch(
            blocking_risks=blocking_risks,
            high_risks=high_risks,
            risk_level=RiskLevel.BLOCKING.value,
            risk_hints=blocking_risks,
        )
    if high_risks:
        return RiskKeywordMatch(
            blocking_risks=blocking_risks,
            high_risks=high_risks,
            risk_level=RiskLevel.HIGH.value,
            risk_hints=high_risks,
        )
    return RiskKeywordMatch(
        blocking_risks=blocking_risks,
        high_risks=high_risks,
        risk_level=RiskLevel.NONE.value,
        risk_hints=[],
    )
