# ACX Quickstart — 5–10 minutes

[English](#english) · [日本語](#日本語) · [简体中文](#简体中文)

## English

Run a minimal Provider and observe `discover → preflight → authorize → commit → execute → receipt` over real local HTTP. Requires Python 3.10+, pip, and a checkout of this repository. Run all commands from the repository root. No API keys, LLM, printer, payment account, or Docker needed.

### 1. Install (1–2 minutes)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Windows PowerShell: use `py -3 -m venv .venv`, then `.venv\Scripts\Activate.ps1` instead of the first two commands.

### 2. Run the complete demo (1 minute)

```bash
python examples/e2e/run.py
```

This starts a Provider on an available loopback port, runs the client, and stops the server automatically. Expect six `PASS` lines followed by a JSON receipt:

```text
1 discover  PASS — org.example.print.simulate
2 preflight PASS — maximum USD 0.00
3 authorize PASS — local policy approved
4 commit    PASS — bound to approved preflight
5 execute   PASS — simulated job <random ID>
6 receipt   PASS — request/result hashes verified
```

### 3. Keep the Provider running (2 minutes)

Terminal A, with the environment activated:

```bash
python examples/e2e/provider.py --port 8765
```

Terminal B, from the repository root with the same environment activated:

```bash
curl http://127.0.0.1:8765/.well-known/acx.json
python examples/e2e/client.py --base-url http://127.0.0.1:8765
```

Stop the Provider with Ctrl+C. If port 8765 is busy, change both commands to 8766. If `jsonschema` is missing, repeat installation in the active environment. A connection error means the Provider is not running or the port differs. Restarting the Provider clears all demo state; rerun the entire client.

### 4. Verify and adapt (1–3 minutes)

```bash
python -m unittest discover -s examples/e2e -p 'test_*.py' -v
python -m acx validate examples/print-manifest.json
```

The seven tests cover the complete flow, changed inputs/digests, missing or unrelated authorization, policy denial, invalid input, expiry, replay, and altered receipts. Edit `request` in `client.py` to change the text. Three copies demonstrate a policy rejection: the input schema allows up to ten, but authorization permits only two.

Read the [demo API and limitations](../examples/e2e/README.md) before adapting the Provider. This is an experimental local HTTP profile: it simulates printing in memory, uses a local automatic approval policy, and produces an unsigned receipt. The existing print manifest describes a separate illustrative service; the running demo serves its own schema-valid manifest.

## 日本語

Python 3.10以上とpipを用意し、取得したリポジトリのルートで実行します。APIキーやプリンターは不要です。所要時間は5〜10分です。

1. 上の「1. Install」で仮想環境を作成・有効化し、`python -m pip install -e .` を実行します。Windowsでは記載のPowerShell用コマンドを使います。
2. `python examples/e2e/run.py` を実行します。空いているローカルポートでProviderが起動し、6段階をHTTPで実行します。6行の `PASS` とJSONのReceiptが表示され、自動終了すれば成功です。
3. 常駐させる場合は `python examples/e2e/provider.py --port 8765` を実行し、別のターミナルで同じ仮想環境を有効化して `python examples/e2e/client.py --base-url http://127.0.0.1:8765` を実行します。Manifestは `http://127.0.0.1:8765/.well-known/acx.json` で取得できます。終了はCtrl+Cです。
4. 上の「4. Verify and adapt」のテストコマンドで拒否ケースも確認します。`client.py` の `request` を変更できます。`copies: 3` は入力検証を通りますが、自動承認ポリシーに拒否されます。

ポートが使用中ならProviderとClientを両方8766へ変更してください。`jsonschema` が見つからない場合は仮想環境内で再インストールします。接続エラー時はProviderの起動とポートを確認してください。再起動で状態が消えるため、Clientを最初から実行し直します。

これは印刷・課金を行わないメモリ上のシミュレーターです。承認はローカルの自動ポリシー、Receiptは署名なしです。HTTP APIは実験的なデモ用であり、確定したACX標準ではありません。[APIと制約](../examples/e2e/README.md)も参照してください。既存の `print-manifest.json` とは別に、デモ独自のManifestを配信します。

## 简体中文

准备Python 3.10以上版本和pip，在已获取的仓库根目录中执行命令。无需API密钥或打印机，预计需要5–10分钟。

1. 按上方“1. Install”创建并激活虚拟环境，然后运行 `python -m pip install -e .`。Windows请使用所列的PowerShell命令。
2. 运行 `python examples/e2e/run.py`。程序在空闲的本地端口启动Provider，通过HTTP完成六个阶段。看到六行 `PASS` 和JSON回执后，服务自动关闭。
3. 如需持续运行，执行 `python examples/e2e/provider.py --port 8765`。在另一终端激活同一虚拟环境，运行 `python examples/e2e/client.py --base-url http://127.0.0.1:8765`。可在 `http://127.0.0.1:8765/.well-known/acx.json` 获取Manifest。使用Ctrl+C停止服务。
4. 使用上方“4. Verify and adapt”的测试命令验证拒绝场景。可以修改 `client.py` 中的 `request`。`copies: 3` 虽然符合输入Schema，但会被自动授权策略拒绝。

若端口被占用，将Provider和Client的端口都改为8766。缺少 `jsonschema` 时，请在当前虚拟环境中重新安装。连接失败时检查服务是否启动及端口是否一致。重启会清空状态，需要重新运行完整Client。

此示例仅在内存中模拟打印，不会打印或扣款。授权使用本地自动策略，回执没有签名。HTTP API是实验性演示接口，并非已确定的ACX标准。请阅读[API与限制](../examples/e2e/README.md)。示例提供自己的Manifest，与现有的 `print-manifest.json` 不同。
