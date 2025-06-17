<link rel="stylesheet" type="text/css" href="docs/custom.css">
<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendNet/blob/master/About Us/LICENSE.md">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE.md">
    <img src="https://img.shields.io/badge/AscendNet%20AlphaWave-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/Why-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Why"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/SFTi-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT"/>
  </a>
  <a href="https://ko-fi.com/statikfintech_llc">
    <img src="https://img.shields.io/badge/Support-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Support"/>
  </a>
  <a href="https://patreon.com/StatikFinTech_LLC?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink">
    <img src="https://img.shields.io/badge/SFTi-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="SFTi"/>
  </a>

# AscendNet Full Architecture and Build Plan

</div>

*Full Alpha Proto-Type. Funding Needed For build-out*

*By: StatikFinTech, LLC*

```text
/AscendNet/
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

---

## AscendNet/ — Top-Level

	•	README.md: Explains the project, architecture, setup instructions.
	•	LICENSE: Open source (or your custom “pay me 3%” license).
	•	.env.example: Example environment variables for dev/prod (DB_URI, P2P_SEED, WALLET_PRIVATE_KEY, etc.).
	•	scripts/: For setup, dev, and E2E testing.

⸻

## /backend/ — The Brains and Brawn

> Handles all API logic, p2p node operations, compute pooling, storage, crypto payments, user auth, utilities.

⸻

**api/ (Public/Private REST, Pipelines, Gateway)**

	•	main.py:
	•	FastAPI entrypoint
	•	Initializes routers, middleware, CORS, logging.
	•	Imports all route modules.
	•	Calls into P2P subsystem, compute, payments, etc.
	•	Logs API calls, errors (via logger.py).
	•	routes_prompts.py:
	•	Endpoints:
	•	/prompts/list — list all prompts (local and discovered P2P)
	•	/prompts/upload — upload prompt to IPFS & broadcast hash
	•	/prompts/buy — purchase prompt via smart contract
	•	/prompts/rate — rate, review, or flag a prompt
	•	Calls:
	•	storage/ipfs_client.py to push prompt
	•	payments/payments.py for transactions
	•	p2p/messaging.py to broadcast new prompt
	•	models.py for validation
	•	routes_compute.py:
	•	Endpoints:
	•	/compute/request — request job, broadcast to P2P
	•	/compute/bid — nodes bid on job
	•	/compute/accept — job acceptance/escrow
	•	/compute/status — fetch current/completed jobs
	•	Calls:
	•	p2p/pubsub.py for broadcast
	•	compute/scheduler.py for matching
	•	payments/escrow.py for handling funds
	•	routes_users.py:
	•	Endpoints: registration, login, wallet connect
	•	Integrates with auth/session.py, auth/key_manager.py
	•	On login, registers node to network
	•	models.py:
	•	Pydantic schemas for all API I/O
	•	Ensures prompt/job/user structures are valid throughout the stack
	•	dependencies.py:
	•	Auth decorators, rate limiting, request context
	•	errors.py:
	•	Custom FastAPI exception handlers, error logging

⸻

**p2p/ (Peer Networking, Node Auto-Discovery, Messaging)**

	•	Every node is both a server and client
	•	Handles all peer broadcast, prompt/job gossip, pubsub, DHT, connection management
	•	node.py:
	•	Node startup: loads keys, discovers other peers using bootstrap list/DHT
	•	Registers itself (and available prompts, compute capacity) to the mesh
	•	Auto-connect on launch (LAN, mesh, or WAN) using libp2p/NATS
	•	Maintains node health, heartbeat, reconnects if dropped
	•	Logs network activity, peer join/leave, and errors
	•	peer_manager.py:
	•	Maintains peer lists, reputations, and bans bad actors
	•	Handles new peer join, broadcast of local prompt/compute catalog to new arrivals
	•	Routes requests to the least-laggy peer
	•	messaging.py:
	•	Serializes/deserializes messages
	•	Standardizes protocol for: prompt trade, job offer, bid, status, and reviews
	•	dht.py:
	•	Runs the distributed hash table for peer discovery and decentralized catalog lookup (prompts, jobs, node stats)
	•	pubsub.py:
	•	Pub/sub channels:
	•	Prompts
	•	Compute Jobs
	•	Payments
	•	System Announcements
	•	All events are published/subscribed here for real-time updates
	•	utils.py:
	•	Common helpers (serialization, unique IDs, crypto functions)

⸻

**compute/ (Pipelined Job Scheduling & Execution)**

	•	Node can act as both client (submits jobs) and worker (executes jobs)
	•	scheduler.py:
	•	Orchestrates incoming compute requests, matches with local or remote nodes
	•	Negotiates bids, awards jobs, updates statuses
	•	Ensures 3% cut is pipelined to payment on success
	•	worker.py:
	•	Actually runs the compute task (in sandbox)
	•	Handles inference, fine-tuning, etc.
	•	Monitors for malicious or broken code
	•	job_queue.py:
	•	Manages incoming, active, completed jobs
	•	Queues up jobs, cancels, retries, and purges
	•	Connects with resource_monitor.py to ensure load balancing
	•	resource_monitor.py:
	•	Tracks node’s resources (CPU, RAM, GPU, disk)
	•	Updates network with current status
	•	sandbox.py:
	•	Runs all jobs in Docker containers or lightweight sandboxes
	•	Isolates client code for security
	•	Cleans up after each run
	•	utils.py:
	•	Helpers for job serialization, task logging

⸻

**payments/ (Crypto Payments, Escrow, Fees)**

	•	All prompt/compute trades flow through here
	•	Manages wallet, smart contract interaction, and fee accounting
	•	payments.py:
	•	Handles ETH/SOL/ERC-20 token payments
	•	Initiates payment flows for prompt purchases, compute jobs
	•	escrow.py:
	•	Escrow logic for jobs (funds held until job is complete)
	•	Releases payment when the work is confirmed (3% auto skimmed)
	•	fees.py:
	•	All 3% logic is here, pipelined into wallet
	•	Calculates and verifies fee transfers per transaction
	•	contract_interface.py:
	•	Reads/writes to deployed smart contracts (smart-contracts/)
	•	Encapsulates contract calls, event listening, on-chain receipts
	•	utils.py:
	•	Crypto formatting, key validation, transaction serialization

⸻

**storage/ (Distributed File, Prompt, and Model Management)**

	•	All prompt chains, models, result files are here, stored locally and/or on IPFS
	•	ipfs_client.py:
	•	Uploads files to IPFS/Filecoin, fetches them back by hash
	•	Validates hashes against what is stored locally
	•	file_manager.py:
	•	Local file IO for prompts/models
	•	Handles temp storage, cleanup, permissioning
	•	hash_utils.py:
	•	Hashes all prompts/models for audit, deduplication, verification
	•	cache.py:
	•	Fast local cache for frequently used assets

⸻

**auth/ (Wallets, Sessions, Permissions)**

	•	Wallet management, user keys, node identity, and access controls
	•	key_manager.py:
	•	Generates/imports wallets and signing keys
	•	Exports/imports mnemonic, private keys
	•	session.py:
	•	Handles user sessions (JWTs, tokens, session cookies)
	•	Validates API/auth for each request
	•	oauth.py:
	•	(Optional) Third-party logins for normies
	•	permissions.py:
	•	Role management, admin, contributor, job runner, etc.

⸻

**utils/ (Shared Tools)**

	•	Logging, config, email notifications, validation, scheduling
	•	logger.py:
	•	Central logging (rotating files, levels, external Sentry/etc.)
	•	Logs to stdout/file, pipes errors to Slack/Discord/etc.
	•	config.py:
	•	Loads env vars from .env, merges with runtime overrides
	•	Handles secrets securely
	•	emailer.py:
	•	Sends notifications to users (job complete, bid accepted, etc.)
	•	validator.py:
	•	Centralized data validation functions
	•	timers.py:
	•	For scheduled maintenance tasks, periodic cleanup, auto-updates

⸻

**/smart-contracts/ (On-chain Marketplace and Compute Pooling)**

	•	PromptMarketplace.sol:
	•	Solidity contract for prompt NFT/token listing, transfer, rating, and payments
	•	Handles ownership, price, transaction history, 3% fee split
	•	ComputeRental.sol:
	•	Solidity for compute escrow—accepts funds, releases to compute provider, cuts fee for platform
	•	scripts/:
	•	deploy.js: deploy contracts to testnet/mainnet
	•	test_*.js: contract logic/unit tests (use Hardhat/Truffle/Foundry)
	•	verify.js: verify contracts on Etherscan
	•	README.md: explains deployment and upgrade process

⸻

## /frontend/ (UI: Web, Desktop, Assets)

**web/**

	•	package.json, .env.example: dependencies, environment
	•	public/: HTML, favicon, static files
	•	src/
	•	index.js: Entry point, loads App
	•	App.js: Main app shell, routes, error boundaries
	•	api/: Connects to backend REST, p2p events, wallet
	•	promptApi.js, computeApi.js, walletApi.js
	•	components/: UI for prompt lists, upload, compute pools, wallet connect, job status, fee dashboard, ratings/reviews, navbar, etc.
	•	styles/: Custom CSS (App.css, etc.)
	•	README.md: Frontend build instructions

**desktop/**

	•	Electron/Tauri wrapper for web UI, adds local OS integration

⸻

**assets/**

	•	Logos, icons, banners, brand styles

⸻

**/docs/ (Everything to get someone up to speed)**

	•	ARCHITECTURE.md: P2P, networking, API, pipeline, flowcharts
	•	API_SPEC.md: All endpoints, data types, message protocols
	•	PROMPT_SCHEMA.md: Prompt format, metadata, licensing, on-chain info
	•	ROADMAP.md: Next features, milestones, backlog
	•	ONBOARDING.md: For new devs/contributors
	•	FAQ.md: “Why isn’t my node connecting?”

⸻

**/scripts/ (DevOps/Tooling)**

	•	setup.sh: Installs dependencies, sets up virtualenv, runs migrations, builds frontend, etc.
	•	run_dev.sh: Runs backend, p2p node, and frontend locally for dev
	•	migrate_contracts.sh: Deploys/updates smart contracts
	•	clear_cache.sh: Nukes and resets all local caches
	•	test_all.sh: Full end-to-end system smoke test

⸻

**Pipelining/Networking/Auto-Discovery Overview**

	•	On Launch:
	•	backend/p2p/node.py autoloads config, private key, bootstraps to P2P mesh
	•	Discovers peers (via DHT/pubsub/mesh), shares available prompts/computing
	•	Prompt Sync:
	•	Any prompt uploaded/updated is immediately broadcast via pubsub.py, appears in every connected node’s prompt list
	•	Job Requests:
	•	Compute jobs are pipelined through /compute/request and distributed via P2P channels
	•	Scheduler matches jobs to nodes, escrow/fees handled by payments module
	•	UI:
	•	Users see up-to-date available prompts, compute, and services instantly
	•	Can request, bid, rate, buy, or upload with a click
	•	Logging:
	•	Every request, trade, error, job, and connection logged centrally for troubleshooting and analytics

⸻

**Environment/Dependency Management**

	•	Python backend: Poetry or pipenv (pyproject.toml/Pipfile)
	•	Frontend: yarn/npm, .env for API URLs, keys
	•	Smart contracts: Hardhat, Foundry, or Truffle (package.json in contracts/scripts)
	•	Scripts: Bash and/or Makefile for repeatable dev/prod workflows

---

```text
┌────────────────────────────┐
│        User/Node           │
│ (Web, Desktop Frontend)    │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│        Frontend UI         │
│ (web/src/ or desktop/src/) │
└────────────┬───────────────┘
             │REST/gRPC/WebSocket (Prompt/Compute APIs)
             ▼
┌────────────────────────────┐
│   backend/api/main.py      │
│ (FastAPI Entrypoint)       │
└────────────┬───────────────┘
             │
             ├──▶ /api/routes_prompts.py ─────┐
             │       │                        │
             │       ▼                        │
             │   Calls IPFS/file_manager      │
             │   Broadcast to P2P/pubsub      │
             │   Payments (buy/upload)        │
             │                                │
             ├──▶ /api/routes_compute.py ─────┐
             │       │                        │
             │       ▼                        │
             │   Job Scheduling/Matching      │
             │   Broadcast Job to P2P/pubsub  │
             │   Escrow/Payment (bid, accept) │
             │                                │
             └──▶ /api/routes_users.py        │
                     │                        │
                     ▼                        │
              Auth, Wallet, Node Register     │
                                              │
                                              ▼
                         ┌────────────────────────────────┐
                         │       backend/p2p/             │
                         │    (Node, PubSub, DHT, Peer)   │
                         └──────────┬──────────────┬──────┘
                                    │              │
       P2P Msgs, Prompt/Job Gossip  │   Peer Discovery/DHT
           (pubsub.py)              │   (dht.py)
                                    ▼
                          All Connected Nodes
                          (P2P Mesh: LAN/WAN)
                                    │
           ┌─────────────┬──────────┴─────────┬────────────┐
           │             │                    │            │
   Prompt/Job  ◀─────────┘        ◀───────────┘    Payments/Escrow
   Sync                │   Broadcast           │    Update Balances
                       ▼                       ▼
             backend/compute/          backend/payments/
           (Scheduler, Worker)      (payments, escrow, fees,
               Job Queue)              smart contract)
                       │
         Runs Jobs in Sandbox (Docker)
         or Sends Job to Other Node
                       │
                Store/Fulfill Results
                       ▼
           backend/storage/
         (ipfs_client, file_manager,
           hash_utils, cache)
                       │
           Local or IPFS/Remote Store
                       │
       ┌───────────────▼─────────────────────┐
       │   Logs (backend/utils/logger.py)    │
       │   - All API calls, P2P events       │
       │   - Job submissions, completions    │
       │   - Errors, warnings, system stats  │
       └─────────────────────────────────────┘

               ▲                          ▲
               │                          │
   Notifications (Email, UI pop, etc)     │
 (backend/utils/emailer.py → Frontend)    │
                                          │
        On-Chain (Smart Contracts)        │
      (payments/contract_interface.py)    │
   ↔  smart-contracts/PromptMarketplace   │
   ↔  smart-contracts/ComputeRental       │
                                          │
   (Escrow, Fees, Ownership, Ratings)     │
                                          │
```

## ────────────── AUTO-DISCOVERY AND PIPELINING ──────────────

1. **Node Startup:**  
   - backend/p2p/node.py loads keys/config, connects to mesh, announces itself
   - Pulls prompt, compute, peer status from mesh (pubsub, DHT)

2. **Prompt Listing:**  
   - On prompt upload or sync, node adds prompt to IPFS  
   - Broadcasts prompt metadata/hash via pubsub  
   - All nodes update local cache, reflect new prompts

3. **Job Scheduling:**  
   - Node posts compute job (via API or direct pubsub)  
   - Other nodes respond with bids/offers (via pubsub, routes, or gRPC)  
   - Winning node’s scheduler accepts, payment escrow triggered

4. **Execution and Storage:**  
   - Worker node runs job in sandbox, stores result (local/IPFS)  
   - Notifies network/job owner of completion

5. **Payment/Escrow:**  
   - On successful delivery, escrow releases payment  
   - 3% fee skimmed to owner wallet

6. **Logging, Monitoring:**  
   - All interactions logged (local file, optional cloud/SIEM)  
   - Errors, jobs, peer drops auto-notify admin/dev

7. **Frontend UI:**  
   - Queries backend API for up-to-date state  
   - Subscribes to websocket/push events for real-time updates  
   - UI reflects live status, peer/market stats, prompt lists, job bids

## ────────────── DEPENDENCY MANAGEMENT ──────────────

- **Backend:**  
  - `pyproject.toml` or `Pipfile` (FastAPI, libp2p/NATS, Docker, web3, ipfshttpclient, etc)
  - `.env` file loaded at boot
- **Frontend:**  
  - `package.json` (React/Vue, ethers.js/web3.js, socket.io-client, etc)
- **Smart Contracts:**  
  - `package.json` (hardhat, ethers, truffle, etc)
- **Scripts:**  
  - `setup.sh`, `run_dev.sh` to build/run all

```text
[USER] –UI–> [BACKEND/API] –REST/gRPC–> [P2P+JOBS+PAYMENTS] –P2P–> [OTHER NODES]
|                           |               |                 |
(UI update)          (Prompt Sync)     (Job Match/Bid)    (On-chain Escrow)
```

---

## **Summary Table**

```text
| Layer           | Role                                 | Inputs            | Outputs               | Interacts With                |
|-----------------|--------------------------------------|-------------------|-----------------------|-------------------------------|
| Frontend        | User interface                       | User, API, Websockets | UI actions, display   | Backend API, P2P Events       |
| API             | REST/gRPC interface                  | Frontend, Nodes   | Validated actions      | Compute, P2P, Payments, Auth  |
| P2P             | Node discovery, mesh, gossip         | Local, Remote     | Prompts, Jobs, Peers   | All nodes, Local API/Compute  |
| Compute         | Job scheduling, sandboxing, resource | API, P2P, Auth    | Results, Status        | Storage, P2P, Payments        |
| Payments        | Crypto, escrow, 3% fees, smart contract | API, Compute   | Funds, status          | Contracts, Wallet, UI         |
| Storage         | IPFS/local, cache, hash audit        | Compute, API      | Prompt/model files     | API, P2P, UI                  |
| Auth            | Wallets, sessions, permissions       | API               | JWTs, keypairs         | API, P2P                      |
| Utils           | Logging, config, alerts              | Everything        | Logs, notifications    | Admin/dev, UI                 |
```

---

## **Visually: Pipeline Sequence Example**

```text
[User/Frontend]
│
│  (Upload Prompt)
▼
[API: /prompts/upload]
│
│–file–> [storage/ipfs_client.py]
│–meta–> [p2p/pubsub.py] –P2P Gossip–> [Other Nodes]
│
│–pay–> [payments/payments.py] –ETH–> [Smart Contract]
│
▼
[UI: PromptList Refreshes Everywhere]
```

---

```text
[User/Frontend]
│
│ (Request Compute Job)
▼
[API: /compute/request]
│
│–job–> [p2p/pubsub.py] –P2P–> [Other Nodes]
│
│–bid–> [compute/scheduler.py] –select–> [Winning Node]
│
│–escrow–> [payments/escrow.py] –ETH–> [Smart Contract]
│
▼
[compute/worker.py]
│
│–results–> [storage/ipfs_client.py]
│–notify–> [API/UI]
│–release–> [escrow: smart contract, 3% fee]
```
