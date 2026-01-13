# 🔐 Wayfinder Vaults

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Discord](https://img.shields.io/badge/discord-join-7289da.svg)](https://discord.gg/fUVwGMXjm3)

Open-source platform for community-contributed crypto trading strategies and adapters. Build, test, and deploy automated trading vaults with direct wallet integration.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/wayfinder-ai/wayfinder-paths.git
cd wayfinder-paths

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# ⚠️ Generate test wallets FIRST (required!)
# This creates wallets.json with a main wallet for local testing
just create-wallets
# Or manually: poetry run python wayfinder_paths/scripts/make_wallets.py -n 1

# Copy and configure
cp wayfinder_paths/config.example.json config.json
# Edit config.json with your Wayfinder credentials

# Run a strategy locally (one-shot status check)
poetry run python wayfinder_paths/run_strategy.py stablecoin_yield_strategy --action status --config config.json

export WAYFINDER_API_KEY="sk_live_abc123..."
poetry run python wayfinder_paths/run_strategy.py stablecoin_yield_strategy --config config.json

# Run continuously (production mode)
poetry run python wayfinder_paths/run_strategy.py stablecoin_yield_strategy --config config.json
```

## 📁 Repository Structure

```
wayfinder_paths/
├── wayfinder_paths/              # Main package directory
│   ├── core/                      # Core engine (maintained by team)
│   │   ├── clients/              # API client managers
│   │   ├── adapters/             # Base adapter interfaces
│   │   ├── engine/               # Trading engine & VaultJob
│   │   ├── strategies/           # Base strategy classes
│   │   └── config.py             # Configuration system
│   ├── vaults/                   # Community contributions (each artifact in its own folder)
│   │   ├── adapters/             # Your exchange/protocol integrations
│   │   │   ├── balance_adapter/
│   │   │   │   ├── adapter.py        # Adapter implementation
│   │   │   │   ├── manifest.yaml     # Adapter manifest (caps, entrypoint)
│   │   │   │   ├── examples.json     # Example inputs for smoke
│   │   │   │   ├── README.md         # Local notes
│   │   │   │   └── test_adapter.py   # Local smoke test
│   │   │   ├── brap_adapter/
│   │   │   └── ...
│   │   └── strategies/           # Your trading strategies
│   │       ├── stablecoin_yield_strategy/
│   │       │   ├── strategy.py       # Strategy implementation
│   │       │   ├── manifest.yaml     # Strategy manifest
│   │       │   ├── examples.json     # Example inputs
│   │       │   ├── README.md         # Local notes
│   │       │   └── test_strategy.py  # Local smoke test
│   │       └── ...
│   ├── tests/                    # Test suite
│   ├── CONFIG_GUIDE.md           # Configuration documentation
│   ├── config.example.json       # Example configuration
│   ├── scripts/                  # Utility scripts
│   └── run_strategy.py           # Strategy runner script
├── config.json                   # Your local config (created by you)
├── wallets.json                  # Generated dev wallets
├── pyproject.toml                # Poetry configuration
└── README.md                     # This file
```

## 🤝 Contributing

We welcome contributions! This is an open-source project where community members can contribute adapters and strategies.

### Quick Contribution Guide

1. **Fork the repository** and clone your fork
2. **Create a feature branch**: `git checkout -b feature/my-strategy`
3. **Copy a template** to get started:
   - **For adapters**: Copy `wayfinder_paths/vaults/templates/adapter/` to `wayfinder_paths/vaults/adapters/my_adapter/`
   - **For strategies**: Copy `wayfinder_paths/vaults/templates/strategy/` to `wayfinder_paths/vaults/strategies/my_strategy/`
4. **Customize** the template (rename classes, update manifest, implement methods)
5. **Test your code** thoroughly using the provided test framework
6. **Validate manifests**: Run `just validate-manifests`
7. **Submit a Pull Request** with a clear description of your changes

### What You Can Contribute

- **Adapters**: Exchange/protocol integrations (e.g., Uniswap, Aave, Compound)
- **Strategies**: Trading algorithms and yield optimization strategies
- **Improvements**: Bug fixes, documentation, or core system enhancements

### Contributor Guidelines

#### For Adapters
- **Start from the template**: Copy `wayfinder_paths/vaults/templates/adapter/` as a starting point
- Extend `BaseAdapter` from `wayfinder_paths/core/adapters/BaseAdapter.py`
- Create a `manifest.yaml` (template at `wayfinder_paths/vaults/templates/adapter/manifest.yaml`) with:
  - `entrypoint`: Full import path to your adapter class
  - `capabilities`: List of capabilities your adapter provides
  - `dependencies`: List of required client classes (e.g., `PoolClient`, `TokenClient`)
- Implement methods that fulfill the declared capabilities
- Add comprehensive tests in `test_adapter.py`
- Include usage examples in `examples.json`
- Document your adapter in `README.md`
- Validate your manifest: `just validate-manifests`

#### For Strategies
- **Start from the template**: Use `just create-strategy "Strategy Name"` to create a new strategy with its own wallet, or copy `wayfinder_paths/vaults/templates/strategy/` manually
- Extend `Strategy` from `wayfinder_paths/core/strategies/Strategy.py`
- Create a `manifest.yaml` (template at `wayfinder_paths/vaults/templates/strategy/manifest.yaml`) with:
  - `entrypoint`: Full import path to your strategy class
  - `name`: Strategy directory name (used for wallet lookup)
  - `permissions.policy`: Security policy for transaction permissions
  - `adapters`: List of required adapters and their capabilities
- Implement required methods: `deposit()`, `update()`, `status()`, `withdraw()`
- Include test cases in `test_strategy.py`
- Add example configurations in `examples.json`
- Validate your manifest: `just validate-manifests`

#### General Guidelines
- **Code Quality**: Follow existing patterns and use type hints
- **Testing**: See [TESTING.md](TESTING.md) - minimum: smoke test for strategies, basic tests for adapters
- **Documentation**: Update README files and add docstrings
- **Security**: Never hardcode API keys or private keys
- **Architecture**: Use adapters for external integrations, not direct API calls

### Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/wayfinder-paths.git
cd wayfinder-paths

# 2. Install dependencies
poetry install

# 3. Generate test wallets (required before testing!)
# Creates a main wallet (or use 'just create-strategy' which auto-creates wallets)
just create-wallets
# Or manually: poetry run python wayfinder_paths/scripts/make_wallets.py -n 1

# 4. Create a new strategy (recommended - automatically creates wallet)
just create-strategy "My Strategy Name"

# Or manually copy a template:
# For adapters:
cp -r wayfinder_paths/vaults/templates/adapter wayfinder_paths/vaults/adapters/my_adapter
# For strategies:
cp -r wayfinder_paths/vaults/templates/strategy wayfinder_paths/vaults/strategies/my_strategy

# 5. Customize the template (see template README.md files for details)

# 6. Validate your manifest
just validate-manifests

# 7. Run tests
poetry run pytest -k smoke -v

# Or test your specific contribution
poetry run pytest wayfinder_paths/vaults/strategies/your_strategy/ -v
poetry run pytest wayfinder_paths/vaults/adapters/your_adapter/ -v

# 8. Test your contribution locally
poetry run python wayfinder_paths/run_strategy.py your_strategy --action status
```

### Getting Help

- 📖 Check existing adapters/strategies for examples
- 🐛 Open an issue for bugs or feature requests

## 🏗️ Architecture

### Client System
The platform uses a unified client system for all API interactions. Clients are thin wrappers that handle low-level API calls, authentication, and network communication. **Strategies should not call clients directly** - use adapters instead for domain-specific operations.

### Clients vs Adapters

- **Clients**: Low-level, reusable service wrappers that talk to networks and external APIs. They handle auth, headers, retries, and response parsing, and expose generic capabilities (e.g., token info, tx building). Examples: `TokenClient`, `TransactionClient`, `WalletClient`.
- **Adapters**: Strategy-facing integrations for a specific exchange/protocol. They compose one or more clients to implement a manifest of capabilities (e.g., `supply`, `borrow`, `place_order`). Adapters encapsulate protocol-specific semantics and raise `NotImplementedError` for unsupported ops.

Recommended usage:

- Strategies call adapters (not clients directly) for domain actions.
- Add or change a client when you need a new low-level capability shared across adapters.
- Add or change an adapter when integrating a new protocol/exchange or changing protocol-specific behavior.

Data flow: `Strategy` → `Adapter` → `Client(s)` → network/API.

### Manifests

Every adapter and strategy requires a `manifest.yaml` file that declares its metadata, capabilities, and dependencies. Manifests are validated automatically in CI/CD and serve as the **single source of truth** for what each component can do.

#### Adapter Manifests

Adapter manifests declare the capabilities an adapter provides and the clients it depends on.

**Template:** Copy `wayfinder_paths/vaults/templates/adapter/manifest.yaml` as a starting point.

**Schema:**
```yaml
schema_version: "0.1"
entrypoint: "adapters.my_adapter.adapter.MyAdapter"
capabilities:
  - "pool.read"
  - "pool.analytics"
dependencies:
  - "PoolClient"
  - "TokenClient"
```

**Fields:**
- `schema_version`: Manifest schema version (currently `"0.1"`)
- `entrypoint`: Full Python import path to the adapter class (required)
- `capabilities`: List of abstract capabilities this adapter provides (required, non-empty)
- `dependencies`: List of client class names from `core.clients` that this adapter requires (required, non-empty)

**Example** (`vaults/adapters/pool_adapter/manifest.yaml`):
```yaml
schema_version: "0.1"
entrypoint: "adapters.pool_adapter.adapter.PoolAdapter"
capabilities:
  - "pool.read"
  - "pool.analytics"
  - "pool.discovery"
  - "llama.data"
  - "pool.reports"
dependencies:
  - "PoolClient"
```

#### Strategy Manifests

Strategy manifests declare permissions and required adapters with their capabilities.

**Template:** Copy `wayfinder_paths/vaults/templates/strategy/manifest.yaml` as a starting point.

**Schema:**
```yaml
schema_version: "0.1"
entrypoint: "strategies.my_strategy.strategy.MyStrategy"
permissions:
  policy: "(wallet.id == 'FORMAT_WALLET_ID') && (eth.tx.to == '0x...')"
adapters:
  - name: "POOL"
    capabilities: ["pool.read", "pool.analytics"]
  - name: "BRAP"
    capabilities: ["swap.quote", "swap.execute"]
```

**Fields:**
- `schema_version`: Manifest schema version (currently `"0.1"`)
- `entrypoint`: Full Python import path to the strategy class (required)
- `name`: Strategy directory name (optional, used for wallet lookup - defaults to directory name)
- `permissions.policy`: Security policy string that defines transaction permissions (required, non-empty)
- `adapters`: List of required adapters with their names and needed capabilities (required, non-empty)
  - `name`: Adapter type identifier (e.g., "POOL", "BRAP")
  - `capabilities`: List of capabilities required from this adapter

**Example** (`vaults/strategies/stablecoin_yield_strategy/manifest.yaml`):
```yaml
schema_version: "0.1"
entrypoint: "strategies.stablecoin_yield_strategy.strategy.StablecoinYieldStrategy"
permissions:
  policy: "(wallet.id == 'FORMAT_WALLET_ID') && ((eth.tx.data[0..10] == '0x095ea7b3' && eth.tx.data[34..74] == 'f75584ef6673ad213a685a1b58cc0330b8ea22cf') || (eth.tx.to == '0xF75584eF6673aD213a685a1B58Cc0330B8eA22Cf'))"
adapters:
  - name: "BALANCE"
    capabilities: ["wallet_read", "wallet_transfer"]
  - name: "POOL"
    capabilities: ["pool.read", "pool.analytics"]
  - name: "BRAP"
    capabilities: ["swap.quote", "swap.execute"]
```

#### Manifest Validation

Manifests are automatically validated to ensure:
- Schema compliance (all required fields present, correct types)
- Entrypoint classes exist and are importable
- Dependencies are valid client classes
- Permissions policies are non-empty

**Validate locally:**
```bash
# Validate all manifests
just validate-manifests

# Or manually
PYTHONPATH=wayfinder_paths poetry run python wayfinder_paths/scripts/validate_manifests.py
```

Validation runs automatically in CI/CD on every PR and push to main. All manifests must be valid before merging.

**How Validation Works:**

The `validate_manifests.py` script performs multi-stage validation:

1. **Schema Validation** (via Pydantic models):
   - Loads YAML file and validates against `AdapterManifest` or `StrategyManifest` schema
   - Checks required fields, types, and basic constraints (e.g., capabilities cannot be empty)
   - Validates entrypoint format (must be full import path like `"adapters.pool_adapter.adapter.PoolAdapter"`)

2. **Entrypoint Verification**:
   - **For Adapters**: Imports the entrypoint class and verifies it's a subclass of `BaseAdapter`
   - **For Strategies**: Imports the entrypoint class and verifies it's a subclass of `Strategy`
   - Uses Python's `__import__()` to dynamically import the module and class
   - Catches import errors, missing classes, and type mismatches

3. **Dependency Verification** (adapters only):
   - Validates that all declared dependencies (e.g., `PoolClient`, `TokenClient`) exist in `core.clients`
   - Attempts to import each dependency as `core.clients.{DepName}`

4. **Permissions Validation** (strategies only):
   - Validated by Pydantic: ensures `permissions.policy` exists and is non-empty
   - Policy syntax is not parsed/validated (assumed to be valid at runtime)

**Validation Flow:**
```
For each manifest file:
  1. Load YAML → Parse with Pydantic (schema validation)
  2. Import entrypoint class → Verify inheritance (entrypoint validation)
  3. For adapters: Import dependencies → Verify they exist (dependency validation)
  4. Collect all errors → Report results
```

The script automatically discovers all manifests by scanning:
- `wayfinder_paths/vaults/adapters/*/manifest.yaml` for adapter manifests
- `wayfinder_paths/vaults/strategies/*/manifest.yaml` for strategy manifests

All errors are collected and reported at the end, with the script exiting with code 1 if any validation fails.

#### Capabilities

Capabilities are abstract operation identifiers (e.g., `"pool.read"`, `"swap.execute"`) declared in manifests. They represent what operations an adapter can perform, not specific method names. The manifest is the **single source of truth** for capabilities—they are not duplicated in code.

When creating an adapter:
1. Declare capabilities in your `manifest.yaml`
2. Implement methods that fulfill those capabilities
3. Capabilities are validated at manifest validation time (entrypoint must be importable)

### Configuration
Configuration is split between:
- **User Config**: Your credentials and preferences
- **System Config**: Platform settings
- **Strategy Config**: Strategy-specific parameters

See [CONFIG_GUIDE.md](wayfinder_paths/CONFIG_GUIDE.md) for details.

### Authentication

Wayfinder Vaults supports two authentication methods:

#### 1. Service Account Authentication (API Key)
For backend services and automated systems with higher rate limits:

**Option A: Pass to Strategy Constructor**
```python
from wayfinder_paths.strategies.stablecoin_yield_strategy.strategy import StablecoinYieldStrategy

strategy = StablecoinYieldStrategy(
    config={...},
    api_key="sk_live_abc123..."  # API key is auto-discovered by all clients
)
```

**Option B: Set Environment Variable**
```bash
export WAYFINDER_API_KEY="sk_live_abc123..."
# All clients will automatically discover and use this
```

**Option C: Add to config.json**
```json
{
  "user": {
    "api_key": "sk_live_abc123..."
  },
  "system": {
    "api_key": "sk_live_abc123..."  // Alternative: system-level API key
  }
}
```

**Priority Order:** Constructor parameter > `config.json` (user.api_key or system.api_key) > `WAYFINDER_API_KEY` environment variable

**Note:** API keys in `config.json` are loaded directly by `WayfinderClient` via `_load_config_credentials()`, not through the `UserConfig` or `SystemConfig` dataclasses. This allows flexible credential loading.

#### 2. Personal Access Authentication (OAuth)
For standalone SDK users with username/password:

```json
{
  "user": {
    "username": "your_username",
    "password": "your_password",
    "refresh_token": null  // Optional: use refresh token instead
  }
}
```

**How It Works:**
- API keys are automatically discovered by all clients (no need to pass explicitly)
- When an API key is available, it's used for all API requests (including public endpoints) for rate limiting
- If no API key is found, the system falls back to OAuth authentication
- All clients created by adapters automatically inherit the API key discovery mechanism
- API keys in `config.json` are loaded directly by `WayfinderClient._load_config_credentials()` from `user.api_key` or `system.api_key`, not stored in the `UserConfig` or `SystemConfig` dataclasses

See [CONFIG_GUIDE.md](wayfinder_paths/CONFIG_GUIDE.md) for detailed authentication documentation.

## 🔌 Creating Adapters

Adapters connect to exchanges and DeFi protocols using the client system.

```python
# wayfinder_paths/vaults/adapters/my_adapter/adapter.py
from wayfinder_paths.core.adapters.BaseAdapter import BaseAdapter
from wayfinder_paths.core.clients.PoolClient import PoolClient


class MyAdapter(BaseAdapter):
    """Thin wrapper around PoolClient that exposes pool metadata to strategies."""

    adapter_type = "POOL"

    def __init__(self, config: dict | None = None):
        super().__init__("my_adapter", config)
        self.pool_client = PoolClient()

    async def connect(self) -> bool:
        """No-op for read-only adapters, but kept for manifest compatibility."""
        return True

    async def get_pools(self, pool_ids: list[str]):
        data = await self.pool_client.get_pools_by_ids(
            pool_ids=",".join(pool_ids), merge_external=True
        )
        return (True, data)
```

## 📈 Building Strategies

Strategies implement trading logic using adapters and the unified client system.

```python
# wayfinder_paths/vaults/strategies/my_strategy/strategy.py
from wayfinder_paths.core.services.web3_service import DefaultWeb3Service
from wayfinder_paths.core.strategies.Strategy import StatusDict, StatusTuple, Strategy
from wayfinder_paths.adapters.balance_adapter.adapter import BalanceAdapter


class MyStrategy(Strategy):
    name = "Demo Strategy"

    def __init__(
        self,
        config: dict | None = None,
        *,
        api_key: str | None = None,  # Optional: API key for service account auth
    ):
        super().__init__(api_key=api_key)  # Pass to base class for auto-discovery
        self.config = config or {}
        web3_service = DefaultWeb3Service(self.config)
        # Adapters automatically discover API key from env var (set by Strategy.__init__)
        balance_adapter = BalanceAdapter(self.config, web3_service=web3_service)
        self.register_adapters([balance_adapter])
        self.balance_adapter = balance_adapter

    async def deposit(
        self, main_token_amount: float = 0.0, gas_token_amount: float = 0.0
    ) -> StatusTuple:
        """Move funds from main wallet into the vault wallet."""
        if main_token_amount <= 0:
            return (False, "Nothing to deposit")

        success, _ = await self.balance_adapter.get_balance(
            token_id=self.config.get("token_id"),
            wallet_address=self.config.get("main_wallet", {}).get("address"),
        )
        if not success:
            return (False, "Unable to fetch balances")

        # Use BalanceAdapter (which leverages LocalTokenTxnService builders) for transfers here.
        self.last_deposit = main_token_amount
        return (True, f"Deposited {main_token_amount} tokens")

    async def update(self) -> StatusTuple:
        """Periodic strategy update"""
        return (True, "No-op update")

    async def _status(self) -> StatusDict:
        """Report balances back to the runner"""
        success, balance = await self.balance_adapter.get_balance(
            token_id=self.config.get("token_id"),
            wallet_address=self.config.get("vault_wallet", {}).get("address"),
        )
        return {
            "portfolio_value": float(balance or 0),
            "net_deposit": float(getattr(self, "last_deposit", 0.0)),
            "strategy_status": {"message": "healthy" if success else "unknown"},
        }
```

### Built-in adapters

- **BALANCE (BalanceAdapter)**: wraps `WalletClient`/`TokenClient` to read wallet, token, and pool balances and now orchestrates transfers between the main/vault wallets with ledger bookkeeping. Requires a `Web3Service` so it can share the same wallet provider as the strategy.
- **POOL (PoolAdapter)**: composes `PoolClient` to fetch pools, llama analytics, combined reports, high-yield searches, and search helpers.
- **BRAP (BRAPAdapter)**: integrates the cross-chain quote service for swaps/bridges, including fee breakdowns, route comparisons, validation helpers, and swap execution/ledger recording when provided a `Web3Service`.
- **LEDGER (LedgerAdapter)**: records deposits, withdrawals, custom operations, and cashflows via `LedgerClient`, and can read vault transaction summaries.
- **TOKEN (TokenAdapter)**: lightweight wrapper around `TokenClient` for token metadata, live price snapshots, and gas token lookups.
- **HYPERLEND (HyperlendAdapter)**: connects to `HyperlendClient` for lending/supply caps inside the HyperLend strategy.

Each strategy manifest declares which adapters it needs and which capabilities it consumes. Adapters must implement the behavior promised in their manifest (or raise `NotImplementedError` if invoked outside the manifest contract).

## 🧪 Testing

**📖 For detailed testing guidance, see [TESTING.md](TESTING.md)**

### Quick Start

```bash
# 1. Generate test wallets (required!)
# Creates a main wallet (or use 'just create-strategy' which auto-creates wallets)
just create-wallets
# Or manually: poetry run python wayfinder_paths/scripts/make_wallets.py -n 1

# 2. Run smoke tests
poetry run pytest -k smoke -v

# 3. Test your specific contribution
poetry run pytest wayfinder_paths/vaults/strategies/my_strategy/ -v     # Strategy
poetry run pytest wayfinder_paths/vaults/adapters/my_adapter/ -v       # Adapter
```

### Testing Your Contribution

**Strategies**: Add a simple smoke test in `test_strategy.py` that exercises deposit → update → status → withdraw.

**Adapters**: Add basic functionality tests with mocked dependencies. Use `examples.json` to drive your tests.

See [TESTING.md](TESTING.md) for complete examples and best practices.

## 💻 Local Development

### Setup

```bash
# Clone repo
git clone https://github.com/wayfinder-ai/wayfinder-paths.git
cd wayfinder-paths

# Install dependencies
poetry install

# Generate test wallets (essential!)
# Creates a main wallet (or use 'just create-strategy' which auto-creates wallets)
just create-wallets
# Or manually: poetry run python wayfinder_paths/scripts/make_wallets.py -n 1

# Copy and configure
cp wayfinder_paths/config.example.json config.json
# Edit config.json with your Wayfinder credentials

# Run a strategy (status check)
poetry run python wayfinder_paths/run_strategy.py stablecoin_yield_strategy --action status --config config.json

# Run with custom config
poetry run python wayfinder_paths/run_strategy.py stablecoin_yield_strategy --config my_config.json

# Run continuously with debug output
poetry run python wayfinder_paths/run_strategy.py stablecoin_yield_strategy --debug --config config.json
```

### Wallet Generation for Testing

**Before running any strategies, generate test wallets.** This creates `wallets.json` in the repository root with throwaway wallets for local testing:

```bash
# Essential: Create main wallet for testing
just create-wallets
# Or manually: poetry run python wayfinder_paths/scripts/make_wallets.py -n 1
```

This creates:
- `main` wallet - your main wallet for testing (labeled "main" in wallets.json)
- `wallets.json` - wallet addresses and private keys for local testing

**Note:** Strategy-specific wallets are automatically created when you use `just create-strategy "Strategy Name"`. For manual creation, use `just create-wallet "strategy_name"` or `poetry run python wayfinder_paths/scripts/make_wallets.py --label "strategy_name"`.

**Important:** These wallets are for testing only. Never use them with real funds or on mainnet.

**Per-Strategy Wallets:** Each strategy should have its own dedicated wallet. When you create a new strategy using `just create-strategy`, a wallet is automatically generated with a label matching the strategy directory name. The system automatically uses this wallet when running the strategy. See [CONFIG_GUIDE.md](wayfinder_paths/CONFIG_GUIDE.md) for details.

Additional options:

```bash
# Add 3 extra wallets for multi-account testing
poetry run python wayfinder_paths/scripts/make_wallets.py -n 3

# Create a wallet with a specific label (e.g., for a strategy)
poetry run python wayfinder_paths/scripts/make_wallets.py --label "my_strategy_name"

# Generate keystore files (for geth/web3 compatibility)
poetry run python wayfinder_paths/scripts/make_wallets.py -n 1 --keystore-password "my-password"
```

### Configuration

See [CONFIG_GUIDE.md](wayfinder_paths/CONFIG_GUIDE.md) for detailed configuration documentation.

#### Setup Configuration

```bash
# Copy example config
cp wayfinder_paths/config.example.json config.json

# Edit config.json with your settings
# Required fields:
#   - user.username: Your Wayfinder username
#   - user.password: Your Wayfinder password
#   - OR user.refresh_token: Your refresh token
#   - system.wallets_path: Path to wallets.json (default: "wallets.json")
#
# Wallet addresses are auto-loaded from wallets.json by default.
# Then run with:
poetry run python wayfinder_paths/run_strategy.py stablecoin_yield_strategy --config config.json
```

## 📦 Versioning

This package follows [Semantic Versioning](https://semver.org/) (SemVer) and is published to PyPI as a public package.

### Version Format: MAJOR.MINOR.PATCH

- **MAJOR** (X.0.0): Breaking changes that require code updates
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

### Version Bumping Rules

- **PATCH**: Bug fixes, security patches, documentation updates
- **MINOR**: New adapters, new strategies, new features (backward compatible)
- **MAJOR**: Breaking API changes, removed features, incompatible changes

### Important Notes

- **Versions are immutable**: Once published to PyPI, a version cannot be changed or deleted
- **Versions must be unique**: Each release must have a new, unique version number
- **Publishing is restricted**: Only publish from the `main` branch to prevent accidental releases

### Publishing Workflow and Order of Operations

**Critical**: Changes must follow this strict order:

1. **Merge to main**: All changes must be merged to the `main` branch first
2. **Publish to PyPI**: The new version must be published to PyPI from `main` branch
3. **Dependent changes**: Only after publishing can dependent changes be merged in other applications

**Why this order matters:**
- Other applications depend on this package from PyPI
- They cannot merge changes that depend on new versions until those versions are available on PyPI
- Publishing from `main` ensures the published version matches what's in the repository
- This prevents dependency resolution failures in downstream applications

**Example workflow:**
```bash
# 1. Make changes in a feature branch
git checkout -b feature/new-adapter
# ... make changes ...
git commit -m "Add new adapter"

# 2. Merge to main
git checkout main
git merge feature/new-adapter

# 3. Bump version in pyproject.toml (e.g., 0.1.3 → 0.2.0)
# Edit pyproject.toml: version = "0.2.0"
git commit -m "Bump version to 0.2.0"
git push origin main

# 4. Publish to PyPI (must be on main branch)
just publish

# 5. Now dependent applications can update their dependencies
# pip install wayfinder-paths==0.2.0
```

## 📦 Publishing

Publish to PyPI:

```bash
export PUBLISH_TOKEN="your_pypi_token"
just publish
```

**Important:**
- ⚠️ **Publishing is only allowed from the `main` branch** - the publish command will fail if run from any other branch
- ⚠️ **Versions must be unique** - ensure the version in `pyproject.toml` has been bumped and is unique
- ⚠️ **Follow the order of operations** - see [Versioning](#-versioning) section above for the required workflow
- ⚠️ **Versions are immutable** - once published, a version cannot be changed or deleted from PyPI

Install the published package:

```bash
pip install wayfinder-paths
# or
poetry add wayfinder-paths
```

Install from Git (development):

```bash
pip install git+https://github.com/wayfinder-ai/wayfinder-paths.git
```

### Managing Package Access

To add collaborators who can publish updates:
1. Go to https://pypi.org/project/wayfinder-paths/
2. Click "Manage" → "Collaborators"
3. Add users as "Maintainers" (can publish) or "Owners" (full control)

## 🔒 Security

- **Never hardcode API keys or Private keys** - use config.json for credentials
- **Never commit config.json** - add it to .gitignore
- **Test on testnet first** - use test network when available
- **Validate all inputs** - sanitize user data
- **Set gas limits** - prevent excessive fees

## 📊 Backtesting

Coming soon

## 🌟 Community

Need help or want to discuss strategies? Join our [Discord](https://discord.gg/fUVwGMXjm3)!

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

🚀 **Happy Wayfinding!**
