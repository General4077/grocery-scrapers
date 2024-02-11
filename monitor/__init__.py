import os

import pandas as pd
import sqlalchemy as sa
import streamlit as st

engine = sa.create_engine(os.environ.get("PLUTUS_DB_URI"))
cnx = st.connection("plutus_db", type="sql")


def update_table():
    state = st.session_state["links_df"]
    if state.get("edited_rows"):
        idx = pd.Index(list(state["edited_rows"].keys()))
        print(idx)
    if state.get("added_rows"):
        idx = pd.Index(list(state["added_rows"].keys()))
        print(idx)
    if state.get("deleted_rows"):
        idx = pd.Index(list(state["deleted_rows"].keys()))
        print(idx)

    print(state)


def insert_link(url: str, link_type: str, strip_params: bool = True) -> bool:
    if strip_params:
        url = url.split("?")[0]
    with engine.connect() as conn:
        try:
            conn.execute(
                sa.sql.text(
                    "INSERT INTO plutus_links (url, type) VALUES (:url, :type)"
                ),
                {"url": url, "type": link_type},
            )
            conn.commit()
            return True
        except sa.exc.IntegrityError:
            st.warning("Duplicate Value!")
            return False


def paint_dataframe():
    df = cnx.query(
        "SELECT active, type, url, updated_at, created_at, id FROM plutus_links"
    )
    st.data_editor(
        df,
        hide_index=True,
        use_container_width=True,
        on_change=update_table,
        num_rows="dynamic",
        key="links_df",
    )


sb_form = st.sidebar.form("options_form")
url = sb_form.text_input("URL")
link_type = sb_form.selectbox("Type", ["PRODUCT", "SPIDER"])
submit = sb_form.form_submit_button("Add Link")
strip_params = sb_form.checkbox("Strip URL Params", value=True)
if submit:
    print(insert_link(url, link_type, strip_params))
    st.rerun()
paint_dataframe()
