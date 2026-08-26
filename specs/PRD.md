# dsh-model-manager PRD

## Problem Statement

DSH 的 llm-pi-ai provider 可能暴露大量模型，导致模型选择列表冗长、效率低。
用户需要一种简单方式只启用自己关心的模型。

## Goals

- 查看当前已启用模型。
- 启用/禁用指定 provider/model。
- 搜索模型。
- 写入 DSH `settings.yaml` 的 `llm-pi-ai.providers.<provider>.models`。

## Non-Goals

- 不直接调用模型。
- 不管理凭据。
- 不修改 DSH 核心代码。

## User Stories

- 作为 DSH 用户，我希望只显示我常用的几个模型。
- 作为 DSH 用户，我希望用命令启用/禁用模型，而不必手改 YAML。
