import os

basedir = os.path.abspath(os.path.dirname(__file__))

AWS_S3UPLOAD_ID = "*******"
AWS_S3UPLOAD_KEY = "*******"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

try:
    from local_config import *      # noqa
except ImportError:
    pass
