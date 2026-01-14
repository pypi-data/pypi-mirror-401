"""LLM course plugin implementation.

This module provides the plugin implementation for the Large Language Models
course as a standalone package.
"""

import logging
import sys

from master_mind.plugin import ExternalCoursePlugin


class LLMCoursePlugin(ExternalCoursePlugin):
    """Large Language Models course plugin."""

    @property
    def name(self) -> str:
        return "llm"

    @property
    def description(self) -> str:
        return "Large Language Models course"

    @property
    def package_name(self) -> str:
        return "su_master_mind_llm"

    def download_datasets(self) -> None:
        """Download datasets and pre-trained models for the LLM course."""
        try:
            from transformers import (
                AutoTokenizer,
                AutoModelForCausalLM,
                AutoModelForSequenceClassification,
            )
        except ModuleNotFoundError:
            logging.info(
                "transformers n'est pas installe (cela ne devrait pas arriver)"
            )
            sys.exit(1)

        try:
            import datasets  # noqa: F401
        except ModuleNotFoundError:
            logging.info("datasets n'est pas installe (cela ne devrait pas arriver)")
            sys.exit(1)

        try:
            import pyterrier as pt
        except ModuleNotFoundError:
            logging.info("pyterrier n'est pas installe (cela ne devrait pas arriver)")
            sys.exit(1)

        HF_MODELS = [
            # Course 2
            ("TinyLlama/TinyLlama-1.1B-Chat-v1.0", AutoModelForCausalLM),
            ("distilbert-base-uncased", AutoModelForSequenceClassification),
            (
                "distilbert-base-uncased-finetuned-sst-2-english",
                AutoModelForSequenceClassification,
            ),
            # Course 3
            ("Qwen/Qwen2.5-3B-Instruct-AWQ", AutoModelForCausalLM),
            ("Qwen/Qwen2.5-7B-Instruct-AWQ", AutoModelForCausalLM),
            ("HuggingFaceTB/SmolLM2-1.7B-Instruct", AutoModelForCausalLM),
        ]
        for hf_id, base_class in HF_MODELS:
            try:
                logging.info("[LLM] Installing %s", hf_id)
                AutoTokenizer.from_pretrained(hf_id)
                base_class.from_pretrained(hf_id)
            except Exception:
                logging.exception("[LLM] error while installing %s", hf_id)

        # IMDB
        logging.info("[LLM] Downloading IMDB")
        import datasets

        datasets.load_dataset("imdb", split="train")

        # Practicals 4 and 5
        logging.info("[LLM] Downloading ir-datasets 'lotte/technology/dev/search'")
        pt.get_dataset("irds:lotte/technology/dev/search")
