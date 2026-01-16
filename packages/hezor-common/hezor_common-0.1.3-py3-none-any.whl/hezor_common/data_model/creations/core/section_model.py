"""Data models for section XML structure."""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Dataset(BaseModel):
    """Dataset information within a data query."""

    name: str = Field(..., description="数据集名称")
    description: Optional[str] = Field(default=None, description="数据集描述")


class ChartSuggestion(BaseModel):
    """Chart suggestion for data visualization."""

    description: str = Field(..., description="图表建议描述")


class DataQuery(BaseModel):
    """Data query specification including datasets and chart suggestions."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    datasets: list[Dataset] = Field(default_factory=list, description="数据集列表")
    chart_suggestion: Optional[ChartSuggestion] = Field(
        default=None, description="图表建议", alias="chart-suggestion"
    )


class TitleGuideline(BaseModel):
    """Guidelines for section title generation."""

    content: str = Field(..., description="标题指南内容")


class AnalysisGuideline(BaseModel):
    """Guidelines for analysis content generation."""

    content: str = Field(..., description="分析指南内容")


class SectionModel(BaseModel):
    """Section data model representing XML section structure.

    文件命名约定: [serial]__[slug].xml
    例如: 1_1__cash_overview.xml
    - serial: 1_1 (用于排序)
    - slug: cash_overview (文件标识名)
    - name: 总体现金流表现 (来自 XML section name 属性)
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: str = Field(..., description="小节名称(来自 XML section 标签的 name 属性)")
    serial: Optional[str] = Field(
        default=None, description="小节序号，如 '1_1'(从文件名解析)"
    )
    slug: Optional[str] = Field(
        default=None, description="文件标识名，如 'cash_overview'(从文件名解析)"
    )
    title_guideline: Optional[TitleGuideline] = Field(
        default=None, description="标题指南", alias="title-guideline"
    )
    data_query: Optional[DataQuery] = Field(
        default=None, description="数据查询", alias="data-query"
    )
    analysis_guideline: Optional[AnalysisGuideline] = Field(
        default=None, description="分析指南", alias="analysis-guideline"
    )

    def get_dataset_names(self) -> list[str]:
        """获取所有数据集名称."""
        if self.data_query and self.data_query.datasets:
            return [ds.name for ds in self.data_query.datasets]
        return []

    def has_chart_suggestion(self) -> bool:
        """检查是否有图表建议."""
        return (
            self.data_query is not None and self.data_query.chart_suggestion is not None
        )
