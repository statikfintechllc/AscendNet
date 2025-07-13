<link rel="stylesheet" type="text/css" href="docs/custom.css">
<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
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

<h1 align="center">GremlinGPT: The Real Autonomous Agent v1.0.3</h1>

<div align="center">
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/GremlinGPT">
    <img src="https://img.shields.io/badge/v1.0.3-alpha-darkred?labelColor=black" alt="Build Status"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/FOUNDER_LOG.md">
    <img src="https://img.shields.io/badge/Founder's%20Log-Manifesto-darkred?labelColor=black" alt="Founder's Log"/>
  </a>
  <br/>
  <a href="https://github.com/statikfintechllc">
    <img src="https://img.shields.io/badge/contributors-2-darkred?labelColor=black" alt="Contributors"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/FOUNDER_STATEMENT.md">
    <img src="https://img.shields.io/badge/Founder's%20Log-Statement-darkred?labelColor=black" alt="Founder's Log"/>
  </a>  
</div>
<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/GremlinGPT/docs/GREMLINGPT_AUTONOMY_REPORT.md">
    <img src="https://img.shields.io/badge/The%20Autonomous-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Why"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/GremlinGPT/docs/GREMLINGPT_AUTONOMY_REPORT.md">
    <img src="https://img.shields.io/badge/GremlinGPT%20v1.0.3-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT"/>
  </a>
</div>

---

# Reviewer's Guide

> *This PR brings the JSON traffic datasets up to date and introduces a new command-line interface under `GremlinGPT/run` for interactive NLP engine access.*

## Sequence Diagram for New CLI Interaction

```mermaid
sequenceDiagram
    actor User
    participant CLI as "GremlinGPT/run/cli.py"
    participant Parser as "nlp_engine.parser"
    participant Handler as "backend.chat_handler"

    User->>CLI: Enters command
    CLI->>Parser: parse_nlp(command)
    Parser-->>CLI: Returns NLP analysis results
    CLI->>Handler: chat(command)
    Handler-->>CLI: Returns chat response
    CLI->>User: Displays NLP Engine Output
    CLI->>User: Displays GremlinGPT response
```
