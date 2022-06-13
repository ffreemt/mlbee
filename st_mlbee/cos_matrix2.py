"""Compute the cosine similarity matrix of A.

https://stackoverflow.com/questions/17627219/whats-the-fastest-way-in-python-to-calculate-cosine-similarity-given-sparse-mat
"""
from typing import Optional
import numpy as np


def cos_matrix2(mat1: np.ndarray, mat2: Optional[np.ndarray] = None) -> np.ndarray:
    """Compute the cosine similarity matrix of mat1, mat2: mat1 * mat2.T.

    Args:
        mat1: np.asarray
        mat2: [Optional], if not present mat2 = mat1
    Returns
        cosine similarity
    """
    if not isinstance(mat1, np.ndarray):
        mat1 = np.asarray(mat1, dtype=np.float32)

    if mat2 is None:
        mat2 = mat1.copy()

    if not isinstance(mat2, np.ndarray):
        mat2 = np.asarray(mat2, dtype=np.float32)

    if mat1.shape[1] != mat2.shape[1]:
        print("shape mismatch: %s, %s", mat1.shape, mat2.shape)
        raise SystemError(1)
    cosine = np.dot(mat1, mat2.T)

    norm1 = np.linalg.norm(mat1, axis=1)
    norm2 = np.linalg.norm(mat2, axis=1)

    # if not (norm1 and norm2): return 0

    size1 = norm1.size
    size2 = norm2.size
    norm_mat = np.dot(norm1.reshape(size1, 1), norm2.reshape(1, size2))

    for idx in range(size1):
        for jdx in range(size2):
            if norm_mat[idx, jdx] == 0:
                cosine[idx, jdx] = 0.0
            else:
                cosine[idx, jdx] = cosine[idx, jdx] / norm_mat[idx, jdx]
    return cosine
