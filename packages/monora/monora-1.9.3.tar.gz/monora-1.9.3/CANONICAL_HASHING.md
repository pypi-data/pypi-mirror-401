# Canonical Hashing Spec

This document defines the canonical JSON and hash-chain rules used by both SDKs
to compute `event_hash` values for immutable event logs.

## Canonical JSON

- Input: the event payload **excluding** `event_hash` and `prev_hash`.
- Types: JSON primitives, arrays, and objects only. Non-JSON values must be
  normalized before hashing.
- Object keys: sorted lexicographically by Unicode codepoint at every level.
- Arrays: preserve element order.
- Encoding: UTF-8.
- Serialization: no extra whitespace.

Equivalent reference implementations:

- Python: `json.dumps(event, sort_keys=True, separators=(",", ":"))`
- Node: `JSON.stringify(canonicalize(event))` where `canonicalize` sorts keys at
  every object level and preserves arrays.

## Hashing

- Algorithm: `immutability.hash_algorithm` (lowercased), default `sha256`.
- Digest input: `prev_hash` (if present) **followed by** canonical JSON bytes.
- Output format: `<algorithm>:<hex_digest>`.

## Verification

Verification recomputes the hash using `event.prev_hash` and compares it to
`event.event_hash`. The algorithm is taken from the `event_hash` prefix.

## Fixtures

Cross-SDK test vectors live in `tests/fixtures/hash_vectors.json`. Both SDKs
should validate these vectors to guarantee identical `event_hash` outputs for
the same event payload.
