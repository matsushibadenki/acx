# ACX — Agent Capability Exchange

HTTP made information addressable.
ACX makes capabilities actionable.
ACX is an open draft for a machine-readable capability layer for an agent-native web.

## Why

Agents need more than tool invocation. Before acting, they need a portable contract for outcome, authority, price, side effects, risk, evidence, and recovery.

ACX composes with existing protocols rather than replacing them: MCP/A2A for execution and coordination; OAuth/OIDC/VC for trust; payment protocols such as AP2 for settlement.

## Developer entry points

- [Quickstart: run a Provider in 5–10 minutes](docs/QUICKSTART.md)
- [ACX vs MCP / A2A](docs/ACX-vs-MCP-A2A.md)
- [Working End-to-End demo](examples/e2e/README.md) — six lifecycle stages over local HTTP

All three guides include English, Japanese and Simplified Chinese.

## Five-minute start
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python examples/e2e/run.py
```

To validate the separate illustrative print manifest:

```bash
python -m pip install jsonschema
PYTHONPATH=src python -m acx validate examples/print-manifest.json
```

The experimental Agent PrintIntent profile is documented in
[`docs/PRINT-PROFILE.md`](docs/PRINT-PROFILE.md) and validated by
`schemas/profiles/acx-print-intent.schema.json`.

Publish the validated manifest at `/.well-known/acx.json`.

## v0.1 lifecycle

`DISCOVER -> PREFLIGHT -> AUTHORIZE -> COMMIT -> EXECUTE -> RECEIPT -> RECOVER`

`PREFLIGHT` is mandatory for consequential/critical capabilities. It returns normalized effects, estimated/max cost, approval requirements, reversibility, expiry, and a request digest. `COMMIT` binds execution to that preflight digest so an agent cannot silently execute materially different parameters.

## Risk classes

- observational: no external mutation
- reversible: external mutation with deterministic rollback
- consequential: meaningful cost, publication, resource use, or physical effect
- critical: safety/legal/high-value action requiring domain-specific controls

## Governance proposal

The specification should remain royalty-free, vendor-neutral and public. Changes require an issue, written rationale, interoperability impact, test vectors, and two independent implementations before a mandatory feature graduates from experimental status.

## Repository roadmap

- [Done] Publish draft Manifest/Receipt JSON Schemas and validator.
- [Done] Add a local HTTP End-to-End demo, rejection tests and trilingual developer guides.
- [Done] Allow namespaced capability extensions and add an experimental Agent PrintIntent profile.
- [Next] Freeze core vocabulary and threat model; agree on lifecycle wire schemas and digest canonicalization.
- [Later] Add signed manifest and receipt profile (JWS/VC-compatible).
- [Later] Build MCP and A2A adapters.
- [Later] Ship JS/Python/Rust SDKs.
- [Later] Run a public interop plugfest with 3+ independent providers.
- [Later] Establish neutral stewardship and submit mature primitives to suitable standards bodies.

## License proposal

Specification text: CC BY 4.0. Reference code: Apache-2.0. Contributors: DCO + explicit royalty-free patent commitment for essential claims.

## Project Site

https://xs927991.xsrv.jp/en/acx/index.html

## Experimental Node Graph Profile

[Node Graph Profile 0.1](docs/NODE-GRAPH-PROFILE.md) defines revision-bound agent editing, execution and conditional recovery of Rust-owned graphs. It includes an [intent schema](schemas/profiles/acx-node-graph-intent.schema.json), [example](examples/node-graph-intent.json) and validation tests. The UNGE reference adapter uses a dedicated JSON Lines pipe; this is an optional experimental binding, not MCP or a new mandatory core feature. The guide includes English, Japanese and Simplified Chinese.
