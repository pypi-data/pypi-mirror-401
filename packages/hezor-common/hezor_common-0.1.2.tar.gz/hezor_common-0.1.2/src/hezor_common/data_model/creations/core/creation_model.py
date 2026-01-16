"""Data models for creation XML structure (top-level model)."""

from typing import Optional
from pydantic import BaseModel, Field

from hezor_common.data_model.creations.core.chapter_model import ChapterModel


class Author(BaseModel):
    """Author information."""

    name: str = Field(..., description="作者名称")
    avatar: Optional[str] = Field(default=None, description="作者头像 URL")


class Contributor(BaseModel):
    """Contributor information."""

    name: str = Field(..., description="贡献者名称")
    avatar: Optional[str] = Field(default=None, description="贡献者头像 URL")


class CreationMeta(BaseModel):
    """Creation metadata with detailed information.

    创建路径约定: [domain]/[slug]/
    例如: food_beverage/single_store_profit_model/
    - domain: 领域标识(如 food_beverage 餐饮领域)
    - slug: 创建标识名(如 single_store_profit_model)
    - name: 单店盈利模型 (来自 meta.xml)
    - path: 完整路径，用于唯一标识(如 'food_beverage/single_store_profit_model')
    """

    name: str = Field(..., description="模型名称(来自 meta.xml)")
    description: str = Field(..., description="模型描述")
    author: Author = Field(..., description="作者信息")
    contributors: list[Contributor] = Field(
        default_factory=list, description="贡献者列表"
    )
    path: Optional[str] = Field(
        default=None,
        description="创建路径，如 'food_beverage/single_store_profit_model'",
    )
    domain: Optional[str] = Field(
        default=None, description="所属领域，如 'food_beverage'"
    )
    slug: Optional[str] = Field(
        default=None,
        description="创建标识名，如 'single_store_profit_model'(从路径解析)",
    )


class CreationSummary(BaseModel):
    """Creation summary content."""

    content: str = Field(..., description="总体描述内容")


class CreationModel(BaseModel):
    """
    Creation data model representing the top-level structure.

    A creation contains meta information, summary, and multiple chapters.
    Example: single_store_profit_model directory structure.
    """

    meta: CreationMeta = Field(..., description="模型元数据")
    summary: CreationSummary = Field(..., description="模型总结")
    chapters: list[ChapterModel] = Field(
        default_factory=list, description="所有章节列表"
    )

    def get_chapter_count(self) -> int:
        """获取章节数量."""
        return len(self.chapters)

    def get_chapter_by_name(self, name: str) -> Optional[ChapterModel]:
        """根据名称获取指定章节."""
        for chapter in self.chapters:
            if chapter.meta.name == name:
                return chapter
        return None

    def get_total_section_count(self) -> int:
        """获取所有章节中的小节总数."""
        return sum(chapter.get_section_count() for chapter in self.chapters)

    def get_all_dataset_names(self) -> list[str]:
        """获取所有章节中的数据集名称."""
        dataset_names = []
        for chapter in self.chapters:
            dataset_names.extend(chapter.get_all_dataset_names())
        return dataset_names

    def get_contributor_names(self) -> list[str]:
        """获取所有贡献者名称."""
        return [contributor.name for contributor in self.meta.contributors]

    def get_author_name(self) -> str:
        """获取作者名称."""
        return self.meta.author.name

    def get_sorted_chapters(self) -> list[ChapterModel]:
        """获取按序号排序的章节列表."""
        return sorted(
            self.chapters, key=lambda c: c.meta.serial if c.meta.serial else ""
        )

    def get_domain(self) -> Optional[str]:
        """获取领域名称."""
        return self.meta.domain

    def get_path(self) -> Optional[str]:
        """获取完整路径."""
        return self.meta.path
