# Changelog

All notable changes to Onyx will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2025-12-28

### Initial Release - The Dark Layer for the Agentic Web

**Onyx** is the production-ready privacy infrastructure for Solana, engineered specifically for Python developers and AI agents. It solves the "transparency paradox" by enabling fully shielded transactions and chain-agnostic micropayments.

### The Onyx Trinity (Core Features)

#### 1. The Onyx Shield (Privacy Primitives)
- **Turn public capital into private state.**
- **Pedersen Commitments**: Uses `ONYX_PROTOCOL_PEDERSEN_H_V1` domain separator.
- **Information-Theoretic Privacy**: Amount data is mathematically impossible to extract without the blinding factor.
- **Circuit-Safe Nullifiers**: Two-step Poseidon hashing prevents secret leakage.
- **Front-Running Protection**: 30-root history buffer ensures proof validity.

#### 2. Onyx Transfer (ZK-Transactions)
- **Move value without leaving a trace.**
- **Groth16 zkSNARKs**: Generate proofs in seconds (2-5s) via Rust core.
- **Encrypted Notes**: Uses `ONYX_NOTE_ENCRYPTION_V1` with ChaCha20-Poly1305 + ECDH.
- **Unlinkability**: The transaction graph is completely severed.

#### 3. Onyx Pay (x402 Integration)
- **Chain-agnostic payments for a multi-chain world.**
- **Gas Abstraction**: Pay Solana fees using USDC on Base, Polygon, Avalanche, etc.
- **Agent-Native**: HTTP 402 standard for autonomous agent payments.
- **15+ Networks**: Validated support for Mainnet and Testnet chains.

### Developer Experience (The Stack)

**"Python Simplicity. Rust Velocity."**

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Interface** | **Python 3.12+** | Async/await OnyxClient for easy integration. |
| **Engine** | **Rust Core** | Native binaries handling heavy cryptography (Poseidon, Groth16). |
| **Verifier** | **Anchor (Solana)** | On-chain program `6p1tzefXSST8j72qcj5EU3pAcY5qSc3HnCfFqc2gWxjM`. |

### Documentation & Examples

#### Comprehensive Guides
- **README.md**: Installation, quick start, roadmap
- **API_REFERENCE.md**: Complete API documentation
- **getting-started/**: Step-by-step tutorials

### Onyx Security Architecture

- **Curve**: BN254 (alt_bn128)
- **Hash**: Poseidon (t=3, RF=8, RP=57)
- **Proof System**: Groth16 (256-byte proofs)
- **Encryption**: ChaCha20-Poly1305 + ECDH
- **Tree Depth**: 20 levels (~1M leaves)
- **Nullifier Safety**: PDA-based constraints and two-step derivation

### Roadmap (The Path Forward)

- **Phase 1: Foundation (Current)**: Python SDK, Rust Core, x402 Integration.
- **Phase 2: The Network (v0.2.0)**: Public Onyx Node (Relayer) launch.
- **Phase 3: Decentralization**: Trusted Setup Ceremony (MPC), Mainnet Launch.
- **Phase 4: Expansion (2026)**: Full Gas Abstraction, Multi-asset support.

### Links

- **Documentation**: https://onyxprotocol.tech/docs/getting-started/overview
- **GitHub**: https://github.com/onyxsolana/onyx-sdk
- **PyPI**: https://pypi.org/project/onyx-solana/
- **TestPyPI**: https://test.pypi.org/project/onyx-solana/
- **Solana Program**: `6p1tzefXSST8j72qcj5EU3pAcY5qSc3HnCfFqc2gWxjM`
- **x402 Protocol**: https://docs.payai.network/x402

### Acknowledgments

Built with modern cryptography and production-grade infrastructure:
- **arkworks-rs**: Cryptographic primitives and zkSNARK implementation
- **PyO3**: Seamless Python-Rust interoperability
- **Anchor**: Solana smart contract framework
- **PayAI**: x402 payment facilitator network

---

**Onyx 0.1.0** - The Dark Layer for the Agentic Web. Privacy for the Machine Economy.
