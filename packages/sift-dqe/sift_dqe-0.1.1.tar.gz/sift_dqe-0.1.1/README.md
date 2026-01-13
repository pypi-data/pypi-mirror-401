# Sift: Adaptive Data Quality Engine (DQE)

**Sift** is a deterministic, explainable engine designed to detect, rank, and suggest fixes for data quality issues in tabular datasets.

Unlike "black box" AI tools that hallucinate fixes, Sift uses a transparent **3-Layer Architecture** to provide statistically backed remediation strategies without requiring labeled training data.

### 🚀 Key Capabilities

* **Layer 1: Structural Profiling** - Infers types, cardinality, and missingness patterns using **Polars**.
* **Layer 2: Semantic Inference** - Uses **Isolation Forest** (Anomaly Detection) and **String Clustering** to find logic errors and fuzzy duplicates.
* **Layer 3: Impact Ranking** - Prioritizes issues by severity (0-1 score) so you fix system-breaking errors first.

---

## 📦 Installation

```bash
pip install sift-dqe

```

---

## ⚡ Quick Start

Sift installs a global CLI tool that you can use immediately.

### 1. Run the Demo

See Sift in action against an internally generated dataset. The engine will spin up, inject random errors (via Chaos Monkey), and attempt to detect them live.

```bash
sift demo

```

### 2. Verify Reliability (The Benchmark)

Don't trust the tool? Audit it. Run the **Reliability Scorecard** to stress-test the engine against 20 cycles of synthetic data corruption.

```bash
sift benchmark

```

### 3. Analyze Your Own Data

Sift supports CSV and Parquet files out of the box.

```bash
sift analyze path/to/your/file.csv

```

---

## 🧠 How It Works

Sift operates on the **Bounded Intelligence** principle—it avoids guessing semantics and instead measures statistical deviation.

1. **Ingest:** Loads data into Polars for high-performance processing.
2. **Profile:** Calculates column statistics (Mode, Mean, Null%).
3. **Infer:** Runs unsupervised ML (Isolation Forest) to detect row-level anomalies.
4. **Rank:** Synthesizes all findings into a prioritized JSON report or Terminal Dashboard.

---

## 🛡️ Known Limitations

Sift is a statistical engine, not a semantic oracle.

* **Small Data:** Datasets with <50 rows may trigger false positives in anomaly detection due to sparse density.
* **Context:** Sift detects *outliers* (e.g., Age=150), but cannot verify if they are *impossible* (e.g., humans don't live to 150).

For a full list of failure modes, please visit the [GitHub Repository](https://github.com/PranavKndpl/Sift).

