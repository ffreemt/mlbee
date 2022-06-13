"""Map cell background color for pandas.DataFrame.

palette = sns.blend_palette(
    # ["pink", "palegreen", 'green'], N_COLORS).as_hex()
    # ["pink", "palegreen"], N_COLORS).as_hex()
    ["red", "palegreen"], N_COLORS).as_hex()
Refer to color_table_applymap.py

Taken from vizbee color_map
"""
# pylint: disable=invalid-name, broad-except
palette = [
    # "#f00000",
    # "#f02315",
    "#e2482c",
    "#d36b41",
    "#c49057",
    "#b5b36c",
    "#a7d883",
    "#98fb98",
]
ncolors = len(palette)


def color_map(v, min_: float = 0, max_: float = 1):
    """Map cell background color.

    e.g. s_df = df.style.applymap(color_map, min_=min_, max_=max_, subset=["B"])
    or s_df = df.style.applymap(color_map, subset=['likelihood'])

    or
    s_df = df.style.applymap(color_map, subset=[2,])

    or
    s_df = df.style.applymap(color_map, subset=[df.columns[2])

    or
    s_df = df.style.applymap(color_map, subset=[*df.columns[1:3]] + [*df.columns[0:1]])
    """
    wd = (max_ - min_) / ncolors
    try:
        v = float(v)  # !!!
        pal = palette[min(ncolors - 1, int((v - min_) / wd))]
    except Exception:  # as e:  # wont style str etc.
        # logger.debug("%s", e)
        # return None
        return "wrap_text: true"

    return f"background-color: {pal}"
