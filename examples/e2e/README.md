# ACX End-to-End example

[English](#english) · [日本語](#日本語) · [简体中文](#简体中文)

## English

Start with the [5–10 minute quickstart](../../docs/QUICKSTART.md). From the repository root after installation:

```bash
python examples/e2e/run.py
python -m unittest discover -s examples/e2e -p 'test_*.py' -v
```

`provider.py` implements the local Provider; `client.py` makes actual HTTP requests and verifies the receipt; `run.py` manages their lifecycle; `test_e2e.py` checks success and refusal cases. There is no framework dependency beyond the repository's `jsonschema` package.

### Experimental wire profile

These routes and JSON envelopes are local conventions, not normative ACX endpoints. The Manifest advertises `type: other` and `profile: experimental-local-http`, because loopback HTTP is not the existing HTTPS binding. All POST bodies and responses are JSON.

| Step | Request | Response / check |
|---|---|---|
| discover | `GET /.well-known/acx.json` | Manifest validated against the existing schema |
| preflight | `POST /preflight` with `{"input":{"text":"Hello ACX","copies":1}}` | `preflightId`, `input`, `requestHash`, `preflightDigest`, capability/version, effects, cost, approval, recovery, `expiresAt` |
| authorize | `POST /authorize` with `preflightId`, `preflightDigest` | `authorization` token, scope, expiry; local policy permits at most two copies |
| commit | `POST /commit` with `preflightId`, `preflightDigest`, `authorization`, `input` | `commitId`, `preflightId`; rejects changed input, expiry, unrelated token, duplicate commit |
| execute | `POST /execute` with `commitId` | `result` and relative `receiptUrl`; only stored committed input is used |
| receipt | `GET <receiptUrl>` | Existing Receipt schema; client checks provider, capability, status, request hash and result hash |

The preflight expires after 120 seconds. `expiresAt` is Unix seconds in this demo. Its digest covers the entire preflight except `preflightDigest`, including the quote and expiry. Hash encoding is UTF-8 JSON with sorted keys, compact separators and unescaped Unicode (`provider.digest`); no text normalization is performed. This is a Python demo convention, not a standardized cross-language canonicalization profile.

Errors return `{"error":"..."}`: 400 invalid input, 403 policy/authorization failure, 404 unknown resource, 409 digest mismatch or duplicate commit, 410 expired preflight, 413 oversized body. Execute retries return the same result and receipt, including after expiry if execution already succeeded. New execution after expiry is rejected. Calls are serialized by the single-threaded server.

### What runs, and what remains

- [Done] Six stages over HTTP, Manifest/output/Receipt validation, bound approval, expiry checks, in-process replay handling, and seven HTTP tests.
- [Next] Agree on interoperable preflight/authorization/commit schemas and canonicalization with independent implementations.
- [Later] MCP/A2A adapters, authenticated deployment, signed evidence, durable state and recovery integration.

This simulator creates a job record in memory and charges USD 0.00. It labels the capability consequential to exercise mandatory preflight for a print-like action. There is no actual printing, file download, human approval, OAuth, cryptographic receipt signature, payment or rollback. `recovery.reversible` is false, so RECOVER is outside this six-stage example.

Use loopback only. Anyone able to call the local service can request policy approval; authorization tokens and commit IDs act as temporary bearer capabilities. Receipt IDs are unguessable lookup keys, not authenticated access. Hash verification establishes internal consistency, not Provider authenticity. State and replay protection disappear on restart. A production integration needs an agreed binding, authenticated callers, audience/scope controls, durable transactions and receipt/signature policy before adding real side effects.

## 日本語

[クイックスタート](../../docs/QUICKSTART.md)に従ってインストール後、上の2コマンドでデモとテストを実行できます。`provider.py` がProvider、`client.py` がHTTP呼び出しとReceipt照合、`run.py` が起動・終了、`test_e2e.py` が正常系と拒否ケースを担当します。

上の表はデモ専用APIです。`GET /.well-known/acx.json` で発見し、`/preflight`、`/authorize`、`/commit`、`/execute` の順でPOSTし、`receiptUrl` をGETします。POSTはJSONです。Preflight IDとDigestを承認・コミットに引き渡し、コミットには承認Tokenと元の入力も必要です。実行には `commitId` を使い、Providerが保持する確定済み入力だけを実行します。

見積もりは120秒で失効し、`expiresAt` はUnix秒です。Digestは自身のフィールドを除いたPreflight全体を対象にします。Hashはキー順を整えた空白なしのUTF-8 JSONで計算し、Unicodeはエスケープせず、文字列の正規化も行いません。これはPythonデモの規約で、言語間の標準形式ではありません。エラーはJSONで、400は入力不正、403は承認拒否、404は未検出、409は不一致・重複コミット、410は期限切れ、413はサイズ超過です。実行の再試行では同じ結果とReceiptを返します。処理は単一スレッドで直列化しています。

- [Done] HTTPによる6段階、Schema検証、承認の紐付け、期限と重複の制御、7件のテスト。
- [Next] 独立した実装との相互運用を通じたPreflight・承認・CommitのSchemaと正規化方式の合意。
- [Later] MCP/A2Aアダプター、認証、署名、永続化、回復処理。

印刷を模したメモリ上のジョブを作成し、費用は0ドルです。必須Preflightを示すためリスクをconsequentialにしています。実際の印刷、ダウンロード、人間の承認、OAuth、署名、決済、ロールバックはありません。回復不可の宣言に合わせ、RECOVERは対象外です。

ループバック専用です。ローカルに接続できる利用者は自動ポリシー承認を要求できます。TokenとCommit IDは一時的なBearer権限で、Receipt IDは推測困難な検索キーです。Hash照合で確認するのは整合性であり、Providerの真正性ではありません。再起動で状態とリプレイ防止情報は消えます。本番で副作用を伴う処理につなぐ場合は、Bindingの合意、呼び出し元認証、権限の対象・範囲、永続化、Receipt署名ポリシーが必要です。

## 简体中文

按[快速入门](../../docs/QUICKSTART.md)安装后，使用上方两个命令运行演示与测试。`provider.py` 实现Provider，`client.py` 发送HTTP请求并核验回执，`run.py` 管理启动和关闭，`test_e2e.py` 验证成功和拒绝场景。

上表中的API仅用于演示。通过 `GET /.well-known/acx.json` 发现能力，然后依次POST到 `/preflight`、`/authorize`、`/commit`、`/execute`，最后GET `receiptUrl`。POST使用JSON。授权与提交需要传递Preflight ID和Digest；提交还需要授权Token和原始输入。执行只传 `commitId`，Provider使用已保存的提交输入。

预检有效期为120秒，`expiresAt` 使用Unix秒。Digest覆盖除自身字段外的整个Preflight。Hash使用按键排序、无多余空格、不转义Unicode的UTF-8 JSON，不进行文本规范化。这只是Python演示约定，并非跨语言标准。错误以JSON返回：400输入无效，403授权拒绝，404资源不存在，409摘要不匹配或重复提交，410过期，413请求过大。重复执行会返回相同结果和回执。服务器通过单线程串行处理请求。

- [Done] HTTP六阶段、Schema验证、授权绑定、有效期和重复执行控制、七项测试。
- [Next] 与独立实现共同确定预检、授权、提交Schema及规范化规则。
- [Later] MCP/A2A适配器、认证、签名、持久化和恢复处理。

示例在内存中创建模拟打印任务，费用为0美元。风险标为consequential以展示强制预检。没有实际打印、下载、人工批准、OAuth、签名、支付或回滚。由于声明不可恢复，RECOVER不在此示例范围内。

仅限本地回环接口。能够访问服务的用户均可请求自动策略授权。Token和Commit ID是临时Bearer权限；Receipt ID是难以猜测的查询键。Hash检查证明内部一致性，不证明Provider身份。重启会清空状态和防重放记录。在连接真实副作用前，需要确定Binding、调用者认证、权限受众与范围、持久事务以及回执签名策略。
