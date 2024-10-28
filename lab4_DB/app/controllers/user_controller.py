from flask import Blueprint, jsonify, request
from ..services.user_service import UserService

class UserDTO:
    def __init__(self, id, name, city_id):
        self.id = id
        self.name = name
        self.city_id = city_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city_id': self.city_id
        }

    @staticmethod
    def from_dict(data):
        return UserDTO(id=data.get('id'), name=data.get('name'), city_id=data.get('city_id'))


user_controller = Blueprint('user_controller', __name__)
user_service = UserService()

@user_controller.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    user_dto_list = [UserDTO(u.id, u.name, u.city_id) for u in users]
    return jsonify([user_dto.to_dict() for user_dto in user_dto_list])

@user_controller.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user:
        user_dto = UserDTO(user.id, user.name, user.city_id)
        return jsonify(user_dto.to_dict())
    return jsonify({'error': 'User not found'}), 404

@user_controller.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = user_service.create_user(data['name'], data['city_id'])
    user_dto = UserDTO(user.id, user.name, user.city_id)
    return jsonify(user_dto.to_dict()), 201

@user_controller.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = user_service.update_user(user_id, data.get('name'), data.get('city_id'))
    if user:
        user_dto = UserDTO(user.id, user.name, user.city_id)
        return jsonify(user_dto.to_dict())
    return jsonify({'error': 'User not found'}), 404

@user_controller.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_service.delete_user(user_id)
    return jsonify({'message': 'User deleted successfully'}), 200
