# ACX — Agent Capability Exchange

ACX is a proposed open capability layer for an agent-native web: a machine-readable contract that tells an AI agent what a service can do, how to invoke it, what authority it needs, what it costs, what side effects it may cause, how the result is proven, and how failure can be recovered.

## Positioning

ACX should **compose with**, not compete with, established protocols. MCP remains an execution/tool integration layer; A2A remains an agent-to-agent coordination layer; OAuth/OIDC remain authorization building blocks; W3C Verifiable Credentials can carry attestations; AP2 can secure agentic payment flows. ACX is the capability-contract layer above them.

## Public launch plan

1. Publish this website, the core specification, JSON Schemas and a threat model under a permissive license.
2. Release `acx validate`, a tiny CLI that validates `/.well-known/acx.json`.
3. Ship reference adapters for MCP, A2A and plain HTTPS plus TypeScript, Python, Rust and Go libraries.
4. Build a public read-only registry that indexes manifests but does not become mandatory infrastructure. Domain-hosted manifests remain authoritative.
5. Recruit 10–20 design partners from different domains: payments, developer tools, cloud, print/manufacturing, scientific instruments, robotics and commerce.
6. Run an interoperability event: one agent must discover and safely execute capabilities from independently implemented providers.
7. Publish conformance test vectors and badges only after at least three independent implementations pass.
8. Establish a neutral technical steering committee. Adopt a public RFC/ACP process and royalty-free patent commitment before v1.0.
9. Seek collaboration with existing protocol communities instead of presenting ACX as a replacement.
10. Standardize only proven pieces. Keep experimental profiles outside the stable core.

## Repository structure to create

- `spec/core.md` — normative core
- `spec/security.md` — threat model and deterministic safety gates
- `schema/acx-manifest.schema.json`
- `schema/acx-receipt.schema.json`
- `profiles/commerce/`, `profiles/robotics/`, `profiles/science/`
- `sdk/typescript/`, `sdk/python/`, `sdk/rust/`, `sdk/go/`
- `adapters/mcp/`, `adapters/a2a/`, `adapters/http/`
- `conformance/` — test suite and vectors
- `examples/` — minimal provider/client examples
- `rfcs/` — public change proposals

## Adoption rule

The standard should remain useful even if every major AI model improves dramatically. ACX standardizes the boundary between intelligence and the world, not the intelligence itself.
