# ARIA Release Notes
Version: 0.2
Date: 2026-01-06

This release finalizes the canonical ARIA API contract and validates the full CLI + Python API implementation.

---

## Highlights

- Canonical ARIA API Reference (v0.2)
- Unified request/response envelopes
- Streaming prediction support
- Mesh topology schemas
- Capability negotiation
- Full conformance suite (32 tests) — ALL PASSED
- Graceful degradation mode in CognitiveEngine
- Improved Holomap validation and session loading

---

## New Features

### 1. API Contract (v0.2)
- Versioned metadata (`contractVersion`, `engineVersion`)
- Streaming predictions (`stream: true`)
- Mesh topology (`MeshNode`, `MeshTopology`)
- Capability negotiation via `status`

### 2. CLI Improvements
- `aria brain list`
- `aria holomap validate`
- `aria tour list`

### 3. Python API Enhancements
- BrainManager model listing
- WorldSnapshot serialization
- SessionRecorder JSONL support
- HolomapValidator path/dict support

---

## Bug Fixes

- `flow.type` → `flow.status`
- Metrics collected from nodes instead of snapshot root
- `flow.source` → `flow.source_id`
- Graceful degradation flag added to engine
- JSONL loading fixed in SessionManager
- Tour loader accepts string paths

---

## Known Limitations

- Predictive flows require ARIA Simulator or real engine
- Mesh operations currently stubbed

---

## Next Steps

- ARIA Simulator (v0.3)
- Predictive flow integration
- Mesh protocol implementation
- SDKs for C#, TS, Kotlin
