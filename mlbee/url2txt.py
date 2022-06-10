"""Fetch text from url."""
from typing import Optional
from urllib.parse import urlparse

import html2text
import httpx
import streamlit as st
from logzero import logger
from readability import Document


# @st.cache
def url2txt(
    url: str,
    bodywidth: Optional[int] = 5000,
    remove: bool = False,
    show_url: bool = True,
    ignore_links: bool = True,
) -> str:
    """Fetch text from url.

    Args:
        url: netloc from which to fetch text
        bodywidth: if set to None, fall back to default bodywidth of
            html2text.HTML2Text
        remove: remove blank lines if set to True
        show_url: prepend url if set to True
        ignore_links: remove [ur](url)

    Return:
        main body in text

    bodywidth: Optional[int] = 5000
    remove: bool = False
    show_url: bool = True
    ignore_links: bool = True
    """
    url = url.strip()
    if not url.startswith("http"):
        url = "http://" + url

    logger.info("url: %s", url)

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:  # no scheme or netloc present
        raise Exception(f"Invalid url: {url}")

    try:
        resp = httpx.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        logger.error(exc)
        raise

    try:
        content_type = resp.headers["content-type"]
    except Exception as e:
        logger.error(e)
        content_type = ""
    # output text if text/plain
    if "text/plain" in content_type:
        return resp.text

    # handle html and the rest
    try:
        doc = Document(resp.text)
    except Exception as exc:
        logger.error(exc)
        raise

    if not doc.summary().strip():
        raise Exception("No content for some reason...")

    if bodywidth is not None:
        handle = html2text.HTML2Text(bodywidth=bodywidth)
    else:
        handle = html2text.HTML2Text()

    handle.ignore_links = ignore_links

    try:
        res = handle.handle(doc.summary())
    except Exception as exc:
        logger.error(exc)
        raise

    # remove double blank lines
    if remove:
        res = "\n".join(elm for elm in res.splitlines() if elm.strip())

    if not res.strip():  # warn if empty output
        logger.warning("Output seems to be empty...")

    if show_url:
        return f"{url}\n# {doc.title()}\n{res}"

    return f"# {doc.title()}\n{res}"
