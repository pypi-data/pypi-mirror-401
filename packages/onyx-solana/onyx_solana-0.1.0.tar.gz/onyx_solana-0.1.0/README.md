# Onyx

> The Dark Layer for the Agentic Web.

**Onyx** is the production-ready privacy infrastructure for Solana, engineered specifically for Python developers and AI agents. By combining a high-level Python SDK with a high-performance Rust cryptographic core, Onyx solves the "transparency paradox" by enabling fully shielded transactions, private transfers, and chain-agnostic micropayments (x402) without sacrificing the speed required for modern DeFi or the usability required for autonomous agents.

[![Documentation](https://img.shields.io/badge/docs-onyxprotocol.tech-blue)](https://onyxprotocol.tech/docs/getting-started/overview)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://www.rust-lang.org/)

## The Onyx Trinity (Core Features)

### 1. The Onyx Shield (Privacy Primitives)
Turn public capital into private state. Onyx uses **Pedersen Commitments** on the BN254 curve to perfectly hide transaction amounts.
*   **Information-Theoretic Privacy**: Amount data is mathematically impossible to extract without the blinding factor.
*   **Circuit-Safe Nullifiers**: Two-step Poseidon hashing prevents double-spending while keeping your master secret isolated from the circuit.
*   **Front-Running Protection**: A 30-root history buffer ensures your proofs remain valid even during network congestion.

### 2. Onyx Transfer (ZK-Transactions)
Move value without leaving a trace.
*   **Groth16 zkSNARKs**: Generate proofs in seconds (2-5s) that certify transaction validity without revealing sender, recipient, or amount.
*   **Encrypted Notes**: Uses ECDH and ChaCha20-Poly1305 to allow recipients to discover and decrypt their incoming funds securely.
*   **Unlinkability**: The transaction graph is severed. Observers see a commitment enter and a different one leave, with no link between them.

### 3. Onyx Pay (x402 Integration)
Chain-agnostic payments for a multi-chain world.
*   **Gas Abstraction**: Pay for privacy services on Solana using USDC on Base, Polygon, Avalanche, or 12+ other networks.
*   **Agent-Native**: Based on the HTTP 402 standard, allowing AI agents to autonomously negotiate and pay for resources.
*   **Seamless Access**: No accounts required. Cryptographically authorized per-request.

## Developer Experience (The Stack)

**"Python Simplicity. Rust Velocity."**

Onyx utilizes a hybrid architecture to balance developer experience with raw performance.

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Interface** | **Python 3.12+** | Async/await SDK for easy integration with AI agents and trading bots. |
| **Engine** | **Rust Core** | Native binaries handling heavy cryptography (Poseidon hashing, Proof generation). |
| **Verifier** | **Anchor (Solana)** | On-chain program handling state, Merkle trees, and nullifier tracking. |

## Quick Start

### Installation

```bash
pip install onyx-solana
```

### Basic Usage

```python
from onyx import OnyxClient
from solders.keypair import Keypair

# Initialize the Dark Layer
client = OnyxClient(rpc_url="https://api.mainnet-beta.solana.com")
user_keypair = Keypair()

# Shield assets (Public -> Private)
# Returns a commitment signature
secret, commitment = client.shield_assets(
    amount=1_000_000_000,  # 1 SOL
    token="SOL",
    keypair=user_keypair
)

# Transfer privately (Private -> Private)
# Proof generation takes <5s via Rust core
tx = await client.private_transfer_async(
    recipient=recipient_address,
    amount=500_000_000,  # 0.5 SOL
    sender_secret=secret,
    sender_commitment=commitment
)

# Unshield assets (Private -> Public)
tx = client.unshield_assets(
    commitment=commitment,
    secret=secret,
    recipient=user_keypair.pubkey()
)
```

## Development

### Prerequisites

- Python 3.12+
- Rust 1.70+
- Solana CLI tools
- Anchor Framework (for Solana program)

### Building from Source

```bash
# Clone the repository
git clone https://github.com/onyxsolana/onyx-sdk.git
cd onyx-sdk

# Install all packages in development mode
make install-dev

# Run tests
make test

# Build all packages
make build
```

## Roadmap (The Path Forward)

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

## Onyx Security Architecture

*   **Curve:** BN254 (alt_bn128).
*   **Hash:** Poseidon (t=3, RF=8, RP=57).
*   **Proof System:** Groth16 (256-byte proofs).
*   **Encryption:** ChaCha20-Poly1305 + ECDH.
*   **Tree Depth:** 20 levels (~1M leaves).
*   **Audit Status:** MPC Ceremony Pending.

## Documentation

- **Getting Started**: [onyxprotocol.tech/docs/getting-started/overview](https://onyxprotocol.tech/docs/getting-started/overview)
- **API Reference**: [onyxprotocol.tech/docs/api](https://onyxprotocol.tech/docs/api)
- **Architecture**: [docs/ARCHITECTURE.md](https://onyxprotocol.tech/docs/architecture/overview)

## Supported Networks (x402)

Onyx x402 integration supports payments on 15+ blockchains:

**Mainnets**: Base, Polygon, Avalanche, Solana, IoTeX, Peaq, Sei, XLayer
**Testnets**: Base Sepolia, Polygon Amoy, Avalanche Fuji, Solana Devnet, and more

See [x402 networks documentation](onyx/x402/networks.py) for full list.

## License

MIT License - see [LICENSE](LICENSE) for details

## Contributing

Contributions welcome! Please see our contributing guidelines.

---

**Onyx** - The Dark Layer for the Agentic Web. Privacy for the Machine Economy.
