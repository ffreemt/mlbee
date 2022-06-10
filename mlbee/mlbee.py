"""Define mlbee."""
# pylint: disable=invalid-name
from typing import List

from cmat2aset import cmat2aset
from logzero import logger

from mlbee.gen_cmat import gen_cmat


def mlbee(
    text1: List[str],
    text2: List[str],
    eps: float = 10,
    min_samples: int = 6,
    # show_plot: bool = True,
):
    """Align multilingual texts.

    Args:
        text1: list of strings
        text2: list of strings
        eps: epsilon
        min_samples: minimum number of points to be considered as a cluster
        x show_plot: whether to show plots, refactored to cmat2html's show_plot
    Returns:
        Aligned text pairs.
    """
    if not (
        [elm for elm in text1 if elm.strip()] and [elm for elm in text2 if elm.strip()]
    ):
        logger.warning("One or both inputs are empty")
        raise Exception("Nothing to do...exiting")

    try:
        # from json_de2zh.gen_cmat import gen_cmat  # noqa  # pylint: disable=import-outside-toplevel
        cmat = gen_cmat(text1, text2)
        # logger.level is reset to 20 in fastlid
        mlbee.cmat = cmat
    except Exception as e:
        logger.exception(e)
        raise

    try:
        # aset = cmat2aset(cmat.T)
        aset = cmat2aset(cmat, eps=eps, min_samples=min_samples)
        mlbee.aset = aset
    except Exception as e:
        logger.exception(e)
        raise

    # paired texts or aset?
    return aset
