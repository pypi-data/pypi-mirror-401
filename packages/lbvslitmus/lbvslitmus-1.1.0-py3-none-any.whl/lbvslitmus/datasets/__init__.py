"""Dataset downloading and management submodule for Litmus.

This submodule provides functionality for downloading and managing datasets
used in virtual screening experiments. All datasets are downloaded from
HuggingFace Hub where they are preprocessed and ready to use.
"""

from lbvslitmus.datasets.dekois import DekoisDownloader
from lbvslitmus.datasets.downloader import DatasetDownloader
from lbvslitmus.datasets.dudad import DUDADDownloader
from lbvslitmus.datasets.dude import DUDEDownloader
from lbvslitmus.datasets.lit_pcba import LITPCBADownloader
from lbvslitmus.datasets.muv import MUVDownloader
from lbvslitmus.datasets.registry import DatasetRegistry
from lbvslitmus.datasets.welqrate import WelQrateDownloader

__all__ = [
    "DUDADDownloader",
    "DUDEDownloader",
    "DatasetDownloader",
    "DatasetRegistry",
    "DekoisDownloader",
    "LITPCBADownloader",
    "MUVDownloader",
    "WelQrateDownloader",
]
