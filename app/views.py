from . import app, db
from flask import render_template, request, jsonify, redirect, url_for, abort

from .models import Item

import uuid
import datetime
import boto3


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/item', methods=['GET', 'POST'])
def items():
    """
    GET     List all available items (should probably be limited)
    POST    Upload a new item. Returns UUID.
    """

    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        file = request.files["file"]    # todo give a better error than 400
        if file and file.filename.endswith(".html"):
            uuid_ = uuid.uuid4().hex
            name = uuid_ + "/" + file.filename
            expires = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            delete_key = uuid.uuid4().hex

            session = boto3.session.Session(
                aws_access_key_id=app.config['AWS_S3UPLOAD_ID'],
                aws_secret_access_key=app.config['AWS_S3UPLOAD_KEY'])

            s3 = session.resource('s3')
            s3_object = s3.Object('dotfile.ca', name)
            s3_object.put(Body=file, ACL='public-read', ContentType='text/html',
                          StorageClass='REDUCED_REDUNDANCY')

            item = Item(uuid=uuid_,
                        expires=expires,
                        delete_key=delete_key,
                        uri="https://s3.amazonaws.com/dotfile.ca/" + name)

            db.session.add(item)
            db.session.commit()

            print(uuid_, delete_key, item.uri)

            return jsonify(uuid=uuid_, delete_key=delete_key, uri=item.uri)
        else:
            print("Not html")
            # return 40x
            pass


@app.route('/item/<uuid>', methods=['GET', 'DELETE'])
def item(uuid):
    """
    GET     Returns the item.
    DELETE  Delete the item. Requires delete_key to be passed in.
    """

    item = Item.query.filter_by(uuid=uuid).first()

    if item is None:
        abort(404)

    return render_template('item.html', src_path=item.uri)


@app.route('/api/item/<uuid>')
def get_item(uuid):
    """Gets URI of item in S3"""
    pass
