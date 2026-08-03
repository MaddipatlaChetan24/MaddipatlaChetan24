<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=260&color=0:0F2027,50:203A43,100:2C5364&text=Maddipatla%20Chetan&fontSize=50&fontAlignY=38&animation=fadeIn"/>

<h1 align="center">I'm Maddipatla Chetan</h1>

<sub><i>AI Engineer · ML Researcher · B.Tech Computer Science</i></sub>

<br>

<img src="https://readme-typing-svg.demolab.com?font=Poppins&weight=700&size=30&duration=3500&pause=1000&color=00C2FF&center=true&vCenter=true&width=900&lines=AI+Engineering;Generative+AI;Large+Language+Models;Retrieval-Augmented+Generation;Agentic+AI;Multi-Agent+Systems;Deep+Learning;Building+Intelligent+AI+Applications"/>

<br>

**Turning research into production-grade AI systems** — LLMs, RAG, agents, and deep learning built end-to-end.

<br>

<img src="https://komarev.com/ghpvc/?username=MaddipatlaChetan24&style=for-the-badge&color=0e75b6"/>

</div>

---

<h2 align="center">About Me</h2>

I'm **Maddipatla Chetan**, a **B.Tech Computer Science** student specializing in **Artificial Intelligence and Machine Learning**.

I design and build AI systems end-to-end — **Generative AI applications, LLM-powered products, RAG pipelines, agentic workflows, and computer vision solutions** — with a foundation in **NLP, Deep Learning, and MLOps**.

My focus: take an idea, validate it, build it, evaluate it, and ship it — bridging research and production with an engineering mindset.

---

<h2 align="center">What I Build</h2>

<p align="center">

| AI Applications | LLM-powered products, RAG chatbots, agentic systems |
|---|---|
| Computer Vision | Real-time detection, surveillance intelligence |
| Model Fine-Tuning | Parameter-efficient adaptation (LoRA / QLoRA) |
| AI Infrastructure | APIs, retrieval pipelines, evaluation, deployment |

</p>

---

<h2 align="center">Tech Stack</h2>

### Programming

<p align="center">
<img src="https://skillicons.dev/icons?i=python,cpp,java&perline=5"/>
</p>

### AI / Machine Learning

<p align="center">
<img src="https://skillicons.dev/icons?i=pytorch,tensorflow,huggingface,langchain,openai&perline=7"/>
</p>

### AI Frameworks & Libraries

<p align="center">
<img src="https://img.shields.io/badge/Transformers-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"/>
<img src="https://img.shields.io/badge/Vector%20Databases-336791?style=for-the-badge"/>
</p>

### Backend

<p align="center">
<img src="https://skillicons.dev/icons?i=fastapi,flask&perline=4"/>
</p>

### Databases

<p align="center">
<img src="https://skillicons.dev/icons?i=postgres,mongodb,mysql&perline=5"/>
</p>

### Tools & Cloud

<p align="center">
<img src="https://skillicons.dev/icons?i=docker,git,github,linux,vscode,aws&perline=8"/>
</p>

---

<h2 align="center">Featured Projects</h2>

### 🛡️ GuardianAI — Multi-Agent Intelligent Surveillance

**Problem:** Real-time threat detection and alerting across surveillance video feeds.

**Solution:** A multi-agent pipeline that fuses OpenCV-based computer vision with LLM-based reasoning to detect, classify, and alert on threats automatically.

| | |
|---|---|
| **Tech Stack** | Python, OpenCV, LangChain, FastAPI |
| **AI Techniques** | Computer Vision, Multi-Agent Reasoning, Object Detection |
| **Links** | [Repository](https://github.com/MaddipatlaChetan24/guardianai-real-time-threat-detection) |

<details>
<summary><b>Architecture Overview</b></summary>

```mermaid
flowchart LR
    A[Video Streams] --> B[OpenCV Detection]
    B --> C[Agent Orchestrator]
    C --> D[LLM Reasoning]
    D --> E[Alerts & Dashboard]
```

</details>

---

### 💬 Medical Chatbot (RAG) — Grounded Medical Assistant

**Problem:** LLMs can hallucinate on medical queries; answers must be grounded in trusted clinical documents.

**Solution:** A retrieval-augmented pipeline that embeds curated medical documents into a vector store and grounds every LLM response in retrieved evidence.

| | |
|---|---|
| **Tech Stack** | LangChain, Vector DB, FastAPI, LLMs |
| **AI Techniques** | Retrieval-Augmented Generation, Embeddings, Semantic Search |
| **Links** | [Repository](https://github.com/MaddipatlaChetan24/Medical-Chatbot-with-LLMs) |

<details>
<summary><b>Architecture Overview</b></summary>

```mermaid
flowchart LR
    A[User Query] --> B[Embedding]
    B --> C[Vector DB Retrieval]
    C --> D[LLM Grounded Answer]
    D --> E[Response]
```

</details>

---

### 🧠 Cache-Augmented Generation (CAG) — Efficient LLM Inference

**Problem:** Repeated LLM inference for similar queries is slow and costly.

**Solution:** Precomputes and reuses key-value caches, eliminating per-query re-processing for repeated contexts — a retrieval-free alternative to RAG.

| | |
|---|---|
| **Tech Stack** | Transformers, PyTorch |
| **AI Techniques** | Key-Value Caching, Inference Optimization |
| **Links** | [Repository](https://github.com/MaddipatlaChetan24/cache-augmented-generation) |

<details>
<summary><b>Architecture Overview</b></summary>

```mermaid
flowchart LR
    A[Documents] --> B[Precompute KV Cache]
    B --> C[Cache Store]
    D[Query] --> E[Cache Retrieval]
    E --> F[LLM Generation]
```

</details>

---

### 🤖 Falcon-7B Fine-Tuning (QLoRA) — Efficient LLM Adaptation

**Problem:** Fine-tuning 7B-parameter LLMs requires expensive GPUs.

**Solution:** Applied QLoRA quantization + LoRA adapters to fine-tune Falcon-7B on consumer hardware, adapting the model to domain tasks without full fine-tuning.

| | |
|---|---|
| **Tech Stack** | Hugging Face, Transformers, QLoRA |
| **AI Techniques** | Parameter-Efficient Fine-Tuning, 4-bit Quantization |
| **Links** | [Repository](https://github.com/MaddipatlaChetan24/falcon-7b-qlora-finetuning) |

<details>
<summary><b>Architecture Overview</b></summary>

```mermaid
flowchart LR
    A[Falcon-7B] --> B[QLoRA Quantization]
    B --> C[LoRA Adapters]
    C --> D[Fine-Tuned Model]
    D --> E[Inference]
```

</details>

---

### ✈️ Navigo AI — Multi-Agent Travel Planner

**Problem:** Travel planning spans search, logistics, and preferences — one model handles it poorly.

**Solution:** Multiple specialized agents (search, itinerary, logistics) orchestrate together to produce complete, coordinated travel plans.

| | |
|---|---|
| **Tech Stack** | Python, LangChain, FastAPI |
| **AI Techniques** | Agentic AI, Multi-Agent Orchestration, Tool Use |
| **Links** | [Repository](https://github.com/MaddipatlaChetan24/Navigo-A-Multi-Agent-Travel-Planner) |

---

### 📖 Neural Language Engine — LSTM Language Modeling

**Problem:** Explore next-word prediction at scale for language modeling.

**Solution:** Trained an LSTM-based recurrent model on large text corpora to predict next words and study sequential language patterns.

| | |
|---|---|
| **Tech Stack** | PyTorch, NLP |
| **AI Techniques** | Recurrent Neural Networks (LSTM), Language Modeling |
| **Links** | [Repository](https://github.com/MaddipatlaChetan24/Neural-Language-Engine) |

---

<h2 align="center">Research Interests</h2>

<p align="center">

<img src="https://img.shields.io/badge/LLM%20Alignment-0E7490?style=for-the-badge"/>
<img src="https://img.shields.io/badge/AI%20Agents-7C3AED?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Efficient%20Fine%20Tuning-F97316?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Multimodal%20AI-0EA5E9?style=for-the-badge"/>
<img src="https://img.shields.io/badge/AI%20Safety-DC2626?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Deep%20Learning%20Optimization-059669?style=for-the-badge"/>

</p>

---

<h2 align="center">Currently Learning</h2>

<p align="center">

<img src="https://img.shields.io/badge/Agentic%20Frameworks%20(LangGraph)-00C2FF?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Model%20Alignment%20(RLHF)-9333EA?style=for-the-badge"/>
<img src="https://img.shields.io/badge/LLM%20Evaluation-059669?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Multimodal%20Systems-0EA5E9?style=for-the-badge"/>
<img src="https://img.shields.io/badge/AI%20Deployment-111827?style=for-the-badge"/>

</p>

---

<h2 align="center">AI Models Worked With</h2>

<p align="center">

<img src="https://img.shields.io/badge/Falcon--7B%20(QLoRA)-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"/>
<img src="https://img.shields.io/badge/OpenAI%20GPT%20API-10A37F?style=for-the-badge&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/Hugging%20Face%20Transformers-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"/>
<img src="https://img.shields.io/badge/Sentence%20Embeddings-336791?style=for-the-badge"/>

</p>

---

<h2 align="center">GitHub Statistics</h2>

<p align="center">

<img height="190" src="https://github-readme-stats.shion.dev/api?username=MaddipatlaChetan24&show_icons=true&theme=github_dark&hide_border=true&count_private=true&include_all_commits=true"/>

<img height="190" src="https://github-readme-stats.shion.dev/api/top-langs/?username=MaddipatlaChetan24&layout=compact&theme=github_dark&hide_border=true"/>

</p>

<p align="center">

<img src="https://streak-stats.demolab.com?user=MaddipatlaChetan24&theme=github-dark&hide_border=true"/>

</p>

---

<h2 align="center">Contribution Activity</h2>

<p align="center">

<img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=MaddipatlaChetan24&theme=github-dark&hide_border=true&area=true"/>

</p>

---

<h2 align="center">Snake Contribution Animation</h2>

<p align="center">

<img width="100%" src="https://raw.githubusercontent.com/MaddipatlaChetan24/MaddipatlaChetan24/output/github-contribution-grid-snake-dark.svg"/>

<sub><i>My contribution history, animated.</i></sub>

</p>

---

<h2 align="center">Connect With Me</h2>

<p align="center">

<a href="mailto:chetan121318@gmail.com">
<img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"/>
</a>

<a href="https://github.com/MaddipatlaChetan24">
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
</a>

<a href="https://www.linkedin.com/in/maddipatla-chetan/">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>

</p>

---

<p align="center">

<img src="https://komarev.com/ghpvc/?username=MaddipatlaChetan24&style=flat-square&color=blue" />

</p>

---

<p align="center">

<i>"Building intelligent systems that solve real-world problems."</i>

</p>

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&section=footer&color=0:0F2027,50:203A43,100:2C5364"/>

</div>
