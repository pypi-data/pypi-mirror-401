#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Deep Learning Context - TensorBoard / Jupyter / Visualizers
"""

DETAILS = {
    "title": "XSS in Machine Learning Visualizers",
    "severity": "high",
    "cvss_score": 8.0,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N",
    "cwe": ["CWE-79"],
    "owasp": ["A03:2021"],
    "description": (
        "Cross-Site Scripting in ML experimentation platforms like TensorBoard, "
        "MLflow, or Jupyter Notebooks. These tools often render rich media "
        "(histograms, text summaries, image captions) from training logs. "
        "If logs are tainted (poisoned dataset), the visualizer executes the payload."
    ),
    "attack_vector": (
        "Attacker poisons a public dataset or model checkpoint. When a data scientist "
        "loads this data and visualizes it (e.g., viewing misclassified examples in TensorBoard), "
        "the malicious label or text summary executes XSS, potentially stealing API keys "
        "or accessing the Jupyter kernel."
    ),
    "remediation": (
        "Sanitize all string data logged to experiment trackers. "
        "Run visualization dashboards in isolated sandboxes. "
        "Disable HTML rendering in log viewers by default."
    ),
    "references": [
        "https://github.com/tensorflow/tensorboard/security/advisories",
        "https://huntr.dev/bounties/tensorboard-xss/",
    ],
    "tags": ["ai", "ml", "tensorboard", "jupyter", "visualization", "dataset-poisoning"],
    "reliability": "medium",
}
