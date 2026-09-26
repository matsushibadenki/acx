# ACX — Agent Capability Exchange

ACX is an open draft for a machine-readable capability layer for an agent-native web.

## Why
Agents need more than tool invocation. Before acting, they need a portable contract for outcome, authority, price, side effects, risk, evidence, and recovery.

ACX composes with existing protocols rather than replacing them: MCP/A2A for execution and coordination; OAuth/OIDC/VC for trust; payment protocols such as AP2 for settlement.

## Five-minute start
```bash
python -m pip install jsonschema
PYTHONPATH=src python -m acx validate examples/print-manifest.json
```
Publish the resulting manifest at `/.well-known/acx.json`.

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
1. Freeze core vocabulary and threat model.
2. Publish JSON Schemas and validator.
3. Add signed manifest and receipt profile (JWS/VC-compatible).
4. Build MCP and A2A adapters.
5. Ship JS/Python/Rust SDKs.
6. Run a public interop plugfest with 3+ independent providers.
7. Establish neutral stewardship and submit mature primitives to suitable standards bodies.

## License proposal
Specification text: CC BY 4.0. Reference code: Apache-2.0. Contributors: DCO + explicit royalty-free patent commitment for essential claims.


## Project Site
https://xs927991.xsrv.jp/en/acx/index.html
