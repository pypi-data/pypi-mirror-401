# Onyx API Reference

## Python SDK

### onyx

Main package for Onyx privacy SDK.

```python
from onyx import (
    OnyxClient,
    ShieldRequest,
    TransferRequest,
    UnshieldRequest,
    PrivateTransaction,
    CommitmentData,
    TransactionStatus,
    generate_secret,
    commitment_to_hex,
)

# Optional: x402 payment integration
from onyx.x402 import (
    X402Client,
    PaymentConfig,
    PaymentResponse,
)
```

---

## OnyxClient

Main client for privacy-preserving transactions.

### Constructor

```python
OnyxClient(
    rpc_url: str = "https://api.devnet.solana.com",
    program_id: Optional[str] = None
)
```

**Parameters:**
- `rpc_url` - Solana RPC endpoint URL
- `program_id` - Privacy program ID (default: `6p1tzefXSST8j72qcj5EU3pAcY5qSc3HnCfFqc2gWxjM`)

**Example:**
```python
client = OnyxClient(rpc_url="https://api.mainnet-beta.solana.com")
```

---

### initialize_pool_async()

Initialize the privacy pool on-chain (one-time setup).

```python
async def initialize_pool_async(
    authority: Keypair
) -> str
```

**Parameters:**
- `authority` - Keypair with authority to initialize the pool

**Returns:** Transaction signature (string)

**Raises:**
- `RuntimeError` - If pool already initialized or transaction fails

**Example:**
```python
from solders.keypair import Keypair

authority = Keypair()  # Load your authority keypair
signature = await client.initialize_pool_async(authority)
print(f"Pool initialized: {signature}")
```

**Note:** This only needs to be called once per program deployment.

---

### shield_assets() / shield_assets_async()

Shield assets to make them private.

#### Async Version (Blockchain Submission)

Submits transaction to blockchain and creates private commitment.

```python
async def shield_assets_async(
    amount: int,
    token: str,
    keypair: Keypair,
    secret: Optional[str] = None
) -> PrivateTransaction
```

**Parameters:**
- `amount` - Amount to shield (in smallest unit, e.g., lamports)
- `token` - Token address or "SOL" for native SOL
- `keypair` - Payer keypair for transaction signing
- `secret` - Optional secret key (auto-generated if None, min 32 chars if provided)

**Returns:** `PrivateTransaction` with commitment and secret

**Raises:**
- `ValueError` - If amount <= 0 or secret too short
- `RuntimeError` - If transaction fails

**Example:**
```python
from solders.keypair import Keypair

payer = Keypair()  # Load your keypair
secret = generate_secret()  # Or provide your own

tx = await client.shield_assets_async(
    amount=1_000_000_000,  # 1 SOL in lamports
    token="SOL",
    keypair=payer,
    secret=secret
)
print(f"Transaction: {tx.signature}")
print(f"Commitment: {tx.commitment}")
print(f"Secret (save this!): {tx.secret}")
```

#### Sync Version (Offline Computation)

Generates commitment without blockchain submission.

```python
def shield_assets(
    amount: int,
    token: str,
    owner_secret: str
) -> PrivateTransaction
```

**Parameters:**
- `amount` - Amount to shield
- `token` - Token address or "SOL"
- `owner_secret` - Owner's secret key (min 32 characters)

**Returns:** `PrivateTransaction` with commitment (status=PENDING)

**Example:**
```python
tx = client.shield_assets(
    amount=1_000_000_000,
    token="SOL",
    owner_secret="my_super_secret_key_at_least_32_chars"
)
print(f"Commitment: {tx.commitment}")
# Note: tx.status == TransactionStatus.PENDING (not submitted to chain)
```

---

### private_transfer() / private_transfer_async()

Transfer assets privately without revealing amounts, sender, or recipient.

#### Async Version (Blockchain Submission)

Submits private transfer transaction to blockchain.

```python
async def private_transfer_async(
    recipient: str,
    amount: int,
    sender_keypair: Keypair,
    sender_secret: str,
    sender_commitment: Optional[str] = None
) -> PrivateTransaction
```

**Parameters:**
- `recipient` - Recipient's Solana address (base58)
- `amount` - Amount to transfer
- `sender_keypair` - Sender's keypair for transaction signing
- `sender_secret` - Sender's secret key (from shield operation)
- `sender_commitment` - Optional sender's commitment hex (auto-generated if None)

**Returns:** `PrivateTransaction` with nullifier, new commitment, proof, and recipient_secret

**Raises:**
- `ValueError` - If invalid address, amount <= 0, or secret too short
- `RuntimeError` - If transaction fails or nullifier already spent

**Example:**
```python
tx = await client.private_transfer_async(
    recipient="RecipientPubkey...",
    amount=500_000_000,  # 0.5 SOL
    sender_keypair=payer,
    sender_secret="my_secret_from_shield",
    sender_commitment="abc123..."  # From shield_assets
)
print(f"Transaction: {tx.signature}")
print(f"Nullifier: {tx.nullifier}")
print(f"New commitment: {tx.commitment}")
print(f"Recipient secret: {tx.recipient_secret}")  # Share with recipient
print(f"Proof: {len(tx.proof)} bytes")
```

#### Sync Version (Offline Computation)

Generates transfer transaction data without blockchain submission.

```python
def private_transfer(
    recipient: str,
    amount: int,
    sender_secret: str,
    sender_commitment: Optional[str] = None
) -> PrivateTransaction
```

**Parameters:**
- `recipient` - Recipient's Solana address
- `amount` - Amount to transfer
- `sender_secret` - Sender's secret key
- `sender_commitment` - Optional sender's commitment (auto-generated if None)

**Returns:** `PrivateTransaction` with nullifier, commitment, proof, and recipient_secret (status=PENDING)

**Example:**
```python
tx = client.private_transfer(
    recipient="RecipientPubkey...",
    amount=500_000_000,
    sender_secret="my_secret",
    sender_commitment="abc123..."
)
# Note: Transaction not submitted, status=PENDING
```

---

### unshield_assets() / unshield_assets_async()

Unshield assets to make them public again (withdraw from privacy pool).

#### Async Version (Blockchain Submission)

Submits unshield transaction to blockchain and withdraws to public address.

```python
async def unshield_assets_async(
    amount: int,
    destination: str,
    owner_keypair: Keypair,
    owner_secret: str,
    commitment: str
) -> PrivateTransaction
```

**Parameters:**
- `amount` - Amount to unshield
- `destination` - Destination public Solana address
- `owner_keypair` - Owner's keypair for transaction signing
- `owner_secret` - Owner's secret key (from shield or transfer)
- `commitment` - Commitment to unshield (hex string)

**Returns:** `PrivateTransaction` with nullifier and proof

**Raises:**
- `ValueError` - If invalid destination address or amount
- `RuntimeError` - If transaction fails or nullifier already spent

**Example:**
```python
tx = await client.unshield_assets_async(
    amount=500_000_000,
    destination="MyPublicWallet...",
    owner_keypair=payer,
    owner_secret="my_secret",
    commitment="commitment_from_transfer..."
)
print(f"Transaction: {tx.signature}")
print(f"Nullifier: {tx.nullifier}")
print(f"Withdrawn {amount} lamports to {destination}")
```

#### Sync Version (Offline Computation)

Generates unshield transaction data without blockchain submission.

```python
def unshield_assets(
    amount: int,
    destination: str,
    owner_secret: str,
    commitment: str
) -> PrivateTransaction
```

**Parameters:**
- `amount` - Amount to unshield
- `destination` - Destination public address
- `owner_secret` - Owner's secret key
- `commitment` - Commitment to unshield (hex string)

**Returns:** `PrivateTransaction` with nullifier and proof (status=PENDING)

**Example:**
```python
tx = client.unshield_assets(
    amount=500_000_000,
    destination="MyPublicWallet...",
    owner_secret="my_secret",
    commitment="commitment_from_transfer..."
)
# Note: Transaction not submitted, status=PENDING
```

---

### verify_proof()

Verify a zkSNARK proof.

```python
def verify_proof(
    proof: bytes,
    public_inputs: dict[str, Any]
) -> bool
```

**Parameters:**
- `proof` - Proof bytes (96 bytes for compact, 256 bytes for Groth16)
- `public_inputs` - Dictionary of public inputs

**Returns:** `True` if proof is valid

**Example:**
```python
valid = client.verify_proof(
    proof=tx.proof,
    public_inputs={
        "nullifier": tx.nullifier,
        "new_commitment": tx.commitment,
        "root": merkle_root
    }
)
```

---

### is_nullifier_spent()

Check if a nullifier has been spent on-chain.

```python
async def is_nullifier_spent(
    nullifier: bytes
) -> bool
```

**Parameters:**
- `nullifier` - 32-byte nullifier to check

**Returns:** `True` if nullifier has been spent (PDA exists)

**Example:**
```python
from onyx import hex_to_bytes

nullifier_bytes = hex_to_bytes(tx.nullifier)
is_spent = await client.is_nullifier_spent(nullifier_bytes)

if is_spent:
    print("Nullifier already spent (double-spend attempt)")
else:
    print("Nullifier not yet spent (transaction is valid)")
```

---

### get_merkle_root()

Get the current Merkle root from on-chain state.

```python
async def get_merkle_root() -> bytes
```

**Returns:** 32-byte Merkle root

**Example:**
```python
root = await client.get_merkle_root()
print(f"Current Merkle root: {root.hex()}")

# Use in proof verification
valid = client.verify_proof(
    proof=tx.proof,
    public_inputs={"root": root.hex(), ...}
)
```

---

### close()

Close RPC connection.

```python
async def close() -> None
```

**Example:**
```python
await client.close()
```

---

## X402Client

Client for chain-agnostic micropayments using the x402 protocol.

**Installation required:** `pip install onyx-client[x402]`

### Constructor

```python
X402Client(
    facilitator_url: str = "https://facilitator.payai.network",
    network: str = "base-sepolia",
    wallet_address: Optional[str] = None
)
```

**Parameters:**
- `facilitator_url` - PayAI facilitator endpoint
- `network` - Blockchain network (see `SUPPORTED_NETWORKS`)
- `wallet_address` - Your wallet address for payments

**Example:**
```python
from onyx.x402 import X402Client

async with X402Client(network="base", wallet_address="0x...") as client:
    # Use client
    pass
```

---

### pay_for_access()

Execute x402 payment flow to access a paid resource.

```python
async def pay_for_access(
    resource_url: str,
    price_usd: float,
    merchant_address: str
) -> PaymentResponse
```

**Parameters:**
- `resource_url` - URL of the paid resource
- `price_usd` - Price in USD
- `merchant_address` - Merchant's receiving address

**Returns:** `PaymentResponse` with access token and payment details

**Raises:**
- `RuntimeError` - If payment flow fails

**Example:**
```python
from onyx.x402 import X402Client

async with X402Client(network="base-sepolia", wallet_address="0x...") as x402:
    payment = await x402.pay_for_access(
        resource_url="https://onyx-api.network/privacy/shield",
        price_usd=0.01,
        merchant_address="0xMERCHANT..."
    )

    print(f"Payment successful! Access token: {payment.access_token}")
    print(f"Verification ID: {payment.verification_id}")
```

---

### Supported Networks

```python
from onyx.x402.networks import SUPPORTED_NETWORKS

# EVM Networks
"base"              # Base mainnet
"base-sepolia"      # Base testnet
"polygon"           # Polygon mainnet
"polygon-amoy"      # Polygon testnet
"avalanche"         # Avalanche C-Chain
"avalanche-fuji"    # Avalanche testnet
"iotex"             # IoTeX mainnet
"peaq"              # Peaq Network
"sei"               # Sei Network
"xlayer"            # XLayer

# Solana
"solana"            # Solana mainnet
"solana-devnet"     # Solana devnet
```

---

## Types

### ShieldRequest

Request to shield assets.

```python
@dataclass
class ShieldRequest:
    amount: int
    token: str
    owner_secret: str

    def validate() -> None
```

---

### TransferRequest

Request for private transfer.

```python
@dataclass
class TransferRequest:
    recipient: str
    amount: int
    sender_secret: str
    sender_commitment: str

    def validate() -> None
```

---

### UnshieldRequest

Request to unshield assets.

```python
@dataclass
class UnshieldRequest:
    amount: int
    destination: str
    owner_secret: str
    commitment: str

    def validate() -> None
```

---

### CommitmentData

Commitment data structure.

```python
@dataclass
class CommitmentData:
    commitment: bytes
    amount: int
    blinding_factor: Optional[bytes] = None

    def to_hex() -> str

    @classmethod
    def from_hex(hex_str: str, amount: int) -> CommitmentData
```

---

### PrivateTransaction

Private transaction result.

```python
@dataclass
class PrivateTransaction:
    signature: str
    status: TransactionStatus
    commitment: Optional[str] = None
    nullifier: Optional[str] = None
    proof: Optional[bytes] = None
    secret: Optional[str] = None  # Secret used for shield commitment
    recipient_secret: Optional[str] = None  # Secret for recipient (transfer only)

    def to_dict() -> dict[str, Any]
```

**Fields:**
- `signature` - Transaction signature (or offline placeholder)
- `status` - Transaction status (PENDING, CONFIRMED, FAILED)
- `commitment` - Hex-encoded commitment (32 bytes)
- `nullifier` - Hex-encoded nullifier (32 bytes, for transfer/unshield)
- `proof` - Proof bytes (96 bytes for compact, 256 bytes for Groth16)
- `secret` - Secret used to generate commitment (shield operations)
- `recipient_secret` - Secret for recipient to spend the commitment (transfer operations)

---

### TransactionStatus

Transaction status enum.

```python
class TransactionStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
```

---

### PaymentConfig (x402)

Configuration for x402 payment.

```python
@dataclass
class PaymentConfig:
    price_usd: float
    merchant_address: str
    network: str = "base-sepolia"
```

---

### PaymentResponse (x402)

Response from x402 payment flow.

```python
@dataclass
class PaymentResponse:
    access_token: str
    verification_id: str
    payment_status: str
    tx_hash: Optional[str] = None
```

---

## Utilities

### generate_secret()

Generate a cryptographically secure secret.

```python
def generate_secret(length: int = 32) -> str
```

**Parameters:**
- `length` - Length of secret in bytes (default 32)

**Returns:** Hex-encoded secret string (64 characters for 32 bytes)

**Example:**
```python
secret = generate_secret()  # "a1b2c3d4..."
```

---

### commitment_to_hex()

Convert commitment bytes to hex string.

```python
def commitment_to_hex(commitment: bytes) -> str
```

---

### hex_to_bytes()

Convert hex string to bytes.

```python
def hex_to_bytes(hex_str: str) -> bytes
```

Handles "0x" prefix automatically.

---

### validate_solana_address()

Validate Solana address.

```python
def validate_solana_address(address: str) -> bool
```

---

## Rust Core (Low-Level)

Access via `onyx._rust_core` (private module, not typically used directly).

### generate_commitment()

```python
def generate_commitment(amount: int, secret: bytes) -> bytes
```

Generate Pedersen commitment using ONYX_PROTOCOL_PEDERSEN_H_V1.

---

### generate_nullifier()

```python
def generate_nullifier(commitment: bytes, secret: bytes) -> bytes
```

Generate nullifier hash using ONYX_NULLIFIER domain separator.

---

### generate_proof()

```python
def generate_proof(witness_json: str) -> bytes
```

Generate zkSNARK proof from witness JSON.

---

### verify_proof()

```python
def verify_proof(proof: bytes, public_inputs_json: str) -> bool
```

Verify zkSNARK proof.

---

### poseidon_hash()

```python
def poseidon_hash(inputs: list[bytes]) -> bytes
```

Compute Poseidon hash of inputs.

---

## Error Handling

All functions may raise:

- `ValueError` - Invalid input parameters
- `RuntimeError` - Cryptographic operation failed

**Example:**
```python
try:
    tx = client.shield_assets(
        amount=-100,  # Invalid!
        token="SOL",
        owner_secret="secret"
    )
except ValueError as e:
    print(f"Invalid input: {e}")
```

---

## Complete Examples

### Basic Privacy Operations (Async)

```python
import asyncio
from onyx import OnyxClient, generate_secret
from solders.keypair import Keypair

async def main():
    # Initialize client
    client = OnyxClient(rpc_url="https://api.devnet.solana.com")

    # Load or generate keypairs
    alice = Keypair()  # In production, load from file/env
    bob_address = "RecipientPublicKeyHere111111111111111111111"

    # Generate secret for privacy
    secret = generate_secret()

    # 1. Shield: Deposit 1 SOL into privacy pool
    print("Shielding assets...")
    shield_tx = await client.shield_assets_async(
        amount=1_000_000_000,  # 1 SOL in lamports
        token="SOL",
        keypair=alice,
        secret=secret
    )
    print(f"✓ Shielded: {shield_tx.signature}")
    print(f"  Commitment: {shield_tx.commitment[:16]}...")
    print(f"  Secret: {shield_tx.secret[:16]}... (save this!)")

    # 2. Private Transfer: Send 0.5 SOL to Bob
    print("\nPrivate transfer...")
    transfer_tx = await client.private_transfer_async(
        recipient=bob_address,
        amount=500_000_000,  # 0.5 SOL
        sender_keypair=alice,
        sender_secret=shield_tx.secret,
        sender_commitment=shield_tx.commitment
    )
    print(f"✓ Transferred: {transfer_tx.signature}")
    print(f"  Nullifier: {transfer_tx.nullifier[:16]}...")
    print(f"  New Commitment: {transfer_tx.commitment[:16]}...")
    print(f"  Recipient Secret: {transfer_tx.recipient_secret[:16]}... (send to Bob)")

    # 3. Verify nullifier is spent
    from onyx import hex_to_bytes
    nullifier_bytes = hex_to_bytes(transfer_tx.nullifier)
    is_spent = await client.is_nullifier_spent(nullifier_bytes)
    print(f"  Nullifier spent: {is_spent}")

    # 4. Unshield: Bob withdraws remaining 0.5 SOL
    print("\nUnshielding assets...")
    unshield_tx = await client.unshield_assets_async(
        amount=500_000_000,
        destination=bob_address,
        owner_keypair=alice,  # In production, Bob's keypair
        owner_secret=transfer_tx.recipient_secret,
        commitment=transfer_tx.commitment
    )
    print(f"✓ Unshielded: {unshield_tx.signature}")
    print(f"  Withdrew 0.5 SOL to {bob_address[:16]}...")

    # Cleanup
    await client.close()

# Run the example
asyncio.run(main())
```

---

### x402 Payment + Privacy Operations

```python
import asyncio
from onyx import OnyxClient
from onyx.x402 import X402Client
from solders.keypair import Keypair

async def main():
    # Initialize clients
    privacy = OnyxClient(rpc_url="https://api.mainnet-beta.solana.com")

    # Pay for privacy service using Base USDC
    async with X402Client(network="base", wallet_address="0x...") as x402:
        # Execute payment
        payment = await x402.pay_for_access(
            resource_url="https://onyx-api.network/privacy/shield",
            price_usd=0.01,
            merchant_address="0xMERCHANT..."
        )

        print(f"Payment verified: {payment.verification_id}")
        print(f"Access token: {payment.access_token}")

        # Use privacy features (with access token if API requires it)
        tx = await privacy.shield_assets_async(
            amount=1_000_000_000,
            token="SOL",
            keypair=Keypair()
        )

        print(f"Privacy operation completed: {tx.signature}")

    await privacy.close()

asyncio.run(main())
```

---

### Offline Mode (No Blockchain Submission)

```python
from onyx import OnyxClient, generate_secret

# Initialize client (no RPC connection needed for offline operations)
client = OnyxClient()
secret = generate_secret()

# Generate commitment offline
tx = client.shield_assets(
    amount=1_000_000_000,
    token="SOL",
    owner_secret=secret
)
print(f"Commitment: {tx.commitment}")
print(f"Status: {tx.status}")  # PENDING (not submitted)

# Generate transfer proof offline
transfer_tx = client.private_transfer(
    recipient="11111111111111111111111111111111",
    amount=500_000_000,
    sender_secret=secret,
    sender_commitment=tx.commitment
)
print(f"Nullifier: {transfer_tx.nullifier}")
print(f"Proof size: {len(transfer_tx.proof)} bytes")
```

---

## Program Information

**Program ID:** `6p1tzefXSST8j72qcj5EU3pAcY5qSc3HnCfFqc2gWxjM`

**Networks:**
- Devnet: https://explorer.solana.com/address/6p1tzefXSST8j72qcj5EU3pAcY5qSc3HnCfFqc2gWxjM?cluster=devnet
- Mainnet: https://explorer.solana.com/address/6p1tzefXSST8j72qcj5EU3pAcY5qSc3HnCfFqc2gWxjM

**Cryptographic Domain Separators:**
- Spending Key: `ONYX_SPENDING_KEY`
- Nullifier: `ONYX_NULLIFIER`
- Pedersen H: `ONYX_PROTOCOL_PEDERSEN_H_V1`
- Note Encryption: `ONYX_NOTE_ENCRYPTION_V1`
