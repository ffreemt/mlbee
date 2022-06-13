"""Fetch upload and convert to list1/list2."""
import streamlit as st
from logzero import logger
from streamlit import session_state as state


def fetch_upload():
    """Fetch upload and convert to list1/list2."""
    src_fileio = b""
    tgt_fileio = b""
    with st.form(key="upload_in_form"):
        _ = st.expander(f"{state.ns.beetype}: Pick two files", expanded=True)
        with _:
            col1, col2 = st.columns(2)
            with col1:
                src_fileio = st.file_uploader(
                    "Choose source file (utf8 txt)",
                    type=[
                        "txt",
                    ],
                    key="src_text",
                    # accept_multiple_files=True,
                    # accept_multiple_files=False,
                )

            with col2:
                tgt_fileio = st.file_uploader(
                    "Choose target file (utf8 txt)",
                    type=[
                        "txt",
                    ],
                    key="tgt_text",
                    # accept_multiple_files=True,
                )
        submitted = st.form_submit_button("Submit")

    # logger.debug(" len(src_fileio): %s", len(src_fileio))
    # logger.debug(" len(tgt_fileio): %s", len(tgt_fileio))

    filename1 = ""
    if src_fileio:
        logger.debug(" type(src_fileio): %s", type(src_fileio))

        # for st.file_uploade accept_multiple_files=True
        if isinstance(src_fileio, list):
            logger.debug(" len(src_fileio): %s", len(src_fileio))
            filenames = []
            try:
                filenames = [elm.name for elm in src_fileio]  # type: ignore
            except Exception as exc:
                logger.error(exc)
            logger.debug("src_fileio  names: *%s*", filenames)

            # state.ns.src_fileio = src_fileio
            state.ns.src_file = src_fileio[-1].getvalue().decode()
            state.ns.src_filename = src_fileio[-1].name
        else:
            logger.debug("src_fileio.name: [%s]", src_fileio.name)
            filenames = [src_fileio.name]
            logger.debug("src_fileio  names: %s", filenames)

            # state.ns.src_fileio = src_fileio
            state.ns.src_file = src_fileio.getvalue().decode()
            state.ns.src_filename = src_fileio.name
        filename1 = state.ns.src_filename

    filename2 = ""
    if tgt_fileio:
        if isinstance(tgt_fileio, list):
            logger.warning("not set to handle multiple files")
            logger.warning("set accept_multiple_files=False in the meantime")
        else:
            state.ns.tgt_file = tgt_fileio.getvalue().decode()
            state.ns.tgt_filename = tgt_fileio.name
            filename2 = tgt_fileio.name

    # proceed when Submit is clicked
    msg1 = ""
    if filename1:
        msg1 += f" file1 {filename1}"
    msg2 = ""
    if filename2:
        msg2 += f" file2 {filename2}"
    glue = ""
    if filename1 and filename2:
        glue = ", "

    upload_placeholder = st.empty()
    prefix = f" Upload submitted: {msg1}{glue}{msg2}"
    upload_placeholder.write(prefix)

    # st.write(f"  Submitted upload: {msg1}{glue}{msg2}")
    if not submitted:
        return None

    if not (filename1 or filename2):
        # st.write("|  no file uploaded")
        upload_placeholder.write(f"{prefix} no file uploaded")
        return None

    if not filename1:
        # st.write("|  file1 not ready")
        upload_placeholder.write(f"{prefix}, file1 not ready")
        return None

    if not filename2:
        # st.write("|  file2 not ready")
        upload_placeholder.write(f"{prefix}, file2 not ready")
        return None

    try:
        _ = state.ns.src_file.splitlines()
        list1 = [elm.strip() for elm in _ if elm.strip()]
        _ = state.ns.tgt_file.splitlines()
        list2 = [elm.strip() for elm in _ if elm.strip()]
    except Exception as exc:
        logger.error(exc)
        list1 = [""]
        list2 = [""]

    logger.debug("len(list1): %s, len(list2): %s", len(list1), len(list2))

    state.ns.list1 = list1[:]
    state.ns.list2 = list2[:]

    state.ns.updated = True
    logger.debug("state.ns.updated: %s", state.ns.updated)

    return None
