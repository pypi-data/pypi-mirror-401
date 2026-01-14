"""Built-in course plugin implementations.

This module defines the plugin implementations for courses that are
built into the su_master_mind package (using extras).
"""

import logging
import shutil
import sys
from typing import Optional
import click

from .plugin import BuiltinCoursePlugin


class DeeplCoursePlugin(BuiltinCoursePlugin):
    """Deep Learning course plugin."""

    @property
    def name(self) -> str:
        return "deepl"

    @property
    def description(self) -> str:
        return "Deep Learning course"

    def download_datasets(self) -> None:
        pass


class RLCoursePlugin(BuiltinCoursePlugin):
    """Reinforcement Learning course plugin."""

    @property
    def name(self) -> str:
        return "rl"

    @property
    def description(self) -> str:
        return "Reinforcement Learning course"

    def get_cli_group(self) -> Optional[click.Group]:
        """Return the RL-specific CLI command group."""
        from .cli.rl import rl_group

        return rl_group

    def pre_install_check(self) -> bool:
        """Check that swig is installed."""
        if sys.platform == "win32":
            has_swig = shutil.which("swig.exe")
        else:
            has_swig = shutil.which("swig")

        if not has_swig:
            logging.error(
                "swig n'est pas installé: sous linux utilisez le "
                "gestionnaire de paquets:\n - sous windows/conda : "
                "conda install swig\n - sous ubuntu: sudo apt install swig"
            )
            return False
        return True


class ADLCoursePlugin(BuiltinCoursePlugin):
    """Advanced Deep Learning course plugin."""

    @property
    def name(self) -> str:
        return "adl"

    @property
    def description(self) -> str:
        return "Advanced Deep Learning course"

    def download_datasets(self) -> None:
        pass


class RitalCoursePlugin(BuiltinCoursePlugin):
    """Information Retrieval course plugin."""

    @property
    def name(self) -> str:
        return "rital"

    @property
    def description(self) -> str:
        return "Information Retrieval course"

    def download_datasets(self) -> None:
        try:
            from datamaestro import prepare_dataset
        except ModuleNotFoundError:
            logging.info("Datamaestro n'est pas installé (cela ne devrait pas arriver)")
            sys.exit(1)

        for dataset_id in [
            "com.github.aagohary.canard",
            "irds.antique.train",
            "irds.antique.test",
        ]:
            logging.info("Preparing %s", dataset_id)
            prepare_dataset(dataset_id)

        try:
            from transformers import AutoTokenizer, AutoModelForMaskedLM
        except ModuleNotFoundError:
            logging.info(
                "transformers n'est pas installé (cela ne devrait pas arriver)"
            )
            sys.exit(1)

        for hf_id in [
            "Luyu/co-condenser-marco",
            "huawei-noah/TinyBERT_General_4L_312D",
        ]:
            AutoTokenizer.from_pretrained(hf_id)
            AutoModelForMaskedLM.from_pretrained(hf_id)
