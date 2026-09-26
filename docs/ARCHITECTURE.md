# Architecture

Human -> Executive Agent -> ACX discovery/policy -> specialized agent/tool -> service/machine.

ACX Core is intentionally small: discovery, semantics, authority declaration, effects/risk, economics declaration, evidence, recovery, and lifecycle binding. Execution stays in bindings. This keeps ACX useful if today's agent protocols change.

## Capability identity
Use reverse-DNS or globally controlled namespaces in production, e.g. `com.example.print.document`. Registries index capabilities but do not own their meaning.

## Preflight
For consequential actions a provider returns a short-lived immutable preflight object. It contains capability/version, normalized request digest, effects, quote/max cost, approval policy, expiry, and recovery terms.

## Commit
Commit includes the preflight identifier/digest plus authorization evidence. A provider rejects material mismatch or expiry.

## Receipt
Receipt binds provider, capability, request hash, result hash, effects, cost and recovery state. Cryptographic envelope is a profile, not a new ACX crypto primitive.
