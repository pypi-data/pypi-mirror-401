<div align="center">

# 📦 `ibm-watsonx-ai`
### Official IBM watsonx.ai Python SDK

![IBM](https://img.shields.io/badge/IBM-watsonx.ai-0F62FE?style=for-the-badge&logo=ibm&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11%20–%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-BSD--3--Clause-6A737D?style=for-the-badge)

[![PyPI](https://img.shields.io/pypi/v/ibm-watsonx-ai.svg?style=flat-square)](https://pypi.org/project/ibm-watsonx-ai/)
[![Downloads](https://img.shields.io/pypi/dm/ibm-watsonx-ai.svg?style=flat-square)](https://pypistats.org/packages/ibm-watsonx-ai)
[![Docs](https://img.shields.io/badge/docs-Documentation-0F62FE?style=flat-square)](https://ibm.github.io/watsonx-ai-python-sdk/)
[![Examples](https://img.shields.io/badge/examples-Jupyter%20Notebooks-10B981?style=flat-square)](https://github.com/IBM/watsonx-ai-samples)

---

**Enterprise-grade Python client for building, tuning and deploying AI models with IBM watsonx.ai**

[🚀 Quick Start](#-quick-start) •
[📘 Documentation](https://ibm.github.io/watsonx-ai-python-sdk/) •
[📓 Examples](https://github.com/IBM/watsonx-ai-samples)

</div>

## 📌 Overview

`ibm-watsonx-ai` is the **official Python SDK for IBM watsonx.ai**, an enterprise-grade AI platform for building, training, tuning, deploying, and operating AI models at scale.

The SDK provides a unified and production-ready Python interface to the full **watsonx.ai ecosystem**, including Foundation Models (within LLMs), AutoAI experiments, Retrieval-Augmented Generation (RAG), model tuning, deployment, and data integration.

With `ibm-watsonx-ai`, developers and data scientists can seamlessly integrate advanced AI capabilities into Python applications running on **IBM watsonx.ai for IBM Cloud** or **IBM watsonx.ai software**, while meeting enterprise requirements such as security, governance, and scalability.

---

## 🎯 What This SDK Is Used For

The `ibm-watsonx-ai` SDK is designed to support the **entire AI lifecycle**:

* 🔐 Secure authentication and environment configuration
* 🤖 Inference with Foundation Models (LLMs, embeddings, time-series, audio)
* 📚 Building Retrieval-Augmented Generation (RAG) systems
* 🧪 Running and optimizing AutoAI experiments
* ⚙️ Fine-tuning and prompt tuning of models
* 🚀 Deploying models to scalable inference endpoints
* 🔗 Integrating enterprise data sources into AI workflows

It is suitable for **research, prototyping, and production deployments**.

---

## 📦 Installation

Install from **PyPI**:

```bash
pip install ibm-watsonx-ai
```

Install with optional extras:

```bash
pip install "ibm-watsonx-ai[rag]"
```

| Extra | Description                              |
|-------|------------------------------------------|
| `rag` | Retrieval‑Augmented Generation utilities |
| `mcp` | Model Context Protocol                   |

---

## 🚀 Quick Start

### Authentication

```python
from ibm_watsonx_ai import Credentials, APIClient

credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    api_key="<your-ibm-api-key>"
)

client = APIClient(credentials, space_id="<your-space-id>")
```
