"""Prep front cover for sidebar (based on st-bumblebee-st_app.py)."""
# pylint: disable=abstract-class-instantiated
import base64
from io import BytesIO
from textwrap import dedent

import logzero
import pandas as pd
import streamlit as st
from logzero import logger
from set_loglevel import set_loglevel

from st_mlbee import __version__

logzero.loglevel(set_loglevel())

msg = dedent(
    """
    What would you like to do?
    The following alignment engines are available.

    **UFast-Engine**: ultra-fast, based on a home-brewed algorithm, faster than blazing fast but can only process en-zh para/sent pairs, not as sophisticated as DL-Engine;

    **SFast-Engine**: super-fast, based on machine translation;

    **Fast-Engine**: based on yet another home-brewed algorithm, blazing fast but can only process en-zh para/sent pairs;

    **DL-Engin**: based on machine learning, multilingual, one para/sent takes about 1s.
    """
).strip()
msg = dedent(
    """
   a multilingual (50+ language pairs) dualtext
    aligner based on machine learning

    It takes about 1-2 s to process a pair of blocks (be it
    sents, paras of docus).
    Extremely long blocks will likely have a negative impact
    on aligning.
    On a powerful computer such as an instance on huggingface spaces, the running time can be reduced by a factor of 10-20.
    """
).strip()


def sb_front_cover():
    """Prep front cover for sidebar."""
    st.sidebar.markdown(f"### mlbee {__version__} ")

    _ = "More info (click to toggle)"
    sb_tit_expander = st.sidebar.expander(_, expanded=False)
    with sb_tit_expander:
        st.markdown(msg)


intructins = dedent(
    f"""
    *   Set up options in the left sidebar

    *   Click expanders / +: to reveal more details; -: to hide them

    *   Press '**Click to start aligning**' to get
    the ball rolling. (The button will appear when
    everything is ready.)

    *   mlbee v.{__version__} from mu@qq41947782's
    keyboard in cyberspace. Join **qq group 316287378**
    for feedback and questions or to be kept updated.
    mlbee is a member of the bee family.
    """
).strip()


def instructions():
    """Prep msg."""
    logger.debug("instructions entry")
    back_cover_expander = st.expander("Instructions")
    with back_cover_expander:
        st.markdown(intructins)

    logger.debug("instructions exit")


about_msg = dedent(
    f"""
    # mlbee {__version__}

    https://bumblebee.freeforums.net/thread/6/mlbee
    or head to 桃花元 （qq group 316287378）
    """
).strip()

menu_items = {
    "Get Help": "https://bumblebee.freeforums.net/thread/6/mlbee",
    "Report a bug": "https://github.com/ffreemt/mlbee/issues",
    "About": about_msg,
}

style_css = """
.row-widget.stTextInput > div:first-of-type {
    background: #fff;
    display: flex;
    border: 1px solid #dfe1e5;
    box-shadow: none;
    border-radius: 24px;
    height: 50px;
    width: auto;
    margin: 10px auto 30px;
}

.row-widget.stTextInput > div:first-of-type:hover,
.row-widget.stTextInput > div:first-of-type:focus {
    box-shadow: 1px 1px 2px 1px rgba(0, 0, 0, 0.2);
}

.row-widget.stTextInput .st-bq {
    background-color: #fff;
}

.row-widget.stTextInput > label {
    color: #b3b3b3;
}

.row-widget.stButton > button {
    border-radius: 24px;
    background-color: #B6C9B1;
    color: #fff;
    border: none;
    padding: 6px 20px;
    float: right;
    background-image: none;
}

.row-widget.stButton > button:hover {
    box-shadow: 1px 1px 2px 1px rgba(0, 0, 0, 0.2);
}

.row-widget.stButton > button:focus {
    border: none;
    color: #fff;
}

.footer-custom {
    position: fixed;
    bottom: 0;
    width: 100%;
    color: var(--text-color);
    max-width: 698px;
    font-size: 14px;
    height: 50px;
    padding: 10px 0;
    z-index: 50;
}

.main {
    padding: 20px;
}

footer {
    display: none !important;
}

.footer-custom a {
    color: var(--text-color);
}

#wikipedia-assistant {
    font-size: 36px;
}

.generated-answer p {
    font-size: 16px;
    font-weight: bold;
}

.react-json-view {
    margin: 40px 0 80px;
}

.tooltip {
    text-align: center;
    line-height: 20px;
    display: table-caption;
    font-size: 10px;
    border-radius: 50%;
    height: 20px;
    width: 20px;
    position: relative;
    cursor: pointer;
    color:#000;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 280px;
    text-align: center;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 1;
    top: 25px;
    left: 50%;
    margin-left: -140px;
    font-size: 14px;
    background-color: #fff;
    border: 1px solid #ccc;
    box-shadow: 0px 0px 3px 1px rgba(0, 0, 0, 0.16);
    color: #000;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
}

.sentence-wrapper {
    border-left: 4px solid #ffc423;
    padding-left: 20px;
    margin-bottom: 40px;
}

#context {
    padding: 2rem 0 1rem;
}

hr {
    margin: 2em 0 1em;
}

.technical-details-info {
    margin-bottom: 100px;
}

.loader-wrapper {
    display: flex;
    align-items: center;
    background-color: rgba(250, 202, 43, 0.2);
    padding: 15px 20px;
    border-radius: 6px;
}

.loader-wrapper p {
    margin-bottom: 0;
    margin-left: 20px;
}

.loader {
    width: 30px;
    height: 30px;
    border: dotted 5px #868686;
    border-radius: 100%;
    animation: spin 1s linear infinite;
}

.loader-note {
    font-size: 14px;
    color: #b3b3b3;
    margin-left: 5px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg) scale(0.8);
    border-top-color: transparent;
    border-right-color: transparent;
  }
  50% { transform: rotate(180deg) scale(1.2);
    border-color: #949494;
    border-top-color: transparent;
    border-right-color: transparent;
  }
  100% { transform: rotate(360deg) scale(0.8);
    border-color: #bbbbbb;
    border-top-color: transparent;
    border-right-color: transparent;
  }
}
"""


def to_excel(df):
    """Convert df to excel.

    ref. st-bumblebee st_app.py
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df):
    """Generates a link.

    Allowing the data in a given panda dataframe
    to be downloaded.

    Args:
        df: pandas.dataframe

    Returns:
        href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="aligned_paras.xlsx">Download aligned paras xlsx file</a>'  # decode b'abc' => abc


def get_table_download_link_sents(df):
    """Generates a link.

    Allowing the data in a given panda dataframe to be
    downloaded for sents aligned.

    Args:
        df: pandas.dataframe

    Returns:
        href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="aligned_sents.xlsx">Download aligned sents xlsx file</a>'  # decode b'abc' => abc  # noqa
