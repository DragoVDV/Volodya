from ..dao.city_dao import CityDAO

class CityService:
    def __init__(self):
        self.city_dao = CityDAO()

    def get_all_cities_with_users(self):
        # Використовуємо правильний метод з CityDAO
        return self.city_dao.get_all_cities_with_users()  # Виклик методу, який існує в CityDAO
    
    