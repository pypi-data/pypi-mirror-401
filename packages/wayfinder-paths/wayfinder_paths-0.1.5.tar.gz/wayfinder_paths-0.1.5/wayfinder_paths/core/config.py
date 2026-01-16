"""
Core Configuration System
Separates user-provided configuration from system configuration
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from loguru import logger

from wayfinder_paths.core.constants.base import (
    ADAPTER_BALANCE,
    ADAPTER_BRAP,
    ADAPTER_HYPERLIQUID,
    ADAPTER_MOONWELL,
)


@dataclass
class UserConfig:
    """
    User-provided configuration
    These are values that users MUST provide to run strategies
    """

    # Credential-based auth (JWT)
    username: str | None = None
    password: str | None = None
    refresh_token: str | None = None

    # Wallet configuration
    main_wallet_address: str | None = None  # User's main wallet address
    strategy_wallet_address: str | None = None  # Dedicated strategy wallet address

    # Optional user preferences
    default_slippage: float = 0.005  # Default slippage tolerance (0.5%)
    gas_multiplier: float = 1.2  # Gas limit multiplier for safety

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserConfig":
        """Create UserConfig from dictionary"""
        return cls(
            username=data.get("username"),
            password=data.get("password"),
            refresh_token=data.get("refresh_token"),
            main_wallet_address=data.get("main_wallet_address"),
            strategy_wallet_address=data.get("strategy_wallet_address"),
            default_slippage=data.get("default_slippage", 0.005),
            gas_multiplier=data.get("gas_multiplier", 1.2),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "username": self.username,
            "password": self.password,
            "refresh_token": self.refresh_token,
            "main_wallet_address": self.main_wallet_address,
            "strategy_wallet_address": self.strategy_wallet_address,
            "default_slippage": self.default_slippage,
            "gas_multiplier": self.gas_multiplier,
        }


@dataclass
class SystemConfig:
    """
    System-level configuration
    These are values managed by the Wayfinder system
    """

    # API endpoints (populated from environment or defaults)
    api_base_url: str = field(
        default_factory=lambda: os.getenv(
            "WAYFINDER_API_URL", "https://api.wayfinder.ai"
        )
    )

    # Job configuration
    job_id: str | None = None
    job_type: str = "strategy"

    # Execution settings
    update_interval: int = 60  # Default update interval in seconds
    max_retries: int = 3  # Maximum retries for failed operations
    retry_delay: int = 5  # Delay between retries in seconds

    # System paths
    log_path: str | None = None
    data_path: str | None = None

    # Local wallets.json path used to auto-populate wallet addresses when not provided
    wallets_path: str | None = "wallets.json"

    # Optional wallet_id for policy rendering
    wallet_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SystemConfig":
        """Create SystemConfig from dictionary"""
        return cls(
            api_base_url=data.get(
                "api_base_url",
                os.getenv("WAYFINDER_API_URL", "https://api.wayfinder.ai"),
            ),
            job_id=data.get("job_id"),
            job_type=data.get("job_type", "strategy"),
            update_interval=data.get("update_interval", 60),
            max_retries=data.get("max_retries", 3),
            retry_delay=data.get("retry_delay", 5),
            log_path=data.get("log_path"),
            data_path=data.get("data_path"),
            wallets_path=data.get(
                "wallets_path", os.getenv("WALLETS_PATH", "wallets.json")
            ),
            wallet_id=data.get("wallet_id") or os.getenv("WALLET_ID"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "api_base_url": self.api_base_url,
            "job_id": self.job_id,
            "job_type": self.job_type,
            "update_interval": self.update_interval,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "log_path": self.log_path,
            "data_path": self.data_path,
            "wallets_path": self.wallets_path,
            "wallet_id": self.wallet_id,
        }


@dataclass
class StrategyJobConfig:
    """
    Complete configuration for a strategy job
    Combines user and system configurations
    """

    user: UserConfig
    system: SystemConfig
    strategy_config: dict[str, Any] = field(
        default_factory=dict
    )  # Strategy-specific configuration

    def __post_init__(self) -> None:
        """
        Enrich strategy_config with wallet addresses and private keys from wallets.json.

        This method automatically loads wallet information from wallets.json to populate
        main_wallet and strategy_wallet addresses in strategy_config. Only uses wallets
        with exact label matches (no fallbacks).

        Wallet enrichment is conditional and can be skipped:
        - Skipped if wallet_type is explicitly set to a non-"local" value
        - Only performed if wallet_type is None, "local", or not specified
        - Allows custom wallet providers (Privy/Turnkey) to opt out of file-based enrichment

        Note:
            This method never raises exceptions - all errors are logged but do not
            prevent config construction failures.
        """
        try:
            if not isinstance(self.strategy_config, dict):
                self.strategy_config = {}

            wallet_type = self._get_wallet_type()
            if wallet_type and wallet_type != "local":
                return

            by_label, by_addr = self._load_wallets_from_file()

            self._enrich_wallet_addresses(by_label)
            if wallet_type in (None, "local"):
                self._enrich_wallet_private_keys(by_addr)
        except Exception as e:
            # Defensive: never allow config construction to fail on enrichment
            logger.warning(
                f"Failed to enrich strategy config with wallet information: {e}"
            )

    def _get_wallet_type(self) -> str | None:
        """
        Determine the wallet type from strategy config.

        Checks strategy_config, main_wallet, and strategy_wallet for wallet_type.
        Returns the first wallet_type found, or None if not specified.

        Returns:
            Wallet type string or None if not specified.
        """
        wallet_type = self.strategy_config.get("wallet_type")
        if wallet_type:
            return wallet_type

        main_wallet = self.strategy_config.get("main_wallet")
        if isinstance(main_wallet, dict):
            wallet_type = main_wallet.get("wallet_type")
            if wallet_type:
                return wallet_type

        strategy_wallet = self.strategy_config.get("strategy_wallet")
        if isinstance(strategy_wallet, dict):
            wallet_type = strategy_wallet.get("wallet_type")
            if wallet_type:
                return wallet_type

        return None

    def _load_wallets_from_file(
        self,
    ) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
        """
        Load wallets from wallets.json file and index by label and address.

        Returns:
            Tuple of (by_label, by_addr) dictionaries:
            - by_label: Maps wallet label to wallet entry
            - by_addr: Maps wallet address (lowercase) to wallet entry
        """
        entries = _read_wallets_file(self.system.wallets_path)
        by_label: dict[str, dict[str, Any]] = {}
        by_addr: dict[str, dict[str, Any]] = {}

        if entries and isinstance(entries, list):
            for e in entries:
                if isinstance(e, dict):
                    # Index by label
                    label = e.get("label")
                    if isinstance(label, str):
                        by_label[label] = e
                    # Index by address
                    addr = e.get("address")
                    if isinstance(addr, str):
                        by_addr[addr.lower()] = e

        return by_label, by_addr

    def _enrich_wallet_addresses(self, by_label: dict[str, dict[str, Any]]) -> None:
        """
        Enrich strategy_config with wallet addresses from wallets.json.

        Loads main_wallet and strategy_wallet addresses by exact label match.
        Only sets addresses if they are not already present in strategy_config.

        Args:
            by_label: Dictionary mapping wallet labels to wallet entries.
        """
        # Load main wallet by exact label match only
        if "main_wallet" not in self.strategy_config:
            main_wallet = by_label.get("main")
            if main_wallet:
                self.strategy_config["main_wallet"] = {
                    "address": main_wallet["address"]
                }

        # Load strategy wallet by strategy name label match only
        strategy_name = self.strategy_config.get("_strategy_name")
        if strategy_name and isinstance(strategy_name, str):
            strategy_wallet = by_label.get(strategy_name)
            if strategy_wallet:
                # Use strategy-specific wallet as strategy_wallet
                if "strategy_wallet" not in self.strategy_config:
                    self.strategy_config["strategy_wallet"] = {
                        "address": strategy_wallet["address"]
                    }
                elif isinstance(self.strategy_config.get("strategy_wallet"), dict):
                    # Ensure address is set if not already
                    if not self.strategy_config["strategy_wallet"].get("address"):
                        self.strategy_config["strategy_wallet"]["address"] = (
                            strategy_wallet["address"]
                        )

    def _enrich_wallet_private_keys(self, by_addr: dict[str, dict[str, Any]]) -> None:
        """
        Enrich wallet configs with private keys from wallets.json.

        Only enriches private keys if using local wallet type (or defaulting to local).
        This ensures custom wallet providers don't get private keys from files.

        Args:
            by_addr: Dictionary mapping wallet addresses (lowercase) to wallet entries.
        """
        try:
            for key in ("main_wallet", "strategy_wallet"):
                wallet_obj = self.strategy_config.get(key)
                if isinstance(wallet_obj, dict):
                    addr = (wallet_obj.get("address") or "").lower()
                    entry = by_addr.get(addr)
                    if entry:
                        pk = entry.get("private_key") or entry.get("private_key_hex")
                        if (
                            pk
                            and not wallet_obj.get("private_key")
                            and not wallet_obj.get("private_key_hex")
                        ):
                            wallet_obj["private_key_hex"] = pk
        except Exception as e:
            logger.warning(
                f"Failed to enrich wallet private keys from wallets.json: {e}"
            )

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], strategy_name: str | None = None
    ) -> "StrategyJobConfig":
        """Create StrategyJobConfig from dictionary

        Args:
            data: Configuration dictionary
            strategy_name: Optional strategy name for per-strategy wallet lookup
        """
        user_cfg = UserConfig.from_dict(data.get("user", {}))
        sys_cfg = SystemConfig.from_dict(data.get("system", {}))
        # No auto-population - wallets must be explicitly set in config or matched by label
        strategy_config = data.get("strategy", {})
        # Store strategy name in config for wallet lookup
        if strategy_name:
            strategy_config["_strategy_name"] = strategy_name
        return cls(
            user=user_cfg,
            system=sys_cfg,
            strategy_config=strategy_config,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "user": self.user.to_dict(),
            "system": self.system.to_dict(),
            "strategy": self.strategy_config,
        }

    def get_adapter_config(self, adapter_name: str) -> dict[str, Any]:
        """
        Get configuration for a specific adapter
        Combines relevant user and system settings
        """
        config = {
            "api_base_url": self.system.api_base_url,
        }

        # Add wallet configuration if needed
        # Only use wallets from strategy_config (matched by label) - no fallbacks
        if adapter_name in [
            ADAPTER_BALANCE,
            ADAPTER_BRAP,
            ADAPTER_MOONWELL,
            ADAPTER_HYPERLIQUID,
        ]:
            strategy_wallet = self.strategy_config.get("strategy_wallet")
            main_wallet = self.strategy_config.get("main_wallet")
            config["strategy_wallet"] = (
                {"address": strategy_wallet["address"]}
                if strategy_wallet
                and isinstance(strategy_wallet, dict)
                and strategy_wallet.get("address")
                else {}
            )
            config["main_wallet"] = (
                {"address": main_wallet["address"]}
                if main_wallet
                and isinstance(main_wallet, dict)
                and main_wallet.get("address")
                else {}
            )
            # user_wallet uses strategy_wallet if available, otherwise main_wallet
            config["user_wallet"] = (
                config.get("strategy_wallet") or config.get("main_wallet") or {}
            )

        # Add specific settings
        if adapter_name == ADAPTER_BRAP:
            config["default_slippage"] = self.user.default_slippage
            config["gas_multiplier"] = self.user.gas_multiplier

        # Add any strategy-specific adapter config
        if adapter_name in self.strategy_config.get("adapters", {}):
            config.update(self.strategy_config["adapters"][adapter_name])

        return config


def load_config_from_env() -> StrategyJobConfig:
    """
    Load configuration from environment variables
    This is the simplest way for users to provide configuration
    """
    user_config = UserConfig(
        username=os.getenv("WAYFINDER_USERNAME"),
        password=os.getenv("WAYFINDER_PASSWORD"),
        refresh_token=os.getenv("WAYFINDER_REFRESH_TOKEN"),
        main_wallet_address=os.getenv("MAIN_WALLET_ADDRESS"),
        strategy_wallet_address=os.getenv("STRATEGY_WALLET_ADDRESS"),
        default_slippage=float(os.getenv("DEFAULT_SLIPPAGE", "0.005")),
        gas_multiplier=float(os.getenv("GAS_MULTIPLIER", "1.2")),
    )

    system_config = SystemConfig(
        api_base_url=os.getenv("WAYFINDER_API_URL", "https://api.wayfinder.ai"),
        job_id=os.getenv("JOB_ID"),
        update_interval=int(os.getenv("UPDATE_INTERVAL", "60")),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        retry_delay=int(os.getenv("RETRY_DELAY", "5")),
        wallets_path=os.getenv("WALLETS_PATH", "wallets.json"),
        wallet_id=os.getenv("WALLET_ID"),
    )

    # No auto-population - wallets must be explicitly set in environment or matched by label

    return StrategyJobConfig(user=user_config, system=system_config)


# --- Internal helpers -------------------------------------------------------


def _read_wallets_file(wallets_path: str | None) -> list[dict[str, Any]]:
    """
    Read wallet entries from a JSON file.

    Args:
        wallets_path: Path to the wallets.json file. If None or empty, returns empty list.

    Returns:
        List of wallet dictionaries. Each wallet dict should contain:
        - label: Wallet label (str)
        - address: Wallet address (str)
        - private_key or private_key_hex: Private key (str, optional)

        Returns empty list if file doesn't exist, is invalid JSON, or contains
        non-list data.

    Note:
        All errors are logged but do not raise exceptions. This allows the
        config system to continue functioning even if wallets.json is missing
        or malformed.
    """
    if not wallets_path:
        return []
    path = Path(wallets_path)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
        if isinstance(data, list):
            return data
        return []
    except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
        logger.warning(f"Failed to read wallets file at {wallets_path}: {e}")
        return []
    except Exception as e:
        logger.warning(f"Unexpected error reading wallets file at {wallets_path}: {e}")
        return []
