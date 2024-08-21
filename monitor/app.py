import datetime
import os
import secrets

import pandas as pd
import sqlalchemy as sa
from flask import Flask, flash, jsonify, redirect, render_template, request
from marshmallow import Schema, fields, post_load

from plutus.orchestration.models.links import Link
from plutus.scrapers import ScrapeType


class LinkSchema(Schema):
    id = fields.Integer(required=False, allow_none=True)
    url = fields.String(required=True)
    type = fields.Enum(ScrapeType)
    active = fields.Boolean(default=True)
    updated_at = fields.DateTime(default=datetime.datetime.now)
    created_at = fields.DateTime(default=datetime.datetime.now)

    @post_load
    def make_link(self, data, **kwargs):
        return Link(**data)


engine = sa.create_engine(
    os.environ.get("PLUTUS_DB_URI", "")
)  # TODO: use st.secrets instead of os.environ.get("PLUTUS_DB_URI")

Session = sa.orm.sessionmaker(bind=engine)


def fetch_link_data():
    cnx = engine.connect()
    return pd.read_sql(
        "SELECT active, type, url, updated_at, created_at, id FROM plutus_links ORDER BY created_at DESC",
        cnx,
    )


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)


@app.route("/")
def index():
    return render_template("index.html", df=fetch_link_data())


@app.route("/links/<id_>", methods=["DELETE"])
def delete_link(id_):
    with Session() as session:
        session.execute(
            sa.text("DELETE FROM plutus_results WHERE link_id = :id"), {"id": id_}
        )
        session.execute(sa.text("DELETE FROM plutus_links WHERE id = :id"), {"id": id_})
        session.commit()
    flash("Link deleted successfully", "success")
    return redirect("/", 303)


@app.route("/links", methods=["POST"])
def create_link():
    with Session() as session:
        link = LinkSchema().load(request.form)
        session.add(link)
        session.commit()
    flash("Link created successfully", "success")
    return redirect("/", 303)
