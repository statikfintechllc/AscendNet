**A. Infra/Component Diagram: Full System**

```mermaid
graph TD
    subgraph User Devices
        FE1[Web Frontend]
        FE2[Desktop App]
    end

    subgraph Backend/API Node
        API[FastAPI API]
        P2P[P2P Mesh Layer]
        Compute[Compute Worker/Scheduler]
        Storage[Storage — IPFS, Local]
        Payments[Payments & Escrow]
        Auth[Wallets & Auth]
        Utils[Logging, Alerts, Validation]
    end

    subgraph Blockchain
        SC1[PromptMarketplace.sol]
        SC2[ComputeRental.sol]
    end

    subgraph Distributed Storage
        IPFS1[IPFS Node]
        IPFS2[Filecoin/Other IPFS]
    end

    FE1 --REST/gRPC/WebSocket--> API
    FE2 --REST/gRPC/WebSocket--> API
    API --p2p event--> P2P
    API --call--> Compute
    API --call--> Payments
    API --call--> Storage
    API --call--> Auth
    API --call--> Utils

    P2P --mesh--> P2P
    P2P --pubsub--> Compute
    P2P --pubsub--> API
    P2P --peer sync--> Storage

    Compute --store--> Storage
    Compute --notify--> API
    Compute --job gossip--> P2P

    Payments --smart contract--> SC1
    Payments --smart contract--> SC2

    Storage --pin/unpin--> IPFS1
    Storage --fetch--> IPFS2

    Auth --JWT, wallet--> API
    Utils --logs--> API

    %% Connections to other nodes
    P2P --peer connection--> P2P
```

⸻

**B. P2P Network Infra: Multi-node Overlay**

```mermaid
graph LR
    subgraph Node_A
        APIN1[API]
        P2PN1[P2P]
        CompN1[Compute]
        StorN1[Storage]
    end

    subgraph Node_B
        APIN2[API]
        P2PN2[P2P]
        CompN2[Compute]
        StorN2[Storage]
    end

    subgraph Node_C
        APIN3[API]
        P2PN3[P2P]
        CompN3[Compute]
        StorN3[Storage]
    end

    APIN1--REST-->P2PN1
    APIN2--REST-->P2PN2
    APIN3--REST-->P2PN3

    P2PN1--P2P mesh-->P2PN2
    P2PN1--P2P mesh-->P2PN3
    P2PN2--P2P mesh-->P2PN3

    P2PN1--pubsub/job gossip-->CompN2
    P2PN2--pubsub/job gossip-->CompN3
    P2PN3--pubsub/job gossip-->CompN1

    StorN1--IPFS-->StorN2
    StorN2--IPFS-->StorN3
    StorN3--IPFS-->StorN1
```

⸻

**C. Main Event Flowcharts (Process-Oriented)**

1. *Prompt Upload/Propagation*

```mermaid
flowchart TD
    A[User uploads prompt — UI]
    B[API receives /prompts/upload]
    C[Pin to IPFS/storage]
    D[Broadcast meta via P2P pubsub]
    E[All nodes update prompt catalog]
    F[Prompt listed on UI globally]

    A-->B-->C-->D-->E-->F
```

⸻

2. *Compute Job Request, Bidding, Execution, Settlement*

```mermaid
flowchart TD
    U[User requests compute job]
    AP[API receives /compute/request]
    P[P2P pubsub broadcasts job]
    N[Nodes bid/offer resources]
    S[Scheduler selects winner]
    E[Escrow funds held]
    J[Job runs in worker/sandbox]
    R[Result uploaded to storage]
    V[User notified, gets result]
    $[Escrow/fee settles to wallets]

    U-->AP-->P-->N-->S-->E-->J-->R-->V-->$
```

⸻

3. *Node Startup/Discovery/Sync*

```mermaid
flowchart TD
    X[Node boots]
    Y[Loads config, keys]
    Z[Bootstraps to DHT]
    P[P2P mesh connects to peers]
    C[Announces self, catalogs to network]
    Q[Pulls all prompt/job/peer lists]
    R[UI and local cache update]

    X-->Y-->Z-->P-->C-->Q-->R
```

⸻

4. *Payment/Escrow/Settlement*

```mermaid
flowchart TD
    B[Buyer initiates purchase/job]
    AP[API triggers payment]
    SC[Smart Contract holds escrow]
    S[Seller delivers prompt/job]
    V[Buyer/API confirms delivery]
    F[Smart contract releases funds]
    O[3% fee to owner, rest to seller]

    B-->AP-->SC
    SC-->|On delivery|S
    S-->V
    V-->F
    F-->O
```

⸻

5. *Logging, Alerts, Monitoring*

```mermaid
flowchart TD
    E[Each API/P2P event]
    L[Logger writes to file/SIEM]
    A[Alerts if error or anomaly]
    D[Dashboard shows logs/status]
    U[Admins/devs notified]

    E-->L-->D
    L-->A-->U
```

⸻

**D. Real-Time Sync at a Glance**

```mermaid
flowchart TD
    PU[Prompt uploaded — any node]
    PUB[P2P pubsub broadcast]
    PN[All peers receive/update cache]
    UI[Frontend UI refreshes market]

    PU-->PUB-->PN-->UI
```
