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

# Pipeline Walkthrough (Detailed, Step-by-Step)

</div>

0. Environment/Setup (Prereq Layer)

**Initial Walk-Through**

	•	User runs scripts/setup.sh:
	•	Installs Python dependencies (poetry or pipenv for backend, npm/yarn for frontend, Hardhat/Foundry for smart contracts).
	•	Sets up .env files, initial key generation, Docker if needed.
	•	Migrates/deploys contracts (scripts/migrate_contracts.sh).
	•	Runs local IPFS node or connects to remote.
	•	Everything loads config from .env for secret keys, API endpoints, etc.
	•	run_dev.sh launches backend API, P2P node, and frontend in dev mode.

⸻

1. Node Startup & Peer Discovery

**backend/p2p/node.py**

	•	Loads node keys from auth/key_manager.py or generates new ones.
	•	Connects to existing mesh (bootstraps from peer list, DHT, or pubsub).
	•	Announces node presence (with available prompts and compute resources).
	•	Auto-discovery: DHT and pubsub channels ensure every new node knows what the network can offer (no SaaS middleman).

**backend/p2p/peer_manager.py**

	•	Keeps active list of known peers, updates on join/leave.
	•	Gossip protocol keeps prompt/job catalogs in sync.
	•	Handles peer scoring/banning (so no one DDoSes the network with fake jobs).

⸻

2. Prompt Upload, Listing, and Sync

**User Action:**

	•	On the frontend, user hits “Upload Prompt” or “List Prompts”.

**Pipeline:**

	•	frontend/web/src/components/PromptUpload.js → POST /api/prompts/upload
	•	API receives:
	•	Metadata + file (prompt, description, price, tags, etc.)
	•	Backend:
	•	routes_prompts.py receives call.
	•	Calls storage/ipfs_client.py to pin the file (returns IPFS hash).
	•	Calls p2p/pubsub.py to broadcast prompt metadata to all connected nodes.
	•	Writes to local cache (storage/cache.py), updates index.
	•	If price > 0: invokes payments/payments.py to create a payment link or smart contract call.
	•	Logs everything via utils/logger.py.
	•	P2P Layer:
	•	Every node (even if offline, when they rejoin) receives latest prompt metadata, IPFS hash, owner address, ratings, and licensing.
	•	Network now shows new prompt everywhere.
	•	Frontend updates:
	•	Calls /api/prompts/list regularly or listens via websocket.
	•	UI updates instantly.

⸻

3. Prompt Purchase & Payment Flow

**User Action:**

	•	User clicks “Buy Prompt” (either web or desktop).

**Pipeline:**

	•	frontend/web/src/components/PromptDetail.js → POST /api/prompts/buy (with prompt hash, user wallet)
	•	API receives:
	•	routes_prompts.py → checks eligibility, price.
	•	Calls payments/payments.py to initiate crypto transfer (ETH/SOL/ERC20).
	•	Payment is routed through payments/escrow.py—held until prompt unlock is confirmed.
	•	Calls payments/contract_interface.py to interact with PromptMarketplace.sol.
	•	On payment confirmation (on-chain event), grants user access to prompt (downloads from IPFS).
	•	Fees: payments/fees.py ensures 3% is skimmed and sent to your wallet.
	•	Transaction logged everywhere.
	•	UI:
	•	User receives prompt file + receipt.
	•	All status/updates via websocket or UI refresh.

⸻

4. Compute Job Request, Matching, and Execution

**User Action:**

	•	User hits “Request Compute” (e.g., wants inference, fine-tuning, or arbitrary code run).

**Pipeline:**

	•	frontend/web/src/components/ComputePool.js → POST /api/compute/request (job spec, files, reward, requirements)
	•	API receives:
	•	routes_compute.py → parses job, validates via models.py.
	•	Calls p2p/pubsub.py to broadcast job to network.
	•	All nodes with matching resources receive job details.
	•	Bidding/Matching:
	•	Nodes respond with offers (/api/compute/bid), price, and ETA.
	•	compute/scheduler.py tracks all bids, selects best node.
	•	Acceptance: compute/scheduler.py triggers payments/escrow.py to lock user funds.
	•	Status is tracked in job_queue.py.
	•	Execution:
	•	compute/worker.py runs job in a Docker sandbox (compute/sandbox.py).
	•	Progress reported via P2P (job status messages).
	•	On completion, output is stored (storage/ipfs_client.py or file_manager.py).
	•	Result:
	•	Job submitter notified (via websocket, email, or UI).
	•	Payment released from escrow on confirmation, 3% fee auto-disbursed.
	•	Logs everywhere.

⸻

5. Peer-to-Peer Networking & Auto-Sync

**At all times:**

	•	All nodes sync catalogs of prompts, jobs, compute resources using p2p/pubsub.py and p2p/dht.py.
	•	Any change (new prompt, node join/leave, job status) is broadcast.
	•	Catalog is always up-to-date—even after node downtime (rehydrated from the mesh).
	•	No SaaS. No central DB. If one node goes down, others take over.

⸻

6. Logging, Monitoring, and Notifications

**Every call and action:**

	•	utils/logger.py:
	•	Logs API requests, errors, job status, payments, peer events.
	•	Supports log rotation, error levels, and external sinks (Sentry, ELK, Discord webhook, etc.).
	•	utils/emailer.py:
	•	Sends out email alerts, confirmations, or error notifications (optional).

⸻

7. Smart Contracts and Escrow

**Any payment event:**

	•	API calls payments/contract_interface.py, which wraps ethers/web3 calls to deployed smart contracts:
	•	PromptMarketplace.sol: NFT ownership, trading, rating, on-chain metadata.
	•	ComputeRental.sol: Locks user payment, releases to job-runner on completion, enforces 3% cut.
	•	Events are listened for and confirmed before releasing assets.

⸻

8. UI Sync and Real-Time Display

**Frontend Proccess**

	•	Frontend polls API (or listens via websockets):
	•	Live updates for prompt/job status, peer count, node health, available resources.
	•	All actions visible and reflected across every node instantly.

⸻

**Pipelining/Networking in Practice**

	•	Every module only cares about its contracted interface.
	•	Everything async, event-driven.
	•	Every function call is logged.
	•	No central control, ever.

⸻

**Security & Resilience**

	•	All jobs run in Docker or equivalent sandboxes (never trust the network).
	•	All payments/escrows are on-chain, immutable.
	•	All node keys are local, never leave disk.
	•	All prompt/job hashes are verified for integrity.
	•	No open inbound ports unless explicitly configured—NAT punching, local relays.
	•	IPFS ensures prompt/model data is always accessible, even if originator is offline.

⸻

**Final Step: Dev/Prod Pipeline**

	•	Local dev:
	•	scripts/run_dev.sh spins up everything (backend, frontend, node).
	•	Contracts: deploy to testnet (scripts/migrate_contracts.sh).
	•	All nodes in local mesh, can simulate failures, scale tests.
	•	Production:
	•	Nodes auto-join global mesh, auto-register, and sync.
	•	Payments go to mainnet, 3% fee real.

⸻

## Visual TL;DR

Every user is their own mini-marketplace and cloud.
Prompts, compute, payments, and catalog auto-sync with every other node.
Kill the SaaS. Collect your 3%. Annoy everyone.
