from flask import Blueprint, jsonify, request
from app.dao.city_dao import CityDAO
from ..services.city_services import CityService
from .user_controller import UserDTO
class CityDTO:
    def __init__(self, id, name, users=None):
        self.id = id
        self.name = name
        self.users = users if users is not None else []

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            
        }
    
    def to_dict_users_in_city(self):
        return {
            'id': self.id,
            'name': self.name,
            'users': [user.to_dict() for user in self.users]  # Передаємо користувачів у словник
        }

    @staticmethod
    def from_dict(data):
        return CityDTO(
            id=data.get('id'),
            name=data.get('name'),
            users=[UserDTO.from_dict(user) for user in data.get('users', [])]  # Додаємо користувачів
        )


city_controller = Blueprint('city_controller', __name__)
city_dao = CityDAO()
city_service = CityService()

@city_controller.route('/cities', methods=['GET'])
def get_cities():
    cities = city_dao.get_all()
    city_dto_list = [CityDTO(city.id, city.name) for city in cities]
    return jsonify([city_dto.to_dict() for city_dto in city_dto_list])

@city_controller.route('/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):
    # Використовуємо метод, який завантажує користувачів разом із містом
    city = city_dao.get_by_id_with_users(city_id)
    if city:
        users_dto = [UserDTO(u.id, u.name, u.city_id) for u in city.people]
        city_dto = CityDTO(city.id, city.name, users_dto)
        return jsonify(city_dto.to_dict_users_in_city())
    return jsonify({'error': 'City not found'}), 404

@city_controller.route('/cities', methods=['POST'])
def create_city():
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'City name is required.'}), 400

    city = city_dao.create(name)
    if city:
        city_dto = CityDTO(city.id, city.name)
        return jsonify(city_dto.to_dict()), 201
    
    return jsonify({'error': 'City creation failed.'}), 500



@city_controller.route('/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'City name is required.'}), 400

    city = city_dao.update(city_id, name)
    if city:
        city_dto = CityDTO(city.id, city.name)
        return jsonify(city_dto.to_dict())
    
    return jsonify({'error': 'City not found'}), 404

@city_controller.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    success = city_dao.delete(city_id)
    if success:
        return jsonify({'message': 'City deleted successfully'}), 200
    
    return jsonify({'error': 'City not found'}), 404


@city_controller.route('/cities_with_users', methods=['GET'])
def get_cities_with_users():
    cities = city_service.get_all_cities_with_users()  # викликаємо через екземпляр
    
    city_dto_list = []
    for city in cities:
        users_dto = [UserDTO(u.id, u.name, u.city_id) for u in city.people]
        city_dto = CityDTO(city.id, city.name, users_dto)
        city_dto_list.append(city_dto)
    
    return jsonify([city_dto.to_dict_with_users_in_city() for city_dto in city_dto_list])