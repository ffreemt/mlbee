"""Fetch text from urls and convert to state.ns.list1/list2."""
# pylint: disable=invalid-name
import streamlit as st
from icecream import ic
from logzero import logger
from streamlit import session_state as state

from mlbee.url2txt import url2txt

ic.configureOutput(
    includeContext=True,
    outputFunction=logger.debug,  # outputFunction=logger.info,
)


def fetch_urls():
    """Fetch text from urls and convert to state.ns.list1/list2."""
    beetype = state.ns.beetype
    sourcecount = state.ns.sourcecount
    value = ""
    if beetype == "ezbee" or beetype == "mlbee":
        url1 = (
            "https://raw.githubusercontent.com/ffreemt/en-de-zh-txt/master/test_en.txt"
        )
        url2 = (
            "https://raw.githubusercontent.com/ffreemt/en-de-zh-txt/master/test_zh.txt"
        )
        value = f"{url1} {url2}"
    if beetype == "dzbee":
        url1 = "https://raw.githubusercontent.com/ffreemt/en-de-zh-txt/master/sternstunden04-de.txt"
        url2 = "https://raw.githubusercontent.com/ffreemt/en-de-zh-txt/master/sternstunden04-zh.txt"
        value = f"{url1} {url2}"
    if beetype == "debee":
        url1 = "https://raw.githubusercontent.com/ffreemt/en-de-zh-txt/master/sternstunden04-de.txt"
        url2 = "https://raw.githubusercontent.com/ffreemt/en-de-zh-txt/master/sternstunden04-en.txt"
        value = f"{url1} {url2}"

    dict_ = dict(text1="", text2="")

    def fetch_cb():
        """Fetch text (dict_["text1"|"text2"]) from urls."""
        ic("fetch_cb")
        urls = [elm.strip() for elm in text_inp.split(" ") if elm.strip()]

        # supply http:// if not startswith http
        urls = [elm if elm.startswith("http") else "http://" + elm for elm in urls]

        _ = "\n\t"
        # st.markdown(f" urls submitted: \n{_.join(urls)}")
        ic(f" urls submitted: \n{_.join(urls)}")

        # st.write(" TODO: fetch text from urls.")

        if state.ns.sourcecount == 2:  # 2-sep
            for idx, url in enumerate(urls[:2]):
                try:
                    _ = url2txt(url)
                except Exception as e:
                    logger.error(e)
                    _ = str(e)
                dict_[f"text{idx + 1}"] = _
                ic(f"{idx + 1}: [{url}] {dict_['text' + str(idx + 1)][:100]}")

            ic(dict_["text1"][:10])
            ic(dict_["text2"][:10])
        else:  # 1-mix
            text1 = ""
            for url in urls:
                try:
                    _ = url2txt(url)
                except Exception as e:
                    logger.error(e)
                    _ = str(e)
                text1 += _
            ic(text1[:10])
            dict_["text1"] = text1[:]

        _ = [elm.strip() for elm in dict_["text1"].splitlines() if elm.strip()]
        state.ns.list1 = _
        _ = [elm.strip() for elm in dict_["text2"].splitlines() if elm.strip()]
        state.ns.list2 = _

        list1 = state.ns.list1
        list2 = state.ns.list2
        ic(len(list1), len(list2))

        state.fetched_text1 = dict_["text1"]
        state.fetched_text2 = dict_["text2"]

        # streamlit complains if an initial value of
        # a widget with this key is set
        # state.text_area_urls = text_inp

    # with st.form(key="urls_in_form"):
    # _ = st.expander(f"{beetype}: Paste urls below and press Ctl+Enter or Space Ctl+Enter to testdrive", expanded=True)
    # with _:
    label = f"{beetype}: Paste urls below and press Ctl+Enter or Space Ctl+Enter to testdrive"
    text_inp = st.text_area(
        label=label,
        value=value,
        key="text_area_urls",
        height=25,
        help=" URLs separated by at least a space or a newline（贴网址，空格分开或另起一行, Ctrl+回车提交）",
        on_change=fetch_cb,
        # args=(text_inp,),
    )

    # st.button("Fetch", on_click=fetch_cb, args=(text_inp,))

    def text2lists():
        """Convert text(s) to list(s)."""
        if text1:
            try:
                list1 = [elm.strip() for elm in text1.splitlines() if elm.strip()]
                state.ns.list1 = list1[:]
            except Exception as e:
                logger.warning("text1 to list1 errors: %s", e)

        if text2:
            try:
                list2 = [elm.strip() for elm in text2.splitlines() if elm.strip()]
                state.ns.list2 = list2[:]
            except Exception as e:
                logger.warning("text2 to list2 errors: %s", e)

    # show fetch text(s)
    text1 = dict_["text1"]
    text2 = dict_["text2"]
    if state.ns.sourcecount == 2:  # 2-sep
        with st.form(key="fetched_2texts_in_form"):
            _ = st.expander(f"{state.ns.beetype}: fetched text", expanded=True)
            with _:
                col1, col2 = st.columns(2)
                with col1:
                    text1 = st.text_area(
                        label="Edit when necessary, click Submit when ready",
                        key="fetched_text1",
                        # help=""
                        height=500,
                        value=text1,
                    )

                with col2:
                    text2 = st.text_area(
                        label="Edit when necessary, click Submit when ready",
                        # help=""
                        key="fetched_text2",
                        height=500,
                        value=text2,
                    )

            submitted = st.form_submit_button("Submit", on_click=text2lists)

    else:  # 1-mix
        with st.form(key="fetched_1_text_in_form"):
            _ = st.expander(f"{state.ns.beetype}: fetched mixed text", expanded=True)
            with _:
                text1 = st.text_area(
                    label="Edit when necessary, click Submit when ready",
                    key="fetched_mixed_text1",
                    height=500,
                    value=text1,
                )
            submitted = st.form_submit_button("Submit", on_click=text2lists)

    # _ = """
    if not submitted:
        ic("Submit not yet clicked")
        return
    # """

    state.ns.src_filename = ""
    state.ns.updated = True
