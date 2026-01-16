# Copilot Instructions - Hezor Common

## Python Module Discoverability Best Practices

当编写 Python 模块时，遵循以下原则以提高模块的可发现性和可检查性（introspection）：

### 1. 完整的 Docstrings（NumPy Style）

**所有公共模块、类、函数和方法都必须包含 NumPy 风格的文档字符串：**

```python
"""Module description.

This module provides...
"""

class MyClass:
    """Class description.
    
    Attributes
    ----------
    attr : type
        Description of the attribute
    
    Examples
    --------
    >>> obj = MyClass()
    >>> obj.method("test")
    42
    """
    
    def method(self, param: str) -> int:
        """Method description.
        
        Parameters
        ----------
        param : str
            Parameter description
            
        Returns
        -------
        int
            Return value description
            
        Raises
        ------
        ValueError
            If param is invalid
            
        Examples
        --------
        >>> method("example")
        42
        """
        pass
```

**NumPy Style 关键要素：**
- 使用三引号 `"""`
- 简短摘要行（一句话）
- 空行后接详细描述
- `Parameters` / `Returns` / `Raises` / `Examples` 等章节
- 每个章节用 `---` 下划线分隔
- 类型和名称用 `: ` 分隔

### 2. 明确的 __all__ 导出列表

每个 `__init__.py` 必须定义 `__all__`，明确指定公共 API：

```python
__all__ = [
    "PublicClass",
    "public_function",
]
```

### 3. 完整的类型提示

所有函数签名必须包含类型提示，提高 IDE 支持和静态检查：

```python
from typing import Optional, List

def process_data(items: List[str], limit: Optional[int] = None) -> dict[str, int]:
    """Process data with type hints."""
    pass
```

### 4. 包元数据

在包的根 `__init__.py` 中定义元数据：

```python
__version__ = "0.1.0"
__author__ = "Your Name"
__all__ = ["exported_items"]
```

### 5. py.typed 标记

包含 `py.typed` 文件标记包支持 PEP 561 类型检查：

```
src/package_name/py.typed  # 空文件
```

### 6. 结构化导出

遵循清晰的导出层级：

- **根包** (`hezor_common/`) - 只导出版本和通用工具
- **功能模块** (`hezor_common.data_model/`) - 导出该功能域的所有公共 API
- **子模块** (`hezor_common.data_model.creations/`) - 导出具体实现

### 7. Pydantic 模型最佳实践

使用 Pydantic 时：

```python
from pydantic import BaseModel, Field, ConfigDict

class MyModel(BaseModel):
    """Model description."""
    
    model_config = ConfigDict(frozen=False, extra="forbid")
    
    field_name: str = Field(..., description="Field description")
```

### 8. 示例和测试

在 docstring 中包含实际可运行的示例：

```python
def my_function(x: int) -> int:
    """Double the input.
    
    Examples
    --------
    >>> my_function(5)
    10
    """
    return x * 2
```

## 代码组织原则

1. **单一职责** - 每个模块、类、函数只做一件事
2. **命名清晰** - 使用描述性名称，遵循 PEP 8
3. **避免循环导入** - 合理设计模块依赖关系
4. **最小化公共 API** - 只导出必要的接口
5. **向后兼容** - 谨慎修改公共 API

## 代码质量工作流

### 1. 开发前准备

```bash
# 安装开发依赖
uv sync --extra dev

# 确认 Python 版本和环境
python --version
which python
```

### 2. 编写代码时

**遵循的原则：**
- 先写文档字符串（NumPy Style）
- 添加完整的类型提示
- 编写可运行的示例代码
- 保持函数简短（<50 行）
- 使用有意义的变量名

**示例：**
```python
def calculate_total(items: list[dict[str, float]], tax_rate: float = 0.1) -> float:
    """Calculate total price including tax.
    
    Parameters
    ----------
    items : list[dict[str, float]]
        List of items with 'price' key
    tax_rate : float, optional
        Tax rate as decimal (default: 0.1 for 10%)
        
    Returns
    -------
    float
        Total price including tax
        
    Examples
    --------
    >>> items = [{"price": 100}, {"price": 200}]
    >>> calculate_total(items)
    330.0
    """
    subtotal = sum(item["price"] for item in items)
    return subtotal * (1 + tax_rate)
```

### 3. 提交前检查

**必须执行的检查：**

```bash
# 1. 格式化代码（使用 ruff 或 black）
ruff format .

# 2. 代码检查（使用 ruff）
ruff check . --fix

# 3. 类型检查（使用 pyright）
pyright

# 4. 运行测试
pytest

# 5. 检查测试覆盖率
pytest --cov=hezor_common --cov-report=term-missing
```

### 4. 提交信息规范

使用清晰的提交信息格式：

```bash
# 格式：<type>: <subject>
# 
# type 可选值：
# - feat: 新功能
# - fix: 修复 bug
# - docs: 文档更新
# - style: 代码格式调整
# - refactor: 重构代码
# - test: 测试相关
# - chore: 构建/工具相关

# 示例：
git commit -m "feat: add CreationModel with metadata support"
git commit -m "fix: correct type hint in SectionModel"
git commit -m "docs: update README with usage examples"
```

### 5. 添加新功能的完整流程

```bash
# 1. 创建功能分支
git checkout -b feature/new-model

# 2. 编写代码（包含 docstring、类型提示、测试）
# 3. 更新 __all__ 导出列表
# 4. 运行所有检查
ruff format . && ruff check . && pyright && pytest

# 5. 提交代码
git add .
git commit -m "feat: add new data model"

# 6. 合并到主分支
git checkout main
git merge feature/new-model

# 7. 更新版本并发布
make bump-minor  # 或 bump-patch
make publish
```

### 6. 代码审查检查清单

在提交 PR 或审查代码时，确认：

- [ ] 所有公共 API 都有 NumPy 风格的 docstring
- [ ] 所有函数都有完整的类型提示
- [ ] `__all__` 列表已更新
- [ ] 添加了单元测试（覆盖率 > 80%）
- [ ] 通过了所有代码检查（ruff、pyright）
- [ ] 文档已更新（README、CHANGELOG）
- [ ] 示例代码可以运行
- [ ] 没有破坏向后兼容性

### 7. 测试驱动开发（TDD）

**推荐的 TDD 流程：**

```python
# 1. 先写测试
def test_calculate_total():
    items = [{"price": 100}, {"price": 200}]
    assert calculate_total(items) == 330.0
    assert calculate_total(items, tax_rate=0.2) == 360.0

# 2. 运行测试（应该失败）
pytest test_module.py::test_calculate_total

# 3. 编写最小实现让测试通过
def calculate_total(items, tax_rate=0.1):
    subtotal = sum(item["price"] for item in items)
    return subtotal * (1 + tax_rate)

# 4. 重构代码（添加类型提示、docstring）
# 5. 再次运行测试确保通过
```

### 8. 性能和安全检查

```bash
# 性能分析
python -m cProfile -o profile.stats your_script.py
python -m pstats profile.stats

# 安全检查（检查依赖漏洞）
pip-audit

# 复杂度检查
radon cc src/ -a
```

## 版本管理

- 使用 `bump-my-version` 管理版本号
- 遵循语义化版本规范（SemVer）
- 每次发布前清理并重新构建

## 发布流程

```bash
# 1. 提交所有更改
git add .
git commit -m "Your changes"

# 2. 更新版本
make bump-patch  # 或 bump-minor, bump-major

# 3. 发布
make publish
```
