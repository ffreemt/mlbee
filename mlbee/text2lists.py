"""Separate text to zh en lists."""
# pylint: disable=unused-import, too-many-locals, invalid-name, too-many-branches, too-many-statements,

# from typing import Tuple,
from typing import Iterable, List, Optional, Tuple, Union  # noqa

import numpy as np
from logzero import logger

# from fastlid import fastlid
from polyglot.text import Detector

# from dzbee.detect import detect
from debee.detect import detect

# from json_de2zh.gen_cmat import gen_cmat
from debee.gen_cmat import gen_cmat

# from radiobee.lists2cmat import lists2cmat  # use fast_scores
# from radiobee.detect import detect
# from fast_scores.gen_cmat import gen_cmat  # pylint: disable=import-error


def text2lists(
    text: Union[Iterable[str], str],
    set_languages: Optional[List[str]] = None,
) -> Tuple[List[str], List[str]]:
    """Separate text to zh en lists.

    Args:
        text: mixed text
        set_languages: no default (open-end)
            use polyglot.text.Detector to pick two languages

    Attributes:
        cmat: correlation matrix (len(list_l) x len(list_r))
            before adjusting (shifting)
        offset: plus, [""] * offset + list2
                minus, [""] * (-offset) + list1
    Returns:
        two lists, best effort alignment
    """
    if not isinstance(text, str) and isinstance(text, Iterable):
        try:
            text = "\n".join(text)
        except Exception as e:
            logger.error(e)
            raise

    # set_languages default to ["en", "zh"]
    if set_languages is None:
        lang12 = [elm.code for elm in Detector(text).languages]

        # set_languages = ["en", "zh"]

        # set 'un' to 'en'
        # set_languages = ['en' if elm in ['un'] else elm for elm in lang12[:2]]
        set_languages = []
        for elm in lang12[:2]:
            if elm in ["un"]:
                logger.warning(" Unknown language, set to en")
                set_languages.append("en")
            else:
                set_languages.append(elm)

    # fastlid.set_languages = set_languages

    list1 = []
    list2 = []

    # lang0, _ = fastlid(text[:15000])
    lang0 = detect(text, set_languages)

    res = []
    left = True  # start with left list1

    for elm in [_ for _ in text.splitlines() if _.strip()]:
        # lang, _ = fastlid(elm)
        try:
            lang = detect(elm, set_languages)
        except Exception:
            lang = "en"
            logger.warning("Cant detect: %s[20]...setting to %s", elm[:20], lang)

        if lang == lang0:
            res.append(elm)
        else:
            if left:
                # list1.append("\n".join(res))
                list1.extend(res)
            else:
                # list2.append("\n".join(res))
                list2.extend(res)
            left = not left

            res = [elm]
            lang0 = lang

    # process the last
    if left:
        list1.extend(res)
    else:
        list2.extend(res)

    try:
        # lang1, _ = fastlid(' '.join(list1))
        lang1 = detect(" ".join(list1), set_languages)
    except Exception as exc:
        logger.error(exc)
        lang1 = "en"
    try:
        # lang2, _ = fastlid(' '.join(list2))
        lang2 = detect(" ".join(list2), set_languages)
    except Exception as exc:
        logger.error(exc)
        lang2 = "en"

    # find offset via diagonal(k),
    len1, len2 = len(list1), len(list2)

    # ylim, xlim = cmat.shape
    ylim, xlim = len2, len1  # check

    # cmat dim: len1 x len2 or ylim x xlim
    # cmat = lists2cmat(list1, list2, lang1, lang2)
    # cmat.shape: len(list1)xlen(list2) or ylim x xlim
    cmat = gen_cmat(list1, list2)

    # sq_mean_pair = [(elm, np.square(cmat.diagonal(elm)).mean()) for elm in range(2 - ylim, xlim + 1)]
    # df = pd.DataFrame(sq_mean_pair, columns=['offset', 'sq_mean'])
    # df.plot.scatter('offset', 'sq_mean')
    # optimum_offset = df.offset[df.sq_mean.argmax()]

    # equiv to np.argmax(sq_mean) - (ylim - 2)
    # locate max, -ylim + 2 ...xlim: range(1 - ylim, xlim)
    # sqare sum

    sq_mean = [
        np.square(cmat.diagonal(elm)).mean() for elm in range(1 - ylim, xlim - 1)
    ]
    # tot: xlim + ylim - 1

    # temp = [np.square(cmat.diagonal(elm)) for elm in range(2 - ylim, xlim + 1)]
    # sq_mean = [elm.mean() if np.any(elm) else 0.0 for elm in temp]

    # plt.figure()
    # plt.scatter(range(1 - ylim, xlim), sq_mean)

    offset = np.argmax(sq_mean) - (ylim - 1)

    text2lists.cmat = cmat
    text2lists.offset = offset
    text2lists.lang1 = lang1
    text2lists.lang2 = lang2

    # shift list1 if offsset >= 0, else shift list2
    if offset > -1:
        # list1a = list1[:]
        # list2a = [""] * offset + list2
        list2 = [""] * offset + list2
    else:
        list1 = [""] * (-offset) + list1
        # list1a = [""] * (-offset) + list1
        # list2a = list2[:]

    # return list1, list2
    return [elm.strip() for elm in list1], [elm.strip() for elm in list2]
