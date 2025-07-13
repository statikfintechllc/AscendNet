# Full System Alpha Pipe-Line

**1. High-Level Sequence:**

*Prompt Upload, Purchase, Compute Job*

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant P2P
    participant Compute
    participant Storage
    participant Payments
    participant SmartContract
    participant OtherNodes

    User->>Frontend: Upload Prompt
    Frontend->>API: POST /prompts/upload (prompt file, meta)
    API->>Storage: Pin to IPFS (ipfs_client.py)
    Storage-->>API: IPFS hash
    API->>P2P: pubsub.broadcast(new prompt meta+hash)
    P2P->>OtherNodes: Gossip prompt meta+hash
    API->>Payments: If paid, initiate payment
    Payments->>SmartContract: Register/transfer prompt (PromptMarketplace.sol)
    SmartContract-->>Payments: On-chain event (ownership, 3% fee)
    Payments-->>API: Payment receipt
    API-->>Frontend: Prompt uploaded & synced
    Frontend-->>User: Prompt available to all nodes

    Note over User,Frontend: Purchase prompt (mirror flow)
    User->>Frontend: Buy Prompt
    Frontend->>API: POST /prompts/buy
    API->>Payments: Start payment/escrow
    Payments->>SmartContract: Transfer funds, 3% fee
    SmartContract-->>Payments: Confirm payment
    Payments-->>API: Confirm
    API->>Storage: Unlock prompt file
    API-->>Frontend: Download for User

    Note over User,Frontend: Compute job request
    User->>Frontend: Request Compute Job
    Frontend->>API: POST /compute/request (job spec)
    API->>P2P: pubsub.broadcast(job)
    P2P->>OtherNodes: Gossip job
    OtherNodes->>API: Bid/accept job
    API->>Compute: Assign to node (worker.py)
    API->>Payments: Lock funds in escrow
    Payments->>SmartContract: Lock funds (ComputeRental.sol)
    Compute->>Storage: Output result (IPFS)
    Compute->>API: Job done
    API->>Payments: Release escrow, 3% to owner
    Payments->>SmartContract: Finalize payment
    API-->>Frontend: Job/result & receipt
    Frontend-->>User: Download/notify
```

⸻

**2. Network Auto-Discovery, Prompt Sync, Job Matching**

```mermaid
flowchart TD
    subgraph "Node Startup"
        node1(backend/p2p/node.py) -->|Loads config, keys| peer_mgr(peer_manager.py)
        peer_mgr --> dht(Distributed Hash Table)
        peer_mgr --> pubsub(PubSub Channels)
        pubsub -->|Broadcast| mesh[Mesh Network Other Nodes]
        dht --> mesh
    end

    subgraph "Prompt Sync"
        storage(ipfs_client.py) -->|Pin prompt| localcache(Local cache)
        localcache --> pubsub
        pubsub -->|Gossip meta| mesh
        mesh -->|Update| localcache
    end

    subgraph "Job Pipelining"
        frontend(Frontend UI) --> api(API: /compute/request)
        api --> pubsub
        pubsub --> mesh
        mesh -->|Bids| api
        api --> compute(Scheduler/Worker)
        compute --> storage
        compute --> payments
        payments --> smartcontract(SmartContract)
        smartcontract --> payments
        payments --> api
        api --> frontend
    end

    subgraph "Payments/Escrow"[Uploading text.txt…]

        api --> payments
        payments --> smartcontract
        smartcontract --> payments
        payments --> api
    end

    style mesh fill:#f8f8ff,stroke:#7b7b7b,stroke-width:1px
```

⸻

**3. System Component Interaction**

```mermaid
graph LR
    Frontend-->|REST/WebSocket|API
    API-->|Function Calls|P2P
    API-->|Function Calls|Compute
    API-->|Function Calls|Storage
    API-->|Function Calls|Payments
    API-->|Function Calls|Auth
    P2P-->|PubSub/DHT|OtherNodes
    Compute-->|Results|Storage
    Payments-->|ETH/SOL|SmartContracts
    P2P-->|Updates|Frontend
    Storage-->|Prompt/Model|Frontend
    API-->|Logs/Alerts|Utils
```

⸻

**4. Single Node Full Lifecycle**

*Prompt upload → job request → payment → receipt*

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Storage
    participant P2P
    participant Compute
    participant Payments
    participant SmartContract

    User->>Frontend: Upload Prompt
    Frontend->>API: /prompts/upload
    API->>Storage: Pin to IPFS
    Storage-->>API: IPFS Hash
    API->>P2P: pubsub.announce(prompt)
    P2P-->>API: Confirm broadcast
    API->>Payments: Initiate payment (buy/upload)
    Payments->>SmartContract: Mint prompt NFT, transfer funds
    SmartContract-->>Payments: Tx confirmed, 3% to owner
    Payments-->>API: Success
    API-->>Frontend: Prompt live everywhere

    User->>Frontend: Request Compute
    Frontend->>API: /compute/request (spec)
    API->>Compute: Add to job_queue
    Compute->>Compute: Sandbox job, monitor resources
    Compute->>Storage: Write results to IPFS/local
    Compute-->>API: Job done, result hash
    API->>Payments: Finalize payment, release escrow
    Payments->>SmartContract: Confirm payout, 3% fee
    Payments-->>API: Done
    API-->>Frontend: Job complete/result
```

⸻

**5. Multi-Node Prompt/Job Sync**

*Prompt posted, all peers instantly see it, jobs distributed and bid upon*

```mermaid
sequenceDiagram
    participant NodeA as Node A (Uploader)
    participant NodeB as Node B (Peer)
    participant NodeC as Node C (Peer)
    participant P2P
    participant Storage

    NodeA->>Storage: Pin Prompt (IPFS)
    Storage-->>NodeA: Hash
    NodeA->>P2P: pubsub.broadcast(prompt meta)
    P2P->>NodeB: Gossip prompt meta+hash
    P2P->>NodeC: Gossip prompt meta+hash
    NodeB->>P2P: Acknowledge, update local cache
    NodeC->>P2P: Acknowledge, update local cache

    NodeB->>P2P: New compute job request (pubsub)
    P2P->>NodeA: Broadcast job req
    P2P->>NodeC: Broadcast job req
    NodeA->>P2P: Bid on job
    NodeC->>P2P: Bid on job
    P2P->>NodeB: Relay bids, select winner
    NodeB->>P2P: Accept bid, trigger escrow/payment
```

⸻

**6. Payment/Escrow Lifecycle**

*Smart contract flow, including 3% fee skimming and escrow release*

```mermaid
sequenceDiagram
    participant Buyer
    participant Seller
    participant API
    participant Payments
    participant SmartContract
    participant FeeWallet

    Buyer->>API: Buy prompt/job
    API->>Payments: Create payment intent
    Payments->>SmartContract: Lock funds in escrow (ComputeRental.sol)
    SmartContract-->>Payments: Escrow confirmed
    Payments-->>Seller: Work notification

    Seller->>API: Deliver prompt/job
    API->>Payments: Confirm delivery
    Payments->>SmartContract: Release escrow, trigger 3% fee split
    SmartContract-->>Payments: Main funds to Seller, 3% fee to FeeWallet
    Payments-->>Buyer: Receipt, unlock download
```

⸻

**4. Node Join, Peer Discovery, Failure, and Recovery**

```mermaid
sequenceDiagram
    participant NewNode
    participant DHT
    participant P2P
    participant Peer1
    participant Peer2
    participant Logger

    NewNode->>DHT: Bootstrap, announce self
    DHT-->>NewNode: Return peer list
    NewNode->>P2P: Connect to mesh, pubsub subscribe
    P2P->>Peer1: Broadcast join event
    P2P->>Peer2: Broadcast join event
    Peer1->>NewNode: Send prompt/compute catalog
    Peer2->>NewNode: Send prompt/compute catalog
    NewNode->>Logger: Log join event

    Peer2-->>P2P: Drops connection (network fail)
    P2P->>Logger: Log peer drop
    P2P->>DHT: Remove Peer2, gossip status
    Peer2->>P2P: Reconnect (after failure)
    DHT-->>Peer2: Peer list (refresh)
    Peer2->>P2P: Resubscribe, catch up state
```

⸻

**5. Real-Time Prompt & Job Auto-Sync**

```mermaid
sequenceDiagram
    participant NodeX as Any Node
    participant P2P
    participant AllNodes as All Connected Nodes

    NodeX->>P2P: Upload new prompt/job meta (pubsub)
    P2P->>AllNodes: Broadcast prompt/job
    AllNodes->>P2P: ACK, update cache
    AllNodes-->>NodeX: Synced, visible in market
    AllNodes->>User: New prompt/job listed instantly
```
