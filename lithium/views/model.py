import json

from flask import Blueprint, request

from lithium.decoder import AlchemyDecoder
from lithium.views.base import BaseView
from lithium.exceptions import HttpNotFound, HttpBadRequest

class ModelView(BaseView):

  model = None
  __exclude__ = []
  db = None

  def post(self):
    data = json.loads(request.data)

    item = self.model(**data)

    if not item.valid:
      raise HttpBadRequest(item.errors)

    self.db.session.add(item)
    self.db.session.commit()

    return AlchemyDecoder(item, self.__exclude__)

  def index(self):
    items = self.model.query.all()
    items = [AlchemyDecoder(item, self.__exclude__) for item in items]
    return items

  def get(self, entity_id):
    item = self.model.query.get(entity_id)

    if item:
      return AlchemyDecoder(item, self.__exclude__)
    else:
      raise HttpNotFound({'error': 'Item not found in database'})

  def put(self, entity_id):
    data = json.loads(request.data)

    item = self.model.query.get(entity_id)

    if not item:
      raise HttpNotFound({'error': 'Item not found in database'})

    for field in data:
      if hasattr(item, field):
        setattr(item, field, data[field])

    if not item.valid:
      raise HttpBadRequest(item.errors)

    self.db.session.add(item)
    self.db.session.commit()

    return AlchemyDecoder(item, self.__exclude__)

  def delete(self, entity_id):
    item = self.model.query.get(entity_id)

    if item:
      self.db.session.delete(item)
      return {'success': 'Item was deleted!'}
    else:
      raise HttpNotFound({'error': 'Item not found in database'})
