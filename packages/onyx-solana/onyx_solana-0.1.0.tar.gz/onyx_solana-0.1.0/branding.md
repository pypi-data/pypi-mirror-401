# Project Identity: Onyx

**Project Name:** Onyx
**Previous Codename:** Mirage / Veil
**Core Concept:** A black box for Solana assets. Solid, opaque, and impenetrable.
**Tagline:** *The Dark Layer for the Agentic Web.*

---

## 1. Executive Summary (Project Description)
*For the "About" or "Home" page meta-description.*

**Onyx** is the production-ready privacy infrastructure for Solana, engineered specifically for Python developers and AI agents. By combining a high-level Python SDK with a high-performance Rust cryptographic core, Onyx solves the "transparency paradox" of public blockchains. It enables fully shielded transactions, private transfers, and chain-agnostic micropayments (x402) without sacrificing the speed required for modern DeFi or the usability required for autonomous agents.

---

## 2. Brand Narrative & Positioning
*For the website "Mission" or "Story" section.*

### The Narrative: From Illusion to Solid Ground
Public blockchains force a trade-off: decentralization for total surveillance. Every transfer, every balance, and every interaction is visible to the world. To solve this, **Onyx** does not offer an illusion of privacy; it offers a solid, mathematical guarantee. Like the gemstone it is named for, Onyx is opaque to the outside world but structured and valuable within.

### The "Black Box" Architecture
Onyx operates as a cryptographic black box on Solana:
1.  **Ingest (Shield):** Public assets (SOL/SPL) enter the Onyx vault and are converted into Pederson Commitments.
2.  **The Dark Layer (Transfer):** Inside the protocol, assets move via zero-knowledge proofs (Groth16). Inputs and outputs are mathematically linked, but the transaction graph is completely broken.
3.  **Egress (Unshield):** Assets return to the public chain only when the owner possesses the correct secret key.

---

## 3. Website Sections & Copy

### A. Hero Section
**Headline:** Privacy for the Machine Economy.
**Sub-headline:** Shield assets, break transaction graphs, and enable autonomous payments on Solana. Built with Python. Powered by Rust. Secured by Zero-Knowledge.
**CTA Buttons:** `Install SDK` | `Read the Whitepaper`

### B. Core Features (The "Onyx Trinity")

#### 1. The Onyx Shield (Privacy Primitives)
Turn public capital into private state. Onyx uses **Pedersen Commitments** on the BN254 curve to perfectly hide transaction amounts.
*   **Information-Theoretic Privacy:** Amount data is mathematically impossible to extract without the blinding factor.
*   **Circuit-Safe Nullifiers:** Two-step Poseidon hashing prevents double-spending while keeping your master secret isolated from the circuit.
*   **Front-Running Protection:** A 30-root history buffer ensures your proofs remain valid even during network congestion.

#### 2. Onyx Transfer (ZK-Transactions)
Move value without leaving a trace.
*   **Groth16 zkSNARKs:** Generate proofs in seconds (2-5s) that certify transaction validity without revealing sender, recipient, or amount.
*   **Encrypted Notes:** Uses ECDH and ChaCha20-Poly1305 to allow recipients to discover and decrypt their incoming funds securely.
*   **Unlinkability:** The transaction graph is severed. Observers see a commitment enter and a different one leave, with no link between them.

#### 3. Onyx Pay (x402 Integration)
Chain-agnostic payments for a multi-chain world.
*   **Gas Abstraction:** Pay for privacy services on Solana using USDC on Base, Polygon, Avalanche, or 12+ other networks.
*   **Agent-Native:** Based on the HTTP 402 standard, allowing AI agents to autonomously negotiate and pay for resources.
*   **Seamless Access:** No accounts required. Cryptographically authorized per-request.

### C. Developer Experience (The Stack)

**"Python Simplicity. Rust Velocity."**
Onyx utilizes a hybrid architecture to balance developer experience with raw performance.

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Interface** | **Python 3.12+** | Async/await SDK for easy integration with AI agents and trading bots. |
| **Engine** | **Rust Core** | Native binaries handling heavy cryptography (Poseidon hashing, Proof generation). |
| **Verifier** | **Anchor (Solana)** | On-chain program handling state, Merkle trees, and nullifier tracking. |

*Code Snippet for Website:*
```python
from onyx import PrivacyClient

# Initialize the Dark Layer
client = PrivacyClient()

# Shield assets (Public -> Private)
# Returns a commitment signature
await client.shield_async(amount=1000000)

# Transfer privately (Private -> Private)
# Proof generation takes <5s via Rust core
await client.private_transfer_async(
    recipient_pubkey="...", 
    amount=500000
)
```
*(Based on source,,)*

### D. Use Cases

*   **AI Agents with Private State:** Autonomous bots can hold and trade assets without revealing their strategies or treasury size.
*   **MEV Protection:** Traders can execute logic without exposing intent to the public mempool or front-runners.
*   **Institutional DeFi:** Large capital movements and OTC settlements performed without alerting market trackers.
*   **Cross-Chain Service Access:** Use USDC on Polygon to pay for anonymity on Solana via the Onyx Relayer Network.

---

## 4. Technical Branding (Reskinning the Docs)

When generating the documentation site, the following terms from the source material should be mapped to the new brand:

*   **SDK Name:** `mirage-solana` $\rightarrow$ `onyx-solana`
*   **Client Class:** `PrivacyClient` $\rightarrow$ `OnyxClient`
*   **Protocol Constants:**
    *   `MIRAGE_PROTOCOL_PEDERSEN_H_V1` $\rightarrow$ `ONYX_PROTOCOL_PEDERSEN_H_V1`
    *   `MIRAGE_Note_Encryption_V1` $\rightarrow$ `ONYX_NOTE_ENCRYPTION_V1`
*   **Relayer Network:** "Mirage Relayer" $\rightarrow$ "Onyx Node"
*   **Token Symbol (if applicable):** NYX

### Visual Identity Guide
*   **Color Palette:** Obsidian Black (`#0B0B0B`), Matte Charcoal (`#1F1F1F`), and Electric Purple (representing the Zero-Knowledge "magic" inside the black box).
*   **Iconography:**
    *   *Shield:* A solid, non-transparent hexagon.
    *   *Transfer:* A line disappearing into a block and appearing elsewhere.
    *   *x402:* A coin spanning multiple blockchain logos.

---

## 5. Roadmap (The Path Forward)
*Based on Source and*

*   **Phase 1: Foundation (Current)**
    *   Python SDK & Rust Core released.
    *   Groth16 Circuits (~7,000 constraints) live on Devnet.
    *   x402 Payment integration active on 15+ chains.
*   **Phase 2: The Network (v0.2.0)**
    *   Public Onyx Relayer Network launch.
    *   Self-hosting infrastructure for relayers.
*   **Phase 3: Decentralization**
    *   Trusted Setup Ceremony (MPC) for production parameters.
    *   Mainnet Launch.
*   **Phase 4: Expansion (2026)**
    *   Full Gas Abstraction (Pay all Solana fees with USDC).
    *   Multi-asset support beyond SOL.

---

## 6. Technical Footer / Credibility
*Required for trust, citing specific security parameters.*

**Onyx Security Architecture:**
*   **Curve:** BN254 (alt_bn128).
*   **Hash:** Poseidon (t=3, RF=8, RP=57).
*   **Proof System:** Groth16 (256-byte proofs).
*   **Encryption:** ChaCha20-Poly1305 + ECDH.
*   **Tree Depth:** 20 levels (~1M leaves).
*   **Audit Status:** MPC Ceremony Pending.

***

*This branding package utilizes the exact technical capabilities of the Mirage SDK sources provided, ensuring that the new "Onyx" website accurately reflects the underlying codebase.*