# Mobile-Developer: Mobile-Mirror

**Structure Build-Out:**

```text
Mobile-Developer: Mobile-Mirror/
│
├── env/
│   │
│   ├── MobileDeveloper.desktop
│   ├── MobileDeveloper.png
│   ├── .env.example
│   ├── apt.txt
│   └── install.sh
│
├── logs/
│   │
│   └── coder-server.log   # ALIGNED
│
├── demos/
│   │
│   └── ...    # SCREEN-SHOTS HERE
│
├── scripts/
│   │
│   ├── remove_mobile.sh
│   ├── start_statik.sh   # 🔁 Starts both statik-server + Mobile-Mirror
│   ├── start_mirror.sh
│   ├── stop_code.sh
│   └── mobile_cli.sh
│
├── mobilemirror/  # 🔥 New SubSystem
│   │
│   ├── backend/
│   │   │
│   │   ├── app.py
│   │   ├── screen_streamer.py
│   │   ├── file_ops.py
│   │   ├── terminal_bridge.py
│   │   ├── mouse_input.py
│   │   └── utils/
│   │       │
│   │       ├── auth.py
│   │       ├── qr_generator.py
│   │       └── logger.py
│   │
│   ├── frontend/
│   │   │
│   │   ├── public/
│   │   │   │ 
│   │   │   └── manifest.json
│   │   │
│   │   └── src/
│   │       │
│   │       ├── App.jsx
│   │       ├── Terminal.jsx
│   │       ├── Editor.jsx
│   │       ├── FileManager.jsx
│   │       ├── ScreenView.jsx
│   │       ├── MouseController.js
│   │       └── api.js
│   │   
│   ├── config/
│   │   │
│   │   ├── system.toml
│   │   └── tailscale_setup.sh
│   │   
│   └── system
│        │   
│        └── services
│           │
│           ├── touchcore_backend.log
│           └── touchcore_frontend.log
│   
├── docs/
│   │
│   ├── README.md
│   ├── SYSTEM_OVERVIEW.md
│   └── STRUCTURE.md
│
└── LICENSE                    # Open-use: GodaCore-style
```
