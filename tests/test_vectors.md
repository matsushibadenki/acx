# Conformance vectors
1. Valid observational capability -> PASS.
2. Consequential capability without authority -> FAIL.
3. Unknown risk class -> FAIL.
4. Binding without type -> FAIL.
5. Irreversible capability with `reversible:true` but no recovery semantics -> profile warning.
6. Commit digest differs from preflight digest -> MUST REJECT at runtime.
7. Expired preflight -> MUST REJECT.
8. Receipt requestHash differs from committed request -> MUST REJECT verification.
