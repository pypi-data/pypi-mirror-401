"""Test shielding operations"""

import pytest

from onyx import OnyxClient
from onyx.types import TransactionStatus
from onyx.utils import generate_secret


def test_shield_assets():
    """Test basic shield operation"""
    client = OnyxClient(rpc_url="https://api.devnet.solana.com")

    tx = client.shield_assets(
        amount=1000,
        token="SOL",
        owner_secret=generate_secret(),
    )

    assert tx.status == TransactionStatus.CONFIRMED
    assert tx.commitment is not None
    assert len(tx.commitment) > 0


def test_shield_deterministic():
    """Test that shielding with same inputs produces same commitment"""
    client = OnyxClient()
    secret = generate_secret()

    tx1 = client.shield_assets(amount=1000, token="SOL", owner_secret=secret)
    tx2 = client.shield_assets(amount=1000, token="SOL", owner_secret=secret)

    assert tx1.commitment == tx2.commitment


def test_shield_different_amounts():
    """Test that different amounts produce different commitments"""
    client = OnyxClient()
    secret = generate_secret()

    tx1 = client.shield_assets(amount=1000, token="SOL", owner_secret=secret)
    tx2 = client.shield_assets(amount=2000, token="SOL", owner_secret=secret)

    assert tx1.commitment != tx2.commitment


def test_shield_invalid_amount():
    """Test shielding with invalid amount"""
    client = OnyxClient()

    with pytest.raises(ValueError, match="Amount must be positive"):
        client.shield_assets(
            amount=-100,
            token="SOL",
            owner_secret=generate_secret(),
        )


def test_shield_zero_amount():
    """Test shielding with zero amount"""
    client = OnyxClient()

    with pytest.raises(ValueError, match="Amount must be positive"):
        client.shield_assets(
            amount=0,
            token="SOL",
            owner_secret=generate_secret(),
        )


def test_shield_short_secret():
    """Test shielding with short secret"""
    client = OnyxClient()

    with pytest.raises(ValueError, match="at least 32"):
        client.shield_assets(
            amount=1000,
            token="SOL",
            owner_secret="short",
        )


def test_shield_transaction_has_signature():
    """Test that shield transaction includes signature"""
    client = OnyxClient()

    tx = client.shield_assets(
        amount=1000,
        token="SOL",
        owner_secret=generate_secret(),
    )

    assert tx.signature is not None
    assert tx.signature.startswith("mock_signature_")
