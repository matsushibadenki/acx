# ACX vs MCP / A2A

[English](#english) · [日本語](#日本語) · [简体中文](#简体中文)

## English

**ACX describes the terms of an action and binds its approved request to execution evidence.** MCP connects applications to tools and context; A2A supports collaboration between agents. ACX is designed to compose with both.

| Question | MCP | A2A | ACX draft 0.1 |
|---|---|---|---|
| Main focus | Access tools, resources, prompts | Exchange messages and delegate agent tasks | Declare outcome, authority, effects, risk, cost, evidence, recovery |
| Discovery | Tool listing and input/output schemas | Agent Card: skills, interfaces, security requirements | `/.well-known/acx.json`: capabilities and execution bindings |
| Acting | Tool invocation | Messages, tasks, status, artifacts | Preflight → authorize → commit, then execute through a binding |
| Approval and risk | Authorization facilities and tool annotations; host policy matters | Declared security schemes and task interactions | Declared approval/risk; consequential and critical actions require preflight |
| Evidence | Tool results | Task results and artifacts | Receipt schema with request hash; architecture also binds result, effects and cost |
| This repository | Example binding JSON | Example binding JSON | Schemas, validator, local HTTP lifecycle demo; adapters and signed profiles unfinished |

**Example:** MCP can call `print_document`; A2A can delegate a print task. ACX adds a portable contract for copies, effects, maximum cost, approval, expiry and a digest-bound commit, followed by a receipt. An application can implement similar controls with MCP/A2A; ACX proposes a shared vocabulary and lifecycle for those controls. Metadata alone does not enforce policy: the Provider must check it.

Try the [working demo](QUICKSTART.md). It uses an experimental local HTTP binding; it does not demonstrate MCP/A2A interoperability or standardized cryptographic verification.

## 日本語

**ACXは実行条件を記述し、承認したリクエストと実行証跡を結び付けます。** MCPはツールやコンテキストへの接続、A2Aはエージェント間の協働を扱い、ACXは両者との組み合わせを想定しています。

| 観点 | MCP | A2A | ACX draft 0.1 |
|---|---|---|---|
| 中心となる役割 | ツール・リソース・プロンプトの利用 | メッセージ交換・タスク委譲 | 成果・権限・影響・リスク・費用・証跡・回復の宣言 |
| 発見 | ツール一覧と入出力Schema | Agent Cardのスキル・接続先・認証要件 | `/.well-known/acx.json` の能力と実行Binding |
| 実行 | ツール呼び出し | メッセージ・タスク・状態・成果物 | 事前確認→承認→コミット後、Binding経由で実行 |
| 承認とリスク | 認可機構、ツール注釈、ホスト側ポリシー | セキュリティ方式の宣言とタスク対話 | 承認・リスクを宣言し、consequential／criticalでは事前確認が必須 |
| 証跡 | ツール結果 | タスク結果と成果物 | リクエストHashを持つReceipt。設計上は結果・影響・費用も結び付ける |
| このリポジトリ | BindingのJSON例 | BindingのJSON例 | Schema・検証CLI・ローカルHTTPデモ。アダプターと署名Profileは未実装 |

印刷なら、MCPがツールを呼び出し、A2Aが印刷タスクを委譲します。ACXは部数・影響・上限金額・承認・有効期限を共通形式で扱い、Digestでコミットを固定してReceiptへつなぎます。MCP/A2Aを使うアプリでも同様の制御は実装できます。ACXが提案するのは、その語彙と手順の共通化です。実際の制御はProviderの検証に依存します。

[動くデモ](QUICKSTART.md)は実験的なローカルHTTP実装です。MCP/A2Aとの相互運用や標準化された暗号検証を実証するものではありません。

## 简体中文

**ACX描述操作条件，并将已批准的请求与执行凭证绑定。** MCP连接工具和上下文，A2A支持代理之间的协作，ACX设计为与两者组合使用。

| 维度 | MCP | A2A | ACX draft 0.1 |
|---|---|---|---|
| 核心职责 | 使用工具、资源和提示词 | 消息交换和任务委派 | 声明结果、权限、影响、风险、费用、凭证和恢复 |
| 发现 | 工具列表及输入输出Schema | Agent Card中的技能、接口和安全要求 | `/.well-known/acx.json` 中的能力和执行Binding |
| 执行 | 调用工具 | 消息、任务、状态和产物 | 预检→授权→提交，然后通过Binding执行 |
| 授权与风险 | 授权机制、工具注解及宿主策略 | 安全方案声明和任务交互 | 声明授权和风险；consequential／critical操作必须预检 |
| 凭证 | 工具结果 | 任务结果和产物 | 包含请求Hash的回执；架构还绑定结果、影响和费用 |
| 本仓库 | Binding JSON示例 | Binding JSON示例 | Schema、验证CLI、本地HTTP演示；适配器和签名Profile尚未实现 |

以打印为例，MCP调用工具，A2A委派打印任务。ACX用共同格式描述份数、影响、费用上限、授权和有效期，通过Digest绑定提交，再提供回执。使用MCP/A2A的应用也能实现类似控制；ACX提出的是共同的词汇与流程。Provider必须实际执行检查，元数据本身不会强制执行策略。

[运行演示](QUICKSTART.md)使用实验性本地HTTP接口，尚未验证MCP/A2A互操作性或标准化的密码学验证。

## Sources / 出典 / 来源

Comparison checked 2026-09-26. MCP annotations are hints, and its authorization facilities should not be confused with approval of a specific transaction. See the official [MCP tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) and [MCP annotation discussion](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/). A2A discovery, security declarations, tasks and artifacts are described in the official [A2A 1.0 specification](https://a2a-protocol.org/v1.0.0/specification). ACX claims refer to this repository's [architecture](ARCHITECTURE.md), [schemas](../schemas), and [roadmap](../README.md#repository-roadmap).
