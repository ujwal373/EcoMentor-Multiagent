<div align="center">

# 🌱 **EcoMentor – Agentic Sustainability Coach**

![EcoMentor Banner](./diagrams/system_architecture.png)

[![Kaggle](https://img.shields.io/badge/Kaggle-Project-blue?logo=kaggle)](https://www.kaggle.com/)
[![Agent AI](https://img.shields.io/badge/Agent%20AI-Multi--Agent%20System-green?logo=robotframework)]()
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-black?logo=openai)]()
[![Python](https://img.shields.io/badge/Python-3.10+-yellow?logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend%20API-teal?logo=fastapi)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)]()

</div>

---

### 🧭 **Overview**
EcoMentor is an intelligent **multi-agent system** that helps individuals and small businesses track and reduce their carbon footprint.  
It combines **LLM reasoning**, **tool-driven emission analysis**, and **contextual memory** to deliver actionable sustainability insights — personalized, measurable, and simple to use.

---

### ⚙️ **Architecture**
Below are the three core design visuals that outline EcoMentor’s structure:

| Diagram | Description |
|----------|--------------|
| 🧠 **System Architecture** | Overall flow of agents, APIs, and data layers. |
| 🔄 **Agent Flow Sequence** | How Mentor, Tool, Memory, and Observability agents interact per query. |
| 🧩 **Agent Internals** | Logic and modular design within each agent. |

<p align="center">
  <img src="./diagrams/agent_flow.png" width="85%"/><br>
  <img src="./diagrams/agent_logic.png" width="85%"/>
</p>

---

### 🧠 **Core Concepts Used**
- Multi-Agent System (LLM + Tool + Memory + Observability)
- Custom Tools (API-based carbon calculators)
- Session & State Management (context memory and goal tracking)
- Context Engineering and Compacting
- Logging & Metrics (for user and agent performance tracking)

---

### 🚀 **Tech Stack**
**Backend:** FastAPI + MCP  
**LLM Layer:** OpenAI GPT-4o-mini  
**Memory:** InMemorySessionService / Redis  
**Data Source:** Carbon Interface API / SEAI / ElectricityMap  
**Frontend:** Streamlit (optional dashboard)

---

### 💡 **Example Query**
> *User:* “I drive 10 km daily to work in a petrol car.”  
> *EcoMentor:* “That’s around 2.7 kg CO₂/day. Switching to hybrid could save 30%, or try carpooling twice a week to start small.”

---

### 🧩 **Next Steps**
- [ ] Add FastAPI endpoints (`/chat`, `/calculate`, `/log`)  
- [ ] Integrate Carbon APIs  
- [ ] Implement agent memory for session tracking  
- [ ] Build a minimal Streamlit interface  

---

<div align="center">

🌍 *Built for Kaggle Agent Intensive — Track: Agents for Good*  
⭐ _By Ujwal Mojidra_

</div>
