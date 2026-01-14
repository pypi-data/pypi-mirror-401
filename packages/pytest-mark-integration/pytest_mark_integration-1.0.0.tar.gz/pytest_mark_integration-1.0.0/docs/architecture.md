# pytest-mark-integration 架构设计文档

## 项目概述

`pytest-mark-integration` 是一个 pytest 插件，用于自动标记和管理集成测试。该插件通过自动检测测试文件路径中的 "integration" 关键字，自动为相关测试添加 `integration` 标记，并提供灵活的命令行选项和配置来控制集成测试的执行行为。

## 核心功能

### 1. 自动标记机制

**功能描述**：
- 插件会自动为测试文件路径中包含 "integration" 关键字的测试用例添加 `@pytest.mark.integration` 标记
- 支持手动使用 `@pytest.mark.integration` 装饰器显式标记测试
- 路径检测是绝对路径级别的，只要测试文件的绝对路径中包含 "integration" 即可

**实现方式**：
- 使用 `pytest_collection_modifyitems` hook 在测试收集阶段自动添加标记
- 检查每个测试项的 `fspath` 属性（文件路径）
- 使用字符串匹配判断路径中是否包含 "integration"

**示例场景**：
```
✓ tests/integration/test_api.py          # 会被标记
✓ tests/api_integration_test.py          # 会被标记
✓ integration/test_database.py           # 会被标记
✗ tests/unit/test_utils.py               # 不会被标记
```

### 2. 命令行选项

**提供两个互斥的命令行选项**：

#### `--with-integration`
- 显式运行带有 `integration` 标记的测试
- 覆盖配置文件中的默认行为
- 适用场景：CI/CD 中专门的集成测试阶段

#### `--without-integration`
- 显式跳过带有 `integration` 标记的测试
- 覆盖配置文件中的默认行为
- 适用场景：快速的单元测试执行

### 3. 配置选项

**通过 pytest.ini 或 pyproject.toml 配置默认行为**：

#### `run_integration_by_default`
- **类型**：布尔值
- **默认值**：`True`
- **含义**：当没有指定 `--with-integration` 或 `--without-integration` 时的默认行为
  - `True`：默认运行集成测试（等同于 `--with-integration`）
  - `False`：默认跳过集成测试（等同于 `--without-integration`）

#### `fail_fast_on_unit_test_failure`
- **类型**：布尔值
- **默认值**：`True`
- **含义**：当非集成测试失败时，是否跳过后续的集成测试
  - `True`：单元测试失败后不运行集成测试
  - `False`：无论单元测试是否失败，都按计划运行集成测试

**配置示例**：

```ini
# pytest.ini
[pytest]
run_integration_by_default = true
fail_fast_on_unit_test_failure = true
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
run_integration_by_default = true
fail_fast_on_unit_test_failure = true
```

### 4. 测试排序

**功能描述**：
- 集成测试始终在非集成测试（单元测试）之后运行
- 确保快速反馈循环：先运行快速的单元测试，后运行慢速的集成测试

**实现方式**：
- 使用 `pytest_collection_modifyitems` hook 对收集到的测试项进行排序
- 排序规则：
  - 没有 `integration` 标记的测试排在前面（优先级 0）
  - 有 `integration` 标记的测试排在后面（优先级 1）

### 5. 失败快速停止

**功能描述**：
- 当 `fail_fast_on_unit_test_failure = True` 时，如果任何单元测试失败，后续的集成测试会被自动跳过
- 这可以节省 CI/CD 时间，避免在基础功能有问题时还运行耗时的集成测试

**实现方式**：
- 使用 `pytest_runtest_makereport` hook 捕获测试失败事件
- 维护一个全局状态标志，记录单元测试是否失败
- 在 `pytest_runtest_setup` hook 中检查这个标志，决定是否跳过集成测试

### 6. 与其他 pytest 插件集成

#### pytest-cov（代码覆盖率）
- 默认情况下，集成测试不计入代码覆盖率统计
- 理念：单元测试应该已经覆盖了所有代码，集成测试主要验证系统间的交互
- 可以通过 `--integration-cover` 选项启用集成测试的覆盖率统计

#### pytest-timeout（超时控制）
- 支持为集成测试设置独立的超时时间
- 使用 `--integration-timeout` 选项指定超时秒数
- 使用 `--integration-timeout-method` 选项指定超时方法（thread 或 signal）

#### pytest-xdist（并行执行）
- 兼容 pytest-xdist 的并行测试执行
- 测试排序在每个 worker 节点上都会生效
- 注意：在并行模式下，fail-fast 行为可能不完全一致（因为测试分散在多个进程中）

## 设计决策记录

### ADR-001: 自动标记范围

**决策**：基于文件路径自动标记 + 支持手动标记

**理由**：
- ✅ **易用性**：开发者无需记住为每个集成测试添加装饰器
- ✅ **灵活性**：仍然支持手动标记，覆盖特殊场景
- ✅ **约定优于配置**：遵循约定的项目结构（如 `tests/integration/`）自动获得正确的标记
- ⚠️ **潜在误判**：文件路径中偶然包含 "integration" 可能导致误标记（概率很低）

**替代方案**：
- 纯手动标记：过于繁琐，容易遗漏
- 仅基于目录：不够灵活，无法处理 `test_api_integration.py` 这样的命名

### ADR-002: 默认运行行为

**决策**：`run_integration_by_default = True`（默认运行集成测试）

**理由**：
- ✅ **最小惊讶原则**：开发者运行 `pytest` 期望运行所有测试
- ✅ **完整性优先**：确保集成测试不会被忘记
- ✅ **CI/CD 友好**：在 CI 环境中，通常希望运行全部测试
- ⚠️ **本地开发速度**：开发者可以通过配置或 `--without-integration` 加速本地测试

**对比**：
- `pytest-integration-mark` 默认跳过集成测试（假设集成测试需要外部依赖）
- 我们的插件假设项目已经设置好了测试环境，默认运行更符合"测试越多越好"的理念

### ADR-003: 失败快速停止默认启用

**决策**：`fail_fast_on_unit_test_failure = True`（默认启用）

**理由**：
- ✅ **快速反馈**：单元测试失败意味着基础功能有问题，集成测试大概率也会失败
- ✅ **节省资源**：避免在 CI 中浪费时间运行注定失败的集成测试
- ✅ **清晰的错误定位**：先修复单元测试错误，再处理集成测试问题
- ⚠️ **可能隐藏问题**：某些集成测试的失败可能与单元测试失败无关

**可配置性**：用户可以设置 `fail_fast_on_unit_test_failure = False` 禁用此行为

### ADR-004: 测试排序始终启用

**决策**：集成测试始终在单元测试之后运行，不可配置

**理由**：
- ✅ **最佳实践**：这是测试金字塔的标准实践
- ✅ **快速反馈**：快速的测试先运行，慢速的测试后运行
- ✅ **简化配置**：减少配置选项，降低复杂度
- ⚠️ **灵活性降低**：某些场景可能希望先运行集成测试（极少见）

### ADR-005: 与 pytest-cov 集成

**决策**：默认情况下集成测试不计入覆盖率，提供 `--integration-cover` 开关

**理由**：
- ✅ **覆盖率准确性**：单元测试应该已经覆盖所有代码
- ✅ **性能优化**：跳过集成测试的覆盖率统计可以加速测试
- ✅ **清晰的职责划分**：单元测试负责覆盖率，集成测试负责端到端验证
- ✅ **灵活性**：仍然可以通过选项启用集成测试覆盖率

### ADR-006: 使用 uv 而非 poetry

**决策**：使用 uv 作为包管理工具

**理由**：
- ✅ **速度**：uv 比 poetry 快 10-100 倍
- ✅ **兼容性**：uv 完全兼容 pyproject.toml 和 pip
- ✅ **简洁性**：uv 更轻量级，依赖更少
- ✅ **未来趋势**：uv 是 Rust 编写的下一代 Python 包管理工具

### ADR-007: Apache-2.0 许可证

**决策**：使用 Apache-2.0 开源许可证

**理由**：
- ✅ **商业友好**：允许商业使用、修改和分发
- ✅ **专利保护**：提供明确的专利授权条款
- ✅ **社区信任**：被广泛接受和信任的许可证
- ✅ **兼容性**：与大多数其他开源许可证兼容

## 技术实现细节

### pytest Hook 使用

1. **`pytest_addoption`**：添加命令行选项
   ```python
   parser.addoption('--with-integration', action='store_true')
   parser.addoption('--without-integration', action='store_true')
   ```

2. **`pytest_configure`**：注册标记和读取配置
   ```python
   config.addinivalue_line("markers", "integration: mark test as integration test")
   ```

3. **`pytest_collection_modifyitems`**（使用 `trylast=True`）：
   - 自动添加标记
   - 排序测试项
   - 添加 `no_cover` 和 `timeout` 标记（如果相应插件已安装）

4. **`pytest_runtest_setup`**（使用 `tryfirst=True`）：
   - 根据命令行选项和配置决定是否跳过测试
   - 检查 fail-fast 标志

5. **`pytest_runtest_makereport`**：
   - 捕获测试失败事件
   - 设置 fail-fast 标志

### 配置优先级

1. **命令行选项**（最高优先级）
   - `--with-integration` → 运行集成测试
   - `--without-integration` → 跳过集成测试

2. **配置文件**（中等优先级）
   - `run_integration_by_default = true/false`

3. **默认行为**（最低优先级）
   - 运行集成测试（`run_integration_by_default` 默认为 `True`）

### 标记检测逻辑

```python
def should_mark_as_integration(test_item):
    """
    判断测试项是否应该被标记为 integration
    """
    # 1. 检查是否已经有手动标记
    if test_item.get_closest_marker('integration'):
        return True
    
    # 2. 检查文件路径
    test_path = str(test_item.fspath)
    if 'integration' in test_path.lower():
        return True
    
    return False
```

## 项目结构

```
pytest-mark-integration/
├── src/
│   └── pytest_mark_integration/
│       ├── __init__.py           # 版本信息和导出
│       └── plugin.py             # 核心插件实现
├── tests/
│   ├── test_auto_marking.py     # 测试自动标记功能
│   ├── test_cli_options.py      # 测试命令行选项
│   ├── test_configuration.py    # 测试配置选项
│   ├── test_sorting.py          # 测试排序功能
│   ├── test_fail_fast.py        # 测试 fail-fast 功能
│   └── test_integration_example.py  # 示例集成测试
├── docs/
│   └── architecture.md          # 本文档
├── README.md                    # 用户文档
├── LICENSE                      # Apache-2.0 许可证
├── CHANGELOG.md                 # 版本变更记录
├── pyproject.toml               # 项目配置（uv 管理）
├── Makefile                     # 开发常用命令
└── .gitignore                   # Git 忽略文件
```

## 发布到 PyPI

### 发布流程

1. **更新版本号**：在 `src/pytest_mark_integration/__init__.py` 中更新 `__version__`
2. **更新 CHANGELOG**：记录本次发布的变更
3. **构建分发包**：`make build`（生成 wheel 和 sdist）
4. **发布到 TestPyPI**：`make publish-test`（测试发布）
5. **发布到 PyPI**：`make publish`（正式发布）

### PyPI 元数据

- **包名**：`pytest-mark-integration`
- **分类标签**：
  - `Development Status :: 4 - Beta`
  - `Framework :: Pytest`
  - `Intended Audience :: Developers`
  - `License :: OSI Approved :: Apache Software License`
  - `Programming Language :: Python :: 3`
  - `Programming Language :: Python :: 3.8`
  - `Programming Language :: Python :: 3.9`
  - `Programming Language :: Python :: 3.10`
  - `Programming Language :: Python :: 3.11`
  - `Programming Language :: Python :: 3.12`
  - `Topic :: Software Development :: Testing`

## 未来扩展

### 可能的功能增强

1. **多级集成测试分类**
   - `@pytest.mark.integration(level='quick')`
   - `@pytest.mark.integration(level='slow')`
   - 支持更细粒度的控制

2. **自定义路径模式**
   - 允许用户配置自定义的路径匹配规则
   - 例如：`integration_path_patterns = ["integration", "e2e", "system"]`

3. **依赖管理**
   - 声明测试之间的依赖关系
   - 例如：数据库集成测试依赖于数据库迁移测试

4. **详细的测试报告**
   - 区分单元测试和集成测试的统计信息
   - 单独显示每种测试类型的执行时间

5. **动态标记策略**
   - 基于测试运行时行为动态添加标记
   - 例如：检测到数据库连接则自动标记为集成测试

## 参考资料

- [pytest 官方文档](https://docs.pytest.org/)
- [pytest-integration](https://github.com/jbwdevries/pytest-integration) - 参考实现
- [pytest-integration-mark](https://github.com/Barbora-Data-Science/pytest-integration-mark) - 参考实现
- [pytest 插件开发指南](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)
- [测试金字塔理论](https://martinfowler.com/articles/practical-test-pyramid.html)
