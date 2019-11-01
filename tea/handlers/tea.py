from pyramid.view import view_config
from tea.handlers.base import BaseHandler, BaseSchema
from tea.models.tea import Tea
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound

from colander import SchemaNode, String, Int


class TeaSchema(BaseSchema):
    name = SchemaNode(String())
    flavors = SchemaNode(String(), missing=None)
    origin_id = SchemaNode(Int())


class Handler(BaseHandler):
    @view_config(route_name='tea', request_method='GET', renderer='json')
    def get_tea(self):
        this_tea = []
        for tea in self.db.query(Tea).order_by(Tea.name):
            tea_item = tea.to_dict()
            tea_item['origin'] = tea.origin.country
            this_tea.append(tea_item)
        return this_tea

    @view_config(route_name='tea', request_method='POST', renderer='json')
    def create_tea(self):
        form = self._validate_request(TeaSchema)
        new_tea = self.bind_form(Tea(), form)
        print(new_tea.name)
        tea_id = ''
        if self.db.query(Tea).filter_by(name=new_tea.name).one_or_none():
            self.db.rollback()
            err_msg = 'Tea Already Exhists'
            print(err_msg)
            self.db.close()
            return HTTPForbidden(body='{msg:"Tea Already Exhists"}')
        else:
            self.db.add(new_tea)
            new_tea = self.db.merge(new_tea)
            tea_id = new_tea.id
            self.db.commit()
            self.db.close()
            return {'id': tea_id}

    @view_config(route_name='tea', request_method='PUT', renderer='json')
    def update_tea(self):
        # form = Form(TeaSchema())
        tea_id = ''
        attrs = self.rdata.copy()
        try:
            query = self.db.query(Tea).filter_by(id=self.rdata['id'])
            found_tea = query.one_or_none()

            if not found_tea:
                return HTTPNotFound('No Tea Found with that ID')

            for key in attrs:
                setattr(found_tea, key, attrs[key])

            self.db.add(found_tea)
            found_tea = self.db.merge(found_tea)
            tea_id = found_tea.id
            self.db.commit()
            self.db.close()
            return {'id': tea_id}

        except Exception as e:
            self.db.rollback()
            err_msg = 'Error when updating application with ID {}: {}'.format(
                tea_id, e)
            print(err_msg)
            return HTTPNotFound(err_msg)

    @view_config(route_name='flavors', request_method='GET', renderer='json')
    def get_flavors(self):
        session = self.db
        list = []
        for instance in session.query(Tea.flavors).distinct():
            list.append(instance[0])

        uniques = []
        for value in list:
            items = value.split(',')
            for item in items:
                if item.strip() not in uniques:
                    uniques.append(item.strip())

        return uniques
