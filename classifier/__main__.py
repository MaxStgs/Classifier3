#!/usr/bin/env python3

import connexion
import sqlite3

from flask import render_template
from classifier import encoder
from classifier import config

connex_app = config.connex_app


def connect_db(app):
    return sqlite3.connect(app.config['DATABASE'])


@connex_app.route("/home/")
def index():
    return render_template('home.html', )


# @connex_app.route("/")
# def


def main():
    # app = connexion.App(__name__, specification_dir='./swagger/')
    connex_app.app.json_encoder = encoder.JSONEncoder
    connex_app.add_api('swagger.yaml', arguments={'title': 'OIDC Service'})

    connex_app.run(port=5000)


if __name__ == '__main__':
    main()
