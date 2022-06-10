"""Test gen_cmat.

king
In [21]: len(de)
Out[21]: 51

In [22]: len(en)
Out[22]: 51

In [23]: len(" ".join(en))
Out[23]: 11208

In [24]: len(" ".join(de))
Out[24]: 13532

In [25]: %time en_vec = model_s.encode(en)
CPU times: user 22 s, sys: 436 ms, total: 22.4 s
Wall time: 22.4 s

In [26]: %time de_vec = model_s.encode(de)
CPU times: user 22.8 s, sys: 311 ms, total: 23.1 s
Wall time: 23.1 s

en1 = loadparas("data/sternstunden04-en.txt")
en2 = loadparas("data/sternstunden04-de.txt")

len(en1)  # 30

len(" ".join(en1))  # 29718
len(" ".join(en2))  # 31478
"""
from cmat2aset import cmat2aset
from aset2pairs import aset2pairs
from mlbee.gen_cmat import gen_cmat
from mlbee.loadtext import loadparas

paras1 = loadparas("data/sternstunden04-en.txt")
paras2 = loadparas("data/sternstunden04-de.txt")
cmat = gen_cmat(paras1, paras2)


def test_gen_cmat_sternstunden04():
    """Test gen_cmat sternstunden04."""
    len1, len2 = len(paras1), len(paras2)

    # note the order
    assert cmat.shape == (len2, len1)


def test_aset2pairs():
    """Test aset2pairs."""
    aset = cmat2aset(cmat)
    pairs = aset2pairs(paras1, paras2, aset)

    assert "Marseillaise" in pairs[2][0]
    assert "Marseillaise" in pairs[2][1]
    assert pairs[2][2] > 0.95
