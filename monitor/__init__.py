import os

import pandas as pd
import sqlalchemy as sa
import streamlit as st

from plutus.orchestration.models.links import Link

engine = sa.create_engine(
    os.environ.get("PLUTUS_DB_URI", "")
)  # TODO: use st.secrets instead of os.environ.get("PLUTUS_DB_URI")
cnx = st.connection("plutus_db", type="sql")


def update_table(df):
    state = st.session_state["links_df"]
    with engine.begin() as cnx:
        if state.get("edited_rows"):
            idx = pd.Index(list(state["edited_rows"].keys()))

            # TODO use the bulk update syntax(https://docs.sqlalchemy.org/en/20/tutorial/data_update.html) with to_json() for fast updates

            df.iloc[idx].apply(
                lambda x: cnx.execute(
                    sa.update(Link)
                    .where(Link.id == x["id"])
                    .values(active=x["active"], type=x["type"], url=x["url"])
                    .returning(Link.id),
                ),
                axis=1,
            )
            cnx.commit()
        if state.get("added_rows"):
            idx = pd.Index(list(state["added_rows"].keys()))
            print(idx)
        if state.get("deleted_rows"):
            idx = pd.Index(list(state["deleted_rows"].keys()))
            print(idx)
    del st.session_state["links_df"]


df = cnx.query("SELECT active, type, url, updated_at, created_at, id FROM plutus_links")
st.data_editor(
    df,
    hide_index=True,
    use_container_width=True,
    on_change=update_table,
    num_rows="dynamic",
    key="links_df",
    args=(df,),
)


def insert_link(
    url: str, link_type: str = "PRODUCT", strip_params: bool = True
) -> bool:
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


sb_form = st.sidebar.form(key="options_form")
url = sb_form.text_input("URL")
link_type = sb_form.selectbox("Type", ["PRODUCT", "SPIDER"])
submit = sb_form.form_submit_button("Add Link")
strip_params = sb_form.checkbox("Strip URL Params", value=True)
if submit:
    print(insert_link(url, link_type, strip_params))
    st.rerun()
