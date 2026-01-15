# HF Inference Benchmark

[![CI Pipeline](https://github.com/rgb-99/hf-inference-benchmark/actions/workflows/ci.yml/badge.svg)](https://github.com/rgb-99/hf-inference-benchmark/actions)
[![PyPI](https://img.shields.io/pypi/v/hf-inference-benchmark?color=orange)](https://pypi.org/project/hf-inference-benchmark/)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![License](https://img.shields.io/badge/license-MIT-green)

> Production-grade benchmarking infrastructure for HuggingFace inference workloads.

`hf-inference-benchmark` is a **reproducible, device-agnostic benchmarking system** that measures the real operational cost of running LLMs — latency, throughput, and memory — under production-like conditions.

It answers one critical question:

> **“Will this model crash my server — and how fast can it actually run?”**

---

## Why This Tool Exists

Most public HuggingFace benchmarking scripts:

• Measure only a single forward pass  
• Ignore warmup behavior  
• Ignore GPU synchronization  
• Ignore memory allocator behavior  
• Produce misleading results  

This tool implements the **same benchmarking discipline used by real ML infrastructure teams.**

---

## Benchmarking Pipeline

```
Model Load
   ↓
Warmup Passes
   ↓
Synchronized Execution
   ↓
Latency Profiling (P50 / P95 / Avg)
   ↓
Token Counting
   ↓
Throughput Calculation (tokens/sec)
   ↓
Peak Memory Tracking
   ↓
Structured JSON Export
```

---

## Metric Definitions

| Metric | Meaning |
|-------|--------|
| latency_p50 | Median inference latency |
| throughput | Real generation speed in tokens/sec |
| memory_mb | Peak RAM/VRAM usage |
| warmup | Kernel stabilization |
| synchronization | Accurate GPU timing |

---

## User Installation

```bash
# From PyPI
pip install hf-inference-benchmark

# From Source (for Developers)
git clone https://github.com/rgb-99/hf-inference-benchmark.git
cd hf-inference-benchmark
pip install -e .
```

---

## Basic Usage

```bash
# Run on CPU/GPU (Auto-detected)
hf-bench facebook/opt-125m

# Export results for the Reporting Suite
hf-bench gpt2 --tokens 64 --out results/gpt2_perf.json
```

---

## Persisting Results 

```bash
hf-bench facebook/opt-125m --tokens 64 --out results/opt125m.json
```

Example:

```json
{
  "model": "facebook/opt-125m",
  "throughput": 54.36,
  "latency_p50": 878.83,
  "memory_mb": 797.56
}
```

---

## Reproducible Benchmarking

For fair comparison:

• Fix prompt  
• Fix token count  
• Fix device  
• Use warmup runs  
• Compare structured JSON outputs  

---

## Platform Integration

This tool is part of the unified NLP infrastructure platform:

```bash
nlp-tool benchmark facebook/opt-125m
nlp-tool report results/opt125m.json
```

---

## Roadmap

• Batch-size profiling  
• Streaming generation benchmarks  
• Multi-GPU scaling  
• Energy-cost estimation  
• CI-based regression tracking  

---
