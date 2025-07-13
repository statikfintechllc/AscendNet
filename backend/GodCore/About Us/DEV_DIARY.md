<link rel="stylesheet" type="text/css" href="docs/custom.css">
<div align="center">
  <a
href="https://github.com/statikfintechllc/GodCore/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/GodCore/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0.3-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>

<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/Why-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Why"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/GremlinGPT-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT"/>
  </a>
</div>

  <div align="center">
  <a href="https://ko-fi.com/statikfintech_llc">
    <img src="https://img.shields.io/badge/Support-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Support"/>
  </a>
  <a href="https://patreon.com/StatikFinTech_LLC?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink">
    <img src="https://img.shields.io/badge/SFTi-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="SFTi"/>
  </a>
</div>

# GodCore: Dev Diary & Gotchas

---

## Releases

- **v0.1.0** — Fully local Mistral backend and dashboard UI  
- **v0.2.0** — Added ngrok integration (buggy background image centering; otherwise fully operational)  
- **v0.3.0 (WIP):**
  - **GPT integration**
  - Multi-model backend debugging
  - API feed and backend “no-fail” patching
  - All features accessible in dashboard (errors currently due to backend failures)
  - Background image now centers; title bar bug (floats/hides) under review

---

## v0.3.0 Progress Log

### Rapid Prototyping & Key Milestones

- **Sunday–Wednesday, v0.1.0 → v0.3.0**  
  *Part-time (~4 hours/day, 3 days):*
    - Prototyped a full GPT wrapper for **free ChatGPT (alpha)** with seamless local integration.
    - Persistent chat memory added to UI; system storage and reloads now work.
    - UI now live: chat, local memory, reloads, error handling.
    - End-to-end reproducibility: installer runs from clone on clean system.

---

## The Wheel of Pain (Llama/Llava Wheel Build Hell)

- **Problem:**  
  Every time `llama-cpp-python` or Llava updated, CUDA support would break, and building a working Python wheel was a multi-day process.

- **Root Cause:**  
  Hidden in `llama_cpp/` are config checks like:

      if (LLAVA)
      if (GGML)
      if (DGGML)
      if (DLLAMA)

  Miss the right combo or option, and the build silently disables features or fails.

- **Solution:**  
  Automated proper build flags in `./install.sh`—just clone and run.

- **Lesson:**  
  When builds break, read the source and hunt CMake/bash logic.

---

**If you’re stuck, open an issue. If you fixed something, PR your solution so the next person doesn’t have to suffer.**

> *“I killed this in 3 hours so you don’t have to lose 3 days. You’re welcome.”*

*StatikFinTech, LLC*
