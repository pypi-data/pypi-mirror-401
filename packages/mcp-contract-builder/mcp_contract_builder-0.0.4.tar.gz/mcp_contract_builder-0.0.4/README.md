# mcp-contract-builder

Contract 生成工具（simple|auto|llm），不执行代码。输出仅短 digest，生成/覆盖 `/.codex/contract.json`。

工具：
- `contract_build(cwd, query, mode)`：`mode` 必填（simple|auto|llm）。返回 `contract_path`、`used_llm`、`difficulty`、`event_lines<=3`，必要时返回 `need_input`（不写文件）。

行为：
- simple：零 LLM，用规则生成合同（goal=用户一句；scope_allow 基于关键词匹配文件/目录；scope_deny=通用禁区；acceptance=通用 2–3 条；questions 为空）。
- llm：调用一次 LLM 生成完整合同（goal/scope_allow/scope_deny/acceptance/questions/risk_flags/context_budget），若 questions 非空则返回 need_input。
- auto：根据关键词/长度判定简单/复杂，选择 simple 或 llm。

存储：
- 合同写入 `/.codex/contract.json`
- 模板示例：`/.codex/contract.template.json`（需主会话/用户准备或复用已有模板）
