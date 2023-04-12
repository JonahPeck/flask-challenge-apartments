from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apartments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


class Index(Resource):
    def get(self):
        response = make_response(
            {
                "message": "Welcome Tenants"
            },
            200
        )
        return response


api.add_resource(Index, '/')


class AllApartments(Resource):
    def post(self):
        data = request.get_json()
        try:
            apartment = Apartment(
                room_number=data['room_number']
            )
            db.session.add(apartment)
            db.session.commit()
        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message,
                422
            )
        response = make_response(
            apartment.to_dict(),
            201
        )
        return response

    def get(self):
        apartments = Apartment.query.all()
        apartments_dict_list = [apartment.to_dict()
                                for apartment in apartments]
        response = make_response(
            apartments_dict_list,
            200
        )
        return response


api.add_resource(AllApartments, '/apartments')


class ApartmentById(Resource):
    def delete(self, id):
        apartment = Apartment.query.filter_by(id=id).first()
        if not apartment:
            return make_response({
                "error": "Activity not found"

            }, 404)
        try:
            db.session.delete(apartment)
            db.session.commit()
        except Exception as e:
            return make_response(
                {
                    "errors": [e.__str__()]
                },
                422
            )
        return make_response(
            "",
            200
        )

    def patch(self, id):
        data = request.get_json()

        apartment = Apartment.query.filter_by(id=id).first()
        for attr in data.keys():
            print(attr)
            setattr(apartment, attr, data[attr])

        db.session.add(apartment)
        db.session.commit()

        response_dict = apartment.to_dict()

        response = make_response(
            response_dict,
            200
        )

        return response


api.add_resource(ApartmentById, '/apartments/<int:id>')


class AllTenants(Resource):
    def post(self):
        data = request.get_json()
        try:
            tenant = Tenant(
                name=data['name'],
                age=data['age']
            )
            db.session.add(tenant)
            db.session.commit()
        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message,
                422
            )
        response = make_response(
            tenant.to_dict(),
            201
        )
        return response

    def get(self):
        tenants = Tenant.query.all()
        tenants_dict_list = [tenant.to_dict()
                             for tenant in tenants]
        response = make_response(
            tenants_dict_list,
            200
        )
        return response


api.add_resource(AllTenants, '/tenants')


class TenantById(Resource):
    def delete(self, id):
        tenant = Tenant.query.filter_by(id=id).first()
        if not tenant:
            return make_response({
                "error": "Activity not found"

            }, 404)
        try:
            db.session.delete(tenant)
            db.session.commit()
        except Exception as e:
            return make_response(
                {
                    "errors": [e.__str__()]
                },
                422
            )
        return make_response(
            "",
            200
        )

    def patch(self, id):
        data = request.get_json()

        tenant = Tenant.query.filter_by(id=id).first()
        for attr in data.keys():
            print(attr)
            setattr(tenant, attr, data[attr])

        db.session.add(tenant)
        db.session.commit()

        response_dict = tenant.to_dict()

        response = make_response(
            response_dict,
            200
        )

        return response


api.add_resource(TenantById, '/tenants/<int:id>')


class LeaseById(Resource):
    def delete(self, id):
        lease = Lease.query.filter_by(id=id).first()
        if not lease:
            return make_response({
                "error": "Activity not found"

            }, 404)
        try:
            db.session.delete(lease)
            db.session.commit()
        except Exception as e:
            return make_response(
                {
                    "errors": [e.__str__()]
                },
                422
            )
        return make_response(
            "",
            200
        )


api.add_resource(LeaseById, '/leases/<int:id>')


class AllLeases(Resource):
    def get(self):
        leases = Lease.query.all()
        leases_dict_list = [lease.to_dict()
                            for lease in leases]
        response = make_response(
            leases_dict_list,
            200
        )
        return response

    def post(self):
        data = request.get_json()
        try:
            lease = Lease(
                rent=data['rent']
            )
            db.session.add(lease)
            db.session.commit()
        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message,
                422
            )
        response = make_response(
            lease.to_dict(),
            201
        )
        return response


api.add_resource(AllLeases, '/leases')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
