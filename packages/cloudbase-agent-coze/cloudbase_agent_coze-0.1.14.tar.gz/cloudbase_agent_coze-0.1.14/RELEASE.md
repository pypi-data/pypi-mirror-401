# Coze Package Release Guide

## 📦 发布系统

Coze 包使用 Cloudbase Agent 统一的发布系统，与 CrewAI、LangGraph 等其他框架完全一致。

## 🚀 发布方式

### 方式 1: 自动化发布所有包（推荐）

适用于发布新版本，一次性发布所有包（core, server, crewai, coze, langgraph 等）。

#### 发布到 TestPyPI（测试）

```bash
cd python-sdk
./scripts/release-cloudbase-py-test.sh --version 0.1.0
```

自动流程：
1. 创建 git tag: `cloudbase-py-test-v0.1.0`
2. 推送 tag 到 GitHub
3. 触发 GitHub Actions workflow
4. 自动构建所有包
5. 自动发布到 TestPyPI

验证：https://test.pypi.org/project/cloudbase-agent-coze/

#### 发布到 PyPI（正式）

```bash
cd python-sdk
./scripts/release-cloudbase-py.sh --version 0.1.0
```

自动流程：
1. 创建 git tag: `cloudbase-py-v0.1.0`
2. 推送 tag 到 GitHub
3. 触发 GitHub Actions workflow
4. 自动构建所有包
5. 自动发布到 PyPI

验证：https://pypi.org/project/cloudbase-agent-coze/

### 方式 2: 手动发布单个包

适用于只需要发布 Coze 包，不影响其他包。

#### 发布到 TestPyPI

```bash
# 设置凭据
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your_testpypi_token

# 发布
cd python-sdk
./scripts/manual-publish-single.sh \
  --package coze \
  --version 0.1.0 \
  --repo testpypi
```

#### 发布到 PyPI

```bash
# 设置凭据
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your_pypi_token

# 发布
cd python-sdk
./scripts/manual-publish-single.sh \
  --package coze \
  --version 0.1.0 \
  --repo pypi
```

#### 干跑模式（只构建不上传）

```bash
cd python-sdk
./scripts/manual-publish-single.sh \
  --package coze \
  --version 0.1.0 \
  --repo testpypi \
  --dry-run
```

## 📋 发布检查清单

发布前确认：

- [ ] 代码已合并到主分支
- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG 已更新
- [ ] 版本号符合语义化版本规范
- [ ] 无未提交的变更

## 🔄 发布流程详解

### 自动化发布流程

```
开发者本地
  ↓ 运行 release 脚本
创建 git tag
  ↓ 推送到 GitHub
触发 GitHub Actions
  ↓
├─ 检查 PyPI 版本冲突
├─ 转换命名空间（cloudbase_agent → cloudbase_agent）
├─ 设置版本号
├─ 构建所有包
├─ Twine 检查
└─ 上传到 PyPI/TestPyPI
  ↓
发布完成
```

### 手动发布流程

```
开发者本地
  ↓ 运行 manual-publish-single 脚本
创建临时工作目录
  ↓
├─ 复制源代码
├─ 转换命名空间（cloudbase_agent → cloudbase_agent）
├─ 设置版本号
├─ 构建单个包
├─ Twine 检查
└─ 上传到 PyPI/TestPyPI
  ↓
清理临时目录
  ↓
发布完成
```

## 📝 版本管理

### 语义化版本规范

- **Major (X.0.0)**: 不兼容的 API 变更
- **Minor (0.X.0)**: 向后兼容的功能新增
- **Patch (0.0.X)**: 向后兼容的 bug 修复

### 版本号策略

- 开发版本：`0.x.y`
- 稳定版本：`1.x.y`
- 所有包统一版本号

## 🛠️ 故障排查

### 问题：Tag 已存在

```
[ERROR] Tag cloudbase-py-v0.1.0 already exists.
```

解决：使用新的版本号或删除已有 tag

```bash
# 删除本地 tag
git tag -d cloudbase-py-v0.1.0

# 删除远程 tag
git push origin :refs/tags/cloudbase-py-v0.1.0
```

### 问题：PyPI 版本冲突

```
Version 0.1.0 already exists on PyPI for: cloudbase-agent-coze
```

解决：使用新的版本号

### 问题：Twine 上传失败

```
HTTPError: 403 Forbidden
```

解决：检查 TWINE_PASSWORD 环境变量是否正确

## 🔗 相关资源

- [GitHub Actions Workflow](/.github/workflows/release-cloudbase-py.yml)
- [Release Script](../../../scripts/release-cloudbase-py.sh)
- [Manual Publish Script](../../../scripts/manual-publish-single.sh)
- [PyPI Package](https://pypi.org/project/cloudbase-agent-coze/)
- [TestPyPI Package](https://test.pypi.org/project/cloudbase-agent-coze/)

## 💡 开发提示

### 单一源码维护

只需要维护 `packages/coze/src/cloudbase_agent/coze/` 中的代码：

```
packages/coze/src/cloudbase_agent/coze/
├── __init__.py
├── agent.py
└── converters.py
```

发布时会自动：
1. 转换命名空间：`cloudbase_agent` → `cloudbase_agent`
2. 重命名目录：`src/cloudbase_agent/` → `src/cloudbase_agent/`
3. 更新包名：`cloudbase-agent-coze` → `cloudbase-agent-coze`
4. 设置版本号
5. 构建和发布

### 不要手动维护两份代码

❌ **不推荐**：手动复制代码到单独的 PyPI 目录
✅ **推荐**：使用统一的发布系统自动转换

这样可以：
- 避免双重维护负担
- 避免遗漏同步
- 保证代码一致性
- 降低人为错误

## 📚 更多信息

查看项目根目录的发布文档了解更多细节。
