"""Gen cmat for de/en text."""
# pylint: disable=invalid-name, too-many-branches

from typing import List, Optional

import more_itertools as mit
import numpy as np

from tqdm import tqdm
from model_pool import load_model_s
from logzero import logger

from mlbee.cos_matrix2 import cos_matrix2

try:
    model_s = load_model_s()
except Exception as _:
    logger.exception(_)
    raise


def gen_cmat(
    text1: List[str],
    text2: List[str],
    bsize: int = 50
) -> np.ndarray:
    """Gen corr matrix for texts.

    Args:
        text1: typically '''...''' splitlines()
        text2: typically '''...''' splitlines()
        bsize: batch size, default 50
    text1 = 'this is a test'
    text2 = 'another test'
    """
    bsize = int(bsize)
    if bsize <= 0:
        bsize = 50

    if isinstance(text1, str):
        text1 = [text1]
    if isinstance(text2, str):
        text1 = [text2]

    vec1 = []
    vec2 = []
    len1 = len(text1)
    len2 = len(text2)
    tot = len1 // bsize + bool(len1 % bsize)
    tot += len2 // bsize + bool(len2 % bsize)
    with tqdm(total=tot) as pbar:
        for chunk in mit.chunked(text1, bsize):
            try:
                vec = model_s.encode(chunk)
            except Exception as exc:
                logger.error(exc)
                raise
            vec1.extend(vec)
            pbar.update()
        for chunk in mit.chunked(text2, bsize):
            try:
                vec = model_s.encode(chunk)
            except Exception as exc:
                logger.error(exc)
                raise
            vec2.extend(vec)
            pbar.update()
    try:
        # note the order vec2, vec1
        _ = cos_matrix2(np.array(vec2), np.array(vec1))
    except Exception as exc:
        logger.exception(exc)
        raise

    return _
