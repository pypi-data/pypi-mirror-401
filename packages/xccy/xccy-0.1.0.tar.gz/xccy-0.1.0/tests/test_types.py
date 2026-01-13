"""Tests for data types."""

import pytest
from decimal import Decimal

from xccy.types import (
    AccountId,
    PoolKey,
    SwapParams,
    SwapResult,
    PositionInfo,
    PoolInfo,
    MarginBalance,
    HealthStatus,
)


class TestAccountId:
    """Tests for AccountId dataclass."""
    
    def test_create_basic(self):
        """Create a basic account ID."""
        account = AccountId(
            owner="0x1234567890123456789012345678901234567890",
            account_id=0,
        )
        assert account.owner == "0x1234567890123456789012345678901234567890"
        assert account.account_id == 0
        assert account.isolated_margin_token is None
    
    def test_create_with_isolated_token(self):
        """Create account with isolated margin token."""
        token = "0xABCDabcdABCDabcdABCDabcdABCDabcdABCDabcd"
        account = AccountId(
            owner="0x1234567890123456789012345678901234567890",
            account_id=1,
            isolated_margin_token=token,
        )
        assert account.isolated_margin_token == token
    
    def test_invalid_owner_address(self):
        """Invalid owner address should raise."""
        with pytest.raises(ValueError, match="Invalid owner"):
            AccountId(owner="not_an_address", account_id=0)
        
        with pytest.raises(ValueError, match="Invalid owner"):
            AccountId(owner="0x123", account_id=0)  # Too short
    
    def test_negative_account_id(self):
        """Negative account ID should raise."""
        with pytest.raises(ValueError, match="non-negative"):
            AccountId(
                owner="0x1234567890123456789012345678901234567890",
                account_id=-1,
            )
    
    def test_invalid_isolated_token(self):
        """Invalid isolated token address should raise."""
        with pytest.raises(ValueError, match="Invalid isolated_margin_token"):
            AccountId(
                owner="0x1234567890123456789012345678901234567890",
                account_id=0,
                isolated_margin_token="invalid",
            )
    
    def test_to_tuple(self):
        """Convert to tuple for contract calls."""
        account = AccountId(
            owner="0x1234567890123456789012345678901234567890",
            account_id=5,
            isolated_margin_token=None,
        )
        
        tup = account.to_tuple()
        assert tup[0] == "0x1234567890123456789012345678901234567890"
        assert tup[1] == 5
        assert tup[2] == "0x0000000000000000000000000000000000000000"
    
    def test_to_tuple_with_isolated(self):
        """Convert to tuple with isolated token."""
        token = "0xABCDabcdABCDabcdABCDabcdABCDabcdABCDabcd"
        account = AccountId(
            owner="0x1234567890123456789012345678901234567890",
            account_id=0,
            isolated_margin_token=token,
        )
        
        tup = account.to_tuple()
        assert tup[2] == token
    
    def test_get_hash(self):
        """Account hash should be deterministic."""
        account = AccountId(
            owner="0x1234567890123456789012345678901234567890",
            account_id=0,
        )
        
        hash1 = account.get_hash()
        hash2 = account.get_hash()
        
        assert hash1 == hash2
        assert len(hash1) == 32  # Keccak256 is 32 bytes
    
    def test_frozen(self):
        """AccountId should be immutable."""
        account = AccountId(
            owner="0x1234567890123456789012345678901234567890",
            account_id=0,
        )
        
        with pytest.raises(Exception):  # FrozenInstanceError
            account.account_id = 1


class TestPoolKey:
    """Tests for PoolKey dataclass."""
    
    def test_create_basic(self):
        """Create a basic pool key."""
        pool = PoolKey(
            underlying_asset="0x1234567890123456789012345678901234567890",
            compound_token="0xABCDabcdABCDabcdABCDabcdABCDabcdABCDabcd",
            term_start_timestamp_wad=1704067200 * 10**18,
            term_end_timestamp_wad=1735689600 * 10**18,
            fee_wad=int(0.003 * 10**18),
            tick_spacing=60,
        )
        
        assert pool.underlying_asset == "0x1234567890123456789012345678901234567890"
        assert pool.tick_spacing == 60
    
    def test_invalid_term_order(self):
        """Term end must be after term start."""
        with pytest.raises(ValueError, match="term_end must be after term_start"):
            PoolKey(
                underlying_asset="0x1234567890123456789012345678901234567890",
                compound_token="0xABCDabcdABCDabcdABCDabcdABCDabcdABCDabcd",
                term_start_timestamp_wad=1735689600 * 10**18,
                term_end_timestamp_wad=1704067200 * 10**18,  # Before start
                fee_wad=int(0.003 * 10**18),
                tick_spacing=60,
            )
    
    def test_term_timestamp_properties(self):
        """Term timestamps should be accessible as Unix timestamps."""
        pool = PoolKey(
            underlying_asset="0x1234567890123456789012345678901234567890",
            compound_token="0xABCDabcdABCDabcdABCDabcdABCDabcdABCDabcd",
            term_start_timestamp_wad=1704067200 * 10**18,
            term_end_timestamp_wad=1735689600 * 10**18,
            fee_wad=int(0.003 * 10**18),
            tick_spacing=60,
        )
        
        assert pool.term_start_timestamp == 1704067200
        assert pool.term_end_timestamp == 1735689600
    
    def test_term_duration(self):
        """Calculate term duration."""
        pool = PoolKey(
            underlying_asset="0x1234567890123456789012345678901234567890",
            compound_token="0xABCDabcdABCDabcdABCDabcdABCDabcdABCDabcd",
            term_start_timestamp_wad=1704067200 * 10**18,
            term_end_timestamp_wad=1735689600 * 10**18,
            fee_wad=int(0.003 * 10**18),
            tick_spacing=60,
        )
        
        duration = pool.term_duration_seconds
        assert duration == 1735689600 - 1704067200
        assert duration > 0
    
    def test_to_tuple(self):
        """Convert to tuple for contract calls."""
        pool = PoolKey(
            underlying_asset="0x1234567890123456789012345678901234567890",
            compound_token="0xABCDabcdABCDabcdABCDabcdABCDabcdABCDabcd",
            term_start_timestamp_wad=1704067200 * 10**18,
            term_end_timestamp_wad=1735689600 * 10**18,
            fee_wad=int(0.003 * 10**18),
            tick_spacing=60,
        )
        
        tup = pool.to_tuple()
        assert len(tup) == 6
        assert tup[5] == 60  # tick_spacing


class TestSwapParams:
    """Tests for SwapParams dataclass."""
    
    def test_create_and_convert(self):
        """Create SwapParams and convert to tuple."""
        account = AccountId(
            owner="0x1234567890123456789012345678901234567890",
            account_id=0,
        )
        
        params = SwapParams(
            account=account,
            amount_specified=10_000 * 10**6,
            sqrt_price_limit_x96=0,
            tick_lower=-6930,
            tick_upper=-6900,
        )
        
        tup = params.to_tuple()
        assert tup[1] == 10_000 * 10**6
        assert tup[3] == -6930


class TestHealthStatus:
    """Tests for HealthStatus dataclass."""
    
    def test_from_values_healthy(self):
        """Create healthy status."""
        status = HealthStatus.from_values(
            margin_value=Decimal("1500"),
            obligations=Decimal("1000"),
        )
        
        assert status.health_factor == Decimal("1.5")
        assert not status.is_liquidatable
        assert status.margin_required == Decimal("0")
    
    def test_from_values_undercollateralized(self):
        """Create undercollateralized status."""
        status = HealthStatus.from_values(
            margin_value=Decimal("800"),
            obligations=Decimal("1000"),
        )
        
        assert status.health_factor == Decimal("0.8")
        assert status.is_liquidatable
        assert status.margin_required == Decimal("200")
    
    def test_from_values_no_obligations(self):
        """No obligations means infinite health."""
        status = HealthStatus.from_values(
            margin_value=Decimal("1000"),
            obligations=Decimal("0"),
        )
        
        assert status.health_factor == Decimal("inf")
        assert not status.is_liquidatable
