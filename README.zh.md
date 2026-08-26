# dsh-model-manager

管理 DeepSeek Harness 中已启用的模型白名单，让模型选择器保持简洁。

> 状态：稳定

## 功能特性

- 查看已启用模型
- 启用/禁用模型
- 搜索模型
- 写入 llm-pi-ai provider models
- 原生 Cordis 命令插件

## 环境要求

- DeepSeek Harness (DSH) 0.1.1+
- OpenCode CLI（可选，用于 sync/catalog/bridge 功能）
- Node.js 22+
- Python 3.12+（仅用于备用 CLI 测试）

## 安装

将插件添加到 DSH profile：

```bash
cd ~/.dsh/profiles/tools
npm install @xucroyuri/dsh-model-manager
```

然后在 `cordis.patch.yml` 中添加：

```yaml
- insert:
    - id: model-manager
      name: '@xucroyuri/dsh-model-manager'
```

## 使用方法

```bash
dsh --profile tools models list
dsh --profile tools models enable deepseek/deepseek-v4-flash
dsh --profile tools models disable deepseek/deepseek-v4-flash
dsh --profile tools models search glm
```

## 开发

```bash
node --check src/index.js
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## 许可证

MIT
