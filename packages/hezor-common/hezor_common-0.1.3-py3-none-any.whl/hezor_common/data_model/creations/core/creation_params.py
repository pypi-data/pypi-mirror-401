"""Creation generation parameters model."""

from pydantic import BaseModel, Field


class CreationParams(BaseModel):
    """Creation generation parameters extracted from query.

    Attributes
    ----------
    subject : str
        主体，如"鮨大山"、"XX品牌"
    period : str
        报告周期，如"2025 年 3 月"、"2025 年第3期"
    data_coverage : str
        使用数据周期，格式 yyyyMMdd-yyyyMMdd 或 yyyyMM-yyyyMM
        例如：20251201-20251231 或 202512-202512

    Examples
    --------
    >>> params = CreationParams(
    ...     subject="鮨大山",
    ...     period="2025 年 12 月",
    ...     data_coverage="202512-202512"
    ... )
    """

    subject: str = Field(..., description="主体，如'鮨大山'")
    period: str = Field(..., description="报告周期，如'2025 年 12 月'")
    data_coverage: str = Field(
        ..., description="使用数据周期，格式 yyyyMMdd-yyyyMMdd 或 yyyyMM-yyyyMM"
    )
