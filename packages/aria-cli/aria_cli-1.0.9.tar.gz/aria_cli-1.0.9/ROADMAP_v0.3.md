# ARIA Roadmap — Version 0.3
Target Release: 2026-02

This roadmap defines the goals and deliverables for ARIA v0.3, focusing on predictive flow simulation, mesh behavior, and SDK expansion.

---

## 1. ARIA Simulator (Core Deliverable)

### Goals
- Provide a deterministic, configurable simulation of ARIA predictions.
- Enable streaming, partial results, and failure injection.
- Support mesh topology simulation.

### Features
- Latency simulation
- Randomized or scripted predictions
- Partial + final streaming segments
- Mesh node simulation (core/edge roles)
- Capability negotiation simulation

---

## 2. Predictive Flow Integration

### Goals
- Allow Lenix/ARIA systems to run predictive cognitive events.
- Validate prompt packs and grounding rules.

### Deliverables
- `predict` event type in cognitive loop
- PredictiveFlowRunner
- Predictive metrics in snapshots

---

## 3. Mesh Protocol Implementation

### Goals
- Implement ARIA Mesh Protocol v0.2
- Support multi-node simulation

### Deliverables
- Mesh discovery
- Mesh status propagation
- Node role negotiation
- Latency-aware routing

---

## 4. SDK Expansion

### Deliverables
- C# SDK (full)
- TypeScript SDK (full)
- Kotlin SDK (full)
- Shared test suite for all SDKs

---

## 5. Documentation

### Deliverables
- ARIA Simulator Guide
- Predictive Flow Guide
- Mesh Protocol Guide
- Updated API Reference (v0.3)
