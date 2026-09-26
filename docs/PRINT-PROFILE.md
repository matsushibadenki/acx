# ACX Print Profile 0.1 (experimental)

[English](#english) · [日本語](#日本語) · [简体中文](#简体中文)

## English

The Print Profile describes an Agent-operated pipeline: Agent → Print API → RIP → Color Management → Queue → Printer. ACX governs discovery, preflight, authorization, commit and receipts; MCP, HTTPS, IPP or A2A bindings perform execution.

Providers publish print-specific data under a reverse-DNS key in a capability's `extensions` object. The initial `PrintIntent` schema distinguishes `required`, `preferred` and `automatic` requirements. A preflight must resolve that intent against the combined RIP, color, queue and printer capabilities and return an executable JobTicket or structured conflicts. Physical printing is consequential because it consumes supplies and creates an external physical effect.

Every stage carries the same `jobId` and `correlationId`; each retry has a new `attemptId`. Receipts distinguish raster export, delivery acceptance and verified device completion. A provider must not describe raster export alone as physical printing completion.

## 日本語

Print Profileは、Agent → Print API → RIP → Color Management → Queue → PrinterというAgent操作型パイプラインを記述します。ACXは発見、事前確認、承認、コミット、Receiptを管理し、MCP、HTTPS、IPP、A2A bindingが実行を担います。

Providerは印刷固有情報を、capabilityの`extensions`内にreverse-DNS keyで公開します。初期`PrintIntent` schemaは要求を`required`、`preferred`、`automatic`に分けます。preflightはRIP、色管理、キュー、印刷機の能力を組み合わせて意図を解決し、実行可能なJobTicketまたは構造化された不一致を返さなければなりません。物理印刷は消耗品を使い、外部へ物理的作用を与えるためconsequentialです。

全工程で同じ`jobId`と`correlationId`を引き継ぎ、再試行ごとに新しい`attemptId`を発行します。Receiptはラスター出力、配送受付、実機完了を区別します。ラスター出力だけを物理印刷完了として表現してはいけません。

## 简体中文

Print Profile描述由Agent操作的流水线：Agent → Print API → RIP → Color Management → Queue → Printer。ACX管理发现、预检、授权、提交和回执，MCP、HTTPS、IPP或A2A binding负责执行。

Provider在capability的`extensions`对象中，以反向域名key发布打印专用信息。初始`PrintIntent` schema将要求分为`required`、`preferred`和`automatic`。预检必须结合RIP、色彩管理、队列和打印机能力解析意图，并返回可执行的JobTicket或结构化冲突。实体打印会消耗材料并产生外部物理效果，因此属于consequential。

所有阶段使用相同的`jobId`和`correlationId`，每次重试使用新的`attemptId`。回执区分栅格输出、传送受理和设备确认完成。仅完成栅格输出时不得声明实体打印完成。
