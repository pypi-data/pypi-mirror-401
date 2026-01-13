# Onyx Architecture

## Overview

Onyx is a production-ready privacy SDK for Solana that enables private transactions using Groth16 zkSNARKs with optional x402 payment integration for chain-agnostic micropayments. The architecture follows a hybrid approach with Python for the user-facing API and Rust for performance-critical cryptographic operations.

Built on BN254 curve with Poseidon hash, Onyx provides complete transaction privacy (amounts, senders, recipients) with ECDH note encryption for recipient discovery. The system includes both async blockchain operations and offline computation modes, plus x402 protocol support for paying across 15+ blockchains.

## Multi-Package Architecture

Onyx is organized as a monorepo with three independent packages:

```
packages/
├── onyx-core       # Rust cryptography + PyO3 bindings
├── onyx-solana     # On-chain Anchor program
└── onyx-client     # Python SDK + x402 integration
```

## System Architecture

```
+-------------------------------------------------------------------------+
|                         Application Layer                               |
|  (DeFi Apps, Trading Bots, AI Agents, User Wallets)                    |
+-------------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------------+
|                     Python SDK (onyx-client)                          |
|  +----------------------+  +--------------------+  +------------------+ |
|  |   OnyxClient      |  |      Types         |  |   x402 Module    | |
|  | - shield_assets()    |  | - ShieldRequest    |  | - X402Client     | |
|  | - *_async()          |  | - TransferRequest  |  | - PaymentConfig  | |
|  | - private_transfer() |  | - PrivateTx        |  | - Facilitator    | |
|  | - unshield_assets()  |  | - CommitmentData   |  | - 15+ Networks   | |
|  | - is_nullifier_      |  +--------------------+  +------------------+ |
|  |   spent()            |  |  Solana Client     |  |      Utils       | |
|  | - get_merkle_root()  |  | - async RPC        |  | - generate_      | |
|  +----------------------+  | - build_ix         |  |   secret()       | |
|                            +--------------------+  +------------------+ |
+-------------------------------------------------------------------------+
                |                                            |
                | PyO3 Bindings                              | HTTPS
                v                                            v
+----------------------------------+  +-------------------------------+
|   Rust Core (onyx-core)        |  | x402 Facilitator              |
|  +------------+  +--------------+ |  | https://facilitator.payai.net |
|  |   Crypto   |  |    Proof     | |  | - /verify (payment check)     |
|  | - ONYX_* |  | - Transfer   | |  | - /settle (execute tx)        |
|  |   domains  |  |   Circuit    | |  | - /list (merchants)           |
|  | - Poseidon |  | - Groth16    | |  +-------------------------------+
|  | - Nullifier|  |   (7k cons)  | |                |
|  | - Merkle   |  | - Gadgets    | |                v
|  +------------+  +--------------+ |  +-------------------------------+
|  |   PyO3 Bindings              | |  | Payment Networks (multi-chain)|
|  | - Python exports             | |  | - Base, Polygon, Avalanche    |
|  +------------------------------+ |  | - Solana, IoTeX, Sei, etc.    |
+----------------------------------+  +-------------------------------+
                |
                | Solana RPC
                v
+-------------------------------------------------------------------------+
|                       Solana Blockchain                                 |
|  +----------------------+  +-------------------+  +-------------------+ |
|  | Privacy Pool (State) |  |   Merkle Tree     |  | Nullifier PDAs    | |
|  | - onyx_solana      |  | - Incremental     |  | - Per-nullifier   | |
|  | - Vault authority    |  | - Depth 20        |  | - Double-spend    | |
|  | - Root history[30]   |  | - Poseidon hash   |  |   prevention      | |
|  | - Asset support      |  +-------------------+  +-------------------+ |
|  | - Program ID:        |  | Groth16 Verify    |  | Proof Type        | |
|  |   6p1tzefX...        |  | - BN254 pairing   |  | - Auto-detect     | |
|  +----------------------+  | - ~200k CU        |  | - 96b vs 256b     | |
|                            +-------------------+  +-------------------+ |
+-------------------------------------------------------------------------+
```

## Package Components

### 1. onyx-core (Rust + PyO3)

**Purpose**: High-performance cryptographic operations

**Key Components**:

#### Cryptography (`crypto/`)
- **Commitment** - Pedersen commitments with ONYX_PROTOCOL_PEDERSEN_H_V1
- **Nullifier** - Spending keys and nullifiers with ONYX_SPENDING_KEY/ONYX_NULLIFIER
- **Poseidon Hash** - Circuit-friendly hash function
- **Note Encryption** - ECDH + ChaCha20-Poly1305 with ONYX_NOTE_ENCRYPTION_V1
- **Merkle Tree** - Depth-20 incremental tree with Poseidon hash

#### Zero-Knowledge Proofs (`proof/`)
- **TransferCircuit** - Groth16 circuit (~7k constraints)
- **Gadgets** - R1CS constraint system components
- **Proving/Verifying** - BN254 curve operations

#### PyO3 Bindings (`lib.rs`)
- Python-callable functions for all crypto operations
- Error handling with OnyxError/OnyxResult
- Async support where needed

**Version**: 0.1.0
**Crate**: `onyx-core`
**Module**: `onyx._rust_core`

### 2. onyx-solana (Anchor Program)

**Purpose**: On-chain privacy pool management

**Key Components**:

#### State Management
- **PrivacyPool** - Pool state with root history
- **Vault** - Token vault authority (PDA)
- **Asset Registry** - Multi-asset support (SOL + SPL)

#### Instructions
- `initialize()` - One-time pool setup
- `shield()` - Deposit into privacy pool
- `transfer()` - Private transfer with proof
- `unshield()` - Withdraw from pool

#### Verification
- **Groth16 Verifier** - On-chain proof verification
- **Nullifier Tracking** - PDA-based double-spend prevention
- **Merkle Updates** - Incremental tree updates

**Program ID**: `6p1tzefXSST8j72qcj5EU3pAcY5qSc3HnCfFqc2gWxjM`
**Version**: 0.1.0
**Framework**: Anchor 0.29

### 3. onyx-client (Python SDK)

**Purpose**: User-facing API with optional x402 payments

**Key Components**:

#### Core Privacy (`onyx/`)
- **OnyxClient** - Main privacy operations
- **SolanaClient** - Blockchain interaction
- **Types** - Request/response data structures
- **Utils** - Secret generation, validation

#### x402 Payment Integration (`onyx/x402/`)
- **X402Client** - HTTP payment client
- **FacilitatorClient** - PayAI facilitator API
- **Networks** - 15+ blockchain configurations
- **Types** - Payment data structures

**Supported x402 Networks**:
- **EVM**: Base, Polygon, Avalanche, IoTeX, Peaq, Sei, XLayer
- **Solana**: Mainnet, Devnet
- **Testnets**: All networks have testnet support

**Version**: 0.1.0
**Package**: `onyx-client`
**Optional Dependencies**: `pip install onyx-client[x402]`

## Data Flow

### Privacy Transaction Flow

```
1. Shield (Deposit)
   User → OnyxClient.shield_assets()
   → onyx-core: Generate commitment
   → onyx-solana: Insert into Merkle tree
   → Result: (secret, commitment)

2. Private Transfer
   User → OnyxClient.private_transfer()
   → onyx-core: Generate zkSNARK proof
   → onyx-solana: Verify proof + nullifier check
   → Recipient gets encrypted note
   → Result: Transaction signature

3. Unshield (Withdraw)
   User → OnyxClient.unshield_assets()
   → onyx-core: Prove commitment ownership
   → onyx-solana: Verify proof + spend nullifier
   → Tokens sent to recipient
   → Result: Transaction signature
```

### x402 Payment Flow

```
1. Request Resource
   User → X402Client.pay_for_access()
   → HTTP GET resource_url
   → 402 Payment Required response

2. Payment Construction
   → Parse X-Accept-Payment header
   → Generate payment payload (amount, merchant, nonce)
   → Sign payload (EIP-712 for EVM, native for Solana)

3. Payment Verification
   → POST to facilitator /verify
   → Facilitator validates signature, balance, amount
   → Returns verification_id

4. Resource Access
   → Retry HTTP GET with X-PAYMENT header
   → Server validates payment
   → 200 OK with X-PAYMENT-RESPONSE
   → User receives access token

5. Payment Settlement (async)
   → Facilitator submits on-chain transaction
   → Returns tx_hash when confirmed
```

## Security Architecture

### Cryptographic Domain Separation

All cryptographic operations use ONYX-prefixed domain separators:

```rust
// Commitment generation
ONYX_PROTOCOL_PEDERSEN_H_V1

// Spending key derivation
ONYX_SPENDING_KEY

// Nullifier generation
ONYX_NULLIFIER

// Note encryption
ONYX_NOTE_ENCRYPTION_V1
```

This ensures:
- Protocol isolation from other systems
- No cross-protocol attacks
- Clear version management
- Backward incompatibility with Veil (intentional)

### Privacy Guarantees

1. **Amount Privacy**: Pedersen commitments hide amounts
2. **Sender Privacy**: zkSNARK proves ownership without revealing identity
3. **Recipient Privacy**: ECDH encrypted notes
4. **Double-Spend Prevention**: Nullifier uniqueness enforced on-chain
5. **Merkle Path Privacy**: Only root verified, path not revealed

### x402 Security

1. **Payment Signatures**: EIP-712 (EVM) or native signing (Solana)
2. **Nonce Uniqueness**: Prevents replay attacks
3. **Facilitator Validation**: Off-chain verification before settlement
4. **On-Chain Settlement**: Atomic payment execution
5. **No Fee Extraction**: Users don't pay network fees (merchant does)

## Performance Characteristics

### Rust Core (onyx-core)
- **Commitment Generation**: ~1ms
- **Nullifier Derivation**: ~0.5ms
- **Merkle Proof**: ~5ms (depth 20)
- **Proof Generation**: ~2-5s (Groth16)
- **Proof Verification**: ~10ms (native)

### Solana Program (onyx-solana)
- **Shield Instruction**: ~50k CU
- **Transfer Instruction**: ~250k CU (with proof verification)
- **Unshield Instruction**: ~200k CU
- **Groth16 Verification**: ~200k CU

### x402 Integration
- **Payment Flow**: ~500ms total (HTTP 402 → verify → retry)
- **Facilitator Verify**: ~100ms
- **Settlement**: 1-30s (depends on blockchain)

## Deployment

### Development
```bash
# Install all packages
make install-dev

# Run tests
make test

# Check compilation
make check
```

### Production

**onyx-core**:
```bash
cd packages/onyx-core
maturin build --release
maturin publish
```

**onyx-solana**:
```bash
cd packages/onyx-solana
anchor build
anchor deploy --provider.cluster mainnet-beta
```

**onyx-client**:
```bash
cd packages/onyx-client
python -m build
twine upload dist/*
```

## Migration from Veil 0.1.x

**Breaking Changes**:
- Domain separators: NYX → ONYX
- Program ID changed
- Package renamed: veil-solana → onyx-client

See [MIGRATION.md](../MIGRATION.md) for complete guide.

## Future Enhancements

1. **Multi-Chain Privacy**: Extend privacy operations beyond Solana
2. **Relayer Network**: Decentralized relayer infrastructure
3. **Advanced Circuits**: More complex privacy preserving operations
4. **Cross-Chain Bridges**: Private bridges between chains using x402
5. **ZK Rollups**: Layer 2 privacy scaling

---

**Onyx** - Privacy by design • Multi-chain payments • Production ready
