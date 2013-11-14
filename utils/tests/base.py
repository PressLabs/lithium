from flask.ext.testing import TestCase

from plutonium import create_app
from plutonium.extensions import db

class BaseTest(TestCase):

  def create_app(self):
    return create_app('local_config.py')

  def setUp(self):
    db.create_all()
    #db.engine.execute('pragma foreign_keys=ON')

  def tearDown(self):
    db.session.remove()
    db.drop_all()
