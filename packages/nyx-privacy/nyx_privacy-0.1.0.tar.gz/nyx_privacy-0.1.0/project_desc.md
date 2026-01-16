Based on your request to refine the documentation with a specific **Project Identity** section—similar to the one previously created for "Onyx"—but tailored to **Nyx Privacy** and leveraging the specific technical details found in your source code (specifically the `NYX` domain separators), here is the drafted section.

This section is designed to be placed at the beginning of your documentation or branding guide.

***

# Project Identity: Nyx Privacy

**Project Name:** Nyx Privacy
**Previous Codename:** Mirage / Veil
**Core Concept:** A black box for Solana assets. Solid, opaque, and mathematically guaranteed.
**Tagline:** *The Dark Layer for the Agentic Web.*

---

## 1. Executive Summary

**Nyx Privacy** is the production-ready privacy infrastructure for Solana, engineered specifically for Python developers and AI agents. By combining a high-level Python SDK with a high-performance Rust cryptographic core, Nyx solves the "transparency paradox" of public blockchains.

It enables fully shielded transactions, private transfers, and chain-agnostic micropayments (x402) without sacrificing the speed required for modern DeFi or the usability required for autonomous agents.

---

## 2. Brand Narrative: The Name Was in the Code

*For the website "About" or "Mission" section.*

### The Origin
We did not choose the name **Nyx**. The code did.

Deep within the Rust cryptographic core of this project, the circuit-safe nullifier derivation has always been secured by the hardcoded domain separator: `NYX_NULLIFIER`.

We are simply aligning the surface identity with the cryptographic reality. **Nyx Privacy** is not a rebrand; it is a revelation of the protocol's true nature.

### The Philosophy: From Illusion to Void
Public blockchains force a trade-off: decentralization for total surveillance. Previous iterations (Mirage) suggested privacy was an illusion. **Nyx** asserts that privacy is a void—a solid, impenetrable space where value exists but cannot be seen.

Nyx does not obfuscate; it erases the trail entirely using Zero-Knowledge proofs.

---

## 3. The "Dark Layer" Architecture

Nyx operates as a cryptographic "Black Box" on Solana, processing data in three stages:

1.  **Ingest (Shield):**
    Public assets (SOL/SPL) enter the Nyx Vault. They are converted into **Pedersen Commitments**. The value is mathematically hidden, but the commitment is added to the public Merkle Tree.
2.  **The Void (Transfer):**
    Inside the Dark Layer, assets move via **Groth16 zkSNARKs**. The transaction graph is severed. Observers see a commitment enter and a different one leave, with no cryptographic link between them.
3.  **Egress (Unshield):**
    Assets return to the public chain only when the owner provides the correct secret key and valid proof.

---

## 4. Core Features (The Trinity)

#### 1. The Nyx Shield (Privacy Primitives)
Turn public capital into private state.
*   **Perfect Hiding:** Transaction amounts are hidden using Pedersen Commitments on the BN254 curve.
*   **Circuit-Safe Nullifiers:** We use a two-step Poseidon hash derivation (`NYX_SPENDING_KEY` $\rightarrow$ `NYX_NULLIFIER`) to prevent double-spending without exposing user secrets.
*   **Front-Running Protection:** A 30-root history buffer ensures proofs remain valid even during network congestion.

#### 2. The Nyx Engine (ZK-Transactions)
Move value without leaving a trace.
*   **High Performance:** ~7,000 R1CS constraints per transaction, generating proofs in seconds via the Rust core,.
*   **Encrypted Discovery:** Uses ECDH and ChaCha20-Poly1305 to allow recipients to discover and decrypt their incoming funds securely.
*   **Unlinkability:** The transaction graph is broken. Inputs cannot be linked to outputs.

#### 3. Nyx Pay (x402 Integration)
Chain-agnostic payments for a multi-chain world.
*   **Gas Abstraction:** Pay for privacy services on Solana using USDC on Base, Polygon, Avalanche, or 12+ other networks.
*   **Agent-Native:** Built on the HTTP 402 standard, allowing AI agents to autonomously negotiate and pay for privacy resources.

---

## 5. Developer Experience (The Stack)

**"Python Simplicity. Rust Velocity."**

Nyx utilizes a hybrid architecture to balance developer experience with raw cryptographic power,.

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Interface** | **Python 3.12+** | Async/await SDK (`NyxClient`) for easy integration with AI agents and bots. |
| **Engine** | **Rust Core** | Native binaries handling heavy cryptography (Poseidon, Groth16) via PyO3. |
| **Verifier** | **Anchor (Solana)** | On-chain program handling state, Merkle trees, and nullifier tracking. |

**Code Identity:**
The SDK should be instantiated as `NyxClient` to reflect the new identity.

```python
from nyx import NyxClient

# Initialize the Dark Layer
client = NyxClient()

# Shield assets (Public -> Private)
await client.shield_async(amount=1_000_000, token="SOL")
```

---

## 6. Technical Branding & Terminology

When updating documentation and code comments, map the following terms from the source material to the new brand:

*   **SDK Package:** `mirage-solana` $\rightarrow$ `nyx-solana` or `nyx-privacy`
*   **Client Class:** `PrivacyClient` $\rightarrow$ `NyxClient`
*   **Vault Term:** "Shielded Pool" $\rightarrow$ "The Dark Layer"
*   **Protocol Constants:**
    *   `MIRAGE_PROTOCOL_PEDERSEN_H_V1` $\rightarrow$ `NYX_PEDERSEN_H_V1`
    *   `MIRAGE_NOTE_ENCRYPTION_V1` $\rightarrow$ `NYX_NOTE_ENCRYPTION_V1`

### Visual Identity Guide
*   **Primary Color:** Void Navy (`#0B1120`).
*   **Accent Color:** Electric Blue (`#3B82F6`) — representing the logic/math layer.
*   **Status Color:** Emerald Green (`#10B981`) — used strictly for "Verified" proofs and "Shielded" status.
*   **Logo Concept:** A perfect, matte-black cube (The Nyx) floating in a void. It represents the "Black Box" architecture where inputs and outputs are visible, but the internal state is opaque.