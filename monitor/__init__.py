import os

import sqlalchemy as sa
import streamlit as st

engine = sa.create_engine(os.environ.get("PLUTUS_DB_URI"))
cnx = st.connection("plutus_db", type="sql")


@st.cache_data(ttl=30)
def paint_dataframe():
    df = cnx.query(
        "SELECT active, type, url, updated_at, created_at, id FROM plutus_links"
    )
    st.data_editor(df, hide_index=True)


sb_form = st.sidebar.form("options_form")
url = sb_form.text_input("URL")
link_type = sb_form.selectbox("Type", ["PRODUCT", "SPIDER"])
submit = sb_form.form_submit_button("Add Link")
if submit:
    with engine.connect() as conn:
        try:
            conn.execute(
                sa.sql.text(
                    "INSERT INTO plutus_links (url, type) VALUES (:url, :type)"
                ),
                {"url": url, "type": link_type},
            )
            conn.commit()
        except sa.exc.IntegrityError:
            st.warning("Duplicate Value!")
        paint_dataframe()
paint_dataframe()
