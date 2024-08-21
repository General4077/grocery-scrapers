# import os

# import pandas as pd
# import sqlalchemy as sa
# import streamlit as st

# from plutus.orchestration.models.links import Link

# print(st.session_state)

# engine = sa.create_engine(
#     os.environ.get("PLUTUS_DB_URI", "")
# )  # TODO: use st.secrets instead of os.environ.get("PLUTUS_DB_URI")


# def fetch_link_data():
#     cnx = st.connection("plutus_db", type="sql")
#     return cnx.query(
#         "SELECT active, type, url, updated_at, created_at, id FROM plutus_links ORDER BY created_at DESC",
#         ttl=-1,
#     )


# placeholder = st.empty()


# def build_editor():
#     df = fetch_link_data()
#     placeholder.empty()
#     placeholder.data_editor(
#         df,
#         hide_index=True,
#         # use_container_width=True,
#         on_change=update_table,
#         num_rows="dynamic",
#         key="links_df",
#         args=(df,),
#     )


# def build_sidepanel():
#     sb_form = st.sidebar.form(key="options_form")
#     url = sb_form.text_input("URL")
#     link_type = sb_form.selectbox("Type", ["PRODUCT", "SPIDER"])
#     submit = sb_form.form_submit_button("Add Link")
#     strip_params = sb_form.checkbox("Strip URL Params", value=True)
#     if submit:
#         print(insert_link(url, link_type, strip_params))
#         # st.rerun()


# def build_page():
#     build_editor()
#     build_sidepanel()


# # https://www.walmart.com/ip/Great-Value-2-Reduced-Fat-Milk-128-Fl-Oz/10450115
# def update_table(df):
#     state = st.session_state["links_df"]
#     with engine.connect() as conn:
#         if state.get("edited_rows"):
#             idx = pd.Index(list(state["edited_rows"].keys()))
#             df.iloc[idx].apply(
#                 lambda x: conn.execute(
#                     sa.update(Link)
#                     .where(Link.id == x["id"])
#                     .values(state["edited_rows"][x.name])
#                     .returning(Link.id),
#                 ).fetchall(),
#                 axis=1,
#             )
#         if state.get("added_rows"):
#             [
#                 conn.execute(sa.Insert(Link(**v)))
#                 for item in state["added_rows"]
#                 for v in item.values()
#                 if item
#             ]

#         if state.get("deleted_rows"):
#             idx = pd.Index(list(state["deleted_rows"].keys()))
#             df.iloc[idx].apply(
#                 lambda x: conn.execute(
#                     sa.delete(Link).where(Link.id == x["id"]),
#                 ),
#                 axis=1,
#             )
#         conn.commit()
#     build_page()


# def insert_link(
#     url: str, link_type: str = "PRODUCT", strip_params: bool = True
# ) -> bool:
#     if strip_params:
#         url = url.split("?")[0]
#     with engine.connect() as conn:
#         try:
#             conn.execute(
#                 sa.sql.text(
#                     "INSERT INTO plutus_links (url, type) VALUES (:url, :type)"
#                 ),
#                 {"url": url, "type": link_type},
#             )
#             conn.commit()
#             return True
#         except sa.exc.IntegrityError:
#             st.warning("Duplicate Value!")
#             return False


# build_page()
