# AscendNet Architecture

*Full Alpha Proto-Type. Funding Needed For build-out*

```text
AscendNet/
│
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI entrypoint
│   │   ├── routes_prompts.py        # Endpoints for prompt listing/trading
│   │   ├── routes_compute.py        # Endpoints for job requests/bidding/results
│   │   ├── routes_users.py          # User registration, login, wallet connect
│   │   ├── models.py                # Pydantic models for API
│   │   ├── dependencies.py          # Auth, rate limiting, etc.
│   │   └── errors.py                # Custom API error handling
│   │
│   ├── p2p/
│   │   ├── __init__.py
│   │   ├── node.py                  # Node startup and discovery
│   │   ├── peer_manager.py          # Peer list, gossip protocol
│   │   ├── messaging.py             # P2P message format/transport
│   │   ├── dht.py                   # Distributed hash table functions
│   │   ├── pubsub.py                # Pub/sub message layer
│   │   └── utils.py                 # P2P utilities, e.g., serialization
│   │
│   ├── compute/
│   │   ├── __init__.py
│   │   ├── scheduler.py             # Match jobs to compute offers
│   │   ├── worker.py                # The local node's compute execution engine
│   │   ├── job_queue.py             # Manage incoming/outgoing jobs
│   │   ├── resource_monitor.py      # Track node's available GPU/CPU, etc.
│   │   ├── sandbox.py               # Docker sandbox for running jobs
│   │   └── utils.py                 # Helper functions
│   │
│   ├── payments/
│   │   ├── __init__.py
│   │   ├── payments.py              # Payment handler, wallet integration
│   │   ├── escrow.py                # Escrow logic for trades/jobs
│   │   ├── fees.py                  # 3% fee processing logic
│   │   ├── contract_interface.py    # Smart contract read/write interface
│   │   └── utils.py                 # Formatting, validation, etc.
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── ipfs_client.py           # IPFS upload/download
│   │   ├── file_manager.py          # Local file IO
│   │   ├── hash_utils.py            # SHA256/etc. for audit
│   │   └── cache.py                 # Local prompt/model cache
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── key_manager.py           # Wallet/key storage and generation
│   │   ├── session.py               # User session/token logic
│   │   ├── oauth.py                 # (Optional) OAuth/third-party login
│   │   └── permissions.py           # Node/user permissions, admin, etc.
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                # Logging config
│       ├── config.py                # Load/read .env and system config
│       ├── emailer.py               # Notification sender (if needed)
│       ├── validator.py             # Data validation helpers
│       └── timers.py                # Cron, scheduled tasks, etc.
│
├── smart-contracts/
│   ├── PromptMarketplace.sol        # Solidity contract for prompt NFTs/marketplace
│   ├── ComputeRental.sol            # Solidity for compute escrow/fee split
│   └── scripts/
│       ├── deploy.js                # JS script to deploy contracts
│       ├── test_prompt_marketplace.js
│       ├── test_compute_rental.js
│       ├── verify.js                # Script to verify contract on Etherscan
│       └── README.md
│
├── frontend/
│   ├── web/
│   │   ├── package.json
│   │   ├── .env.example
│   │   ├── public/
│   │   │   ├── index.html
│   │   │   └── favicon.ico
│   │   ├── src/
│   │   │   ├── index.js
│   │   │   ├── App.js
│   │   │   ├── api/
│   │   │   │   ├── promptApi.js
│   │   │   │   ├── computeApi.js
│   │   │   │   └── walletApi.js
│   │   │   ├── components/
│   │   │   │   ├── NavBar.js
│   │   │   │   ├── PromptList.js
│   │   │   │   ├── PromptDetail.js
│   │   │   │   ├── PromptUpload.js
│   │   │   │   ├── ComputePool.js
│   │   │   │   ├── JobStatus.js
│   │   │   │   ├── WalletConnect.js
│   │   │   │   ├── FeeDashboard.js
│   │   │   │   └── Ratings.js
│   │   │   └── styles/
│   │   │       └── App.css
│   │   └── README.md
│   │
│   ├── desktop/
│   │   ├── package.json
│   │   ├── main.js
│   │   ├── preload.js
│   │   ├── src/
│   │   │   ├── index.js
│   │   │   ├── App.js
│   │   │   ├── components/
│   │   │   │   ├── NavBar.js
│   │   │   │   ├── PromptList.js
│   │   │   │   ├── ComputeStatus.js
│   │   │   │   ├── WalletConnect.js
│   │   │   │   └── FeeDashboard.js
│   │   │   └── styles/
│   │   │       └── App.css
│   │   └── README.md
│   │
│   └── assets/
│       ├── logo.svg
│       ├── icon.png
│       ├── gremlingpt-banner.png
│       └── custom.css
│
├── docs/
│   ├── ARCHITECTURE.md             # Overview, diagrams, P2P, contract flow
│   ├── API_SPEC.md                 # All API endpoints (REST, gRPC, P2P messaging)
│   ├── PROMPT_SCHEMA.md            # Prompt format, on-chain metadata, licensing, hashes
│   ├── ROADMAP.md                  # Features, milestones, backlog, TODOs
│   ├── ONBOARDING.md               # New user/dev onboarding
│   └── FAQ.md                      # Self-explanatory
│
├── scripts/
│   ├── setup.sh                    # Install all system dependencies
│   ├── run_dev.sh                  # Start dev servers (all parts)
│   ├── migrate_contracts.sh        # Deploy and migrate smart contracts
│   ├── clear_cache.sh              # Reset system caches
│   └── test_all.sh                 # End-to-end smoke test
│
├── .env.example
├── README.md
└── LICENSE
```
