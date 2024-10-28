from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from app.models import City, db
import logging

logger = logging.getLogger(__name__)

class CityDAO:
    def get_all(self):
        try:
            return City.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all cities: {str(e)}")
            return []

    def get_by_id(self, city_id):
        try:
            return City.query.get(city_id)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching city by ID {city_id}: {str(e)}")
            return None

    def create(self, name):
        city = City(name=name)
        try:
            db.session.add(city)
            db.session.commit()
            return city
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error creating city: {str(e)}")
            return None

    def update(self, city_id, name):
        city = self.get_by_id(city_id)
        if city:
            try:
                city.name = name
                db.session.commit()
                return city
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Error updating city {city_id}: {str(e)}")
                return None
        return None

    def delete(self, city_id):
        city = self.get_by_id(city_id)
        if city:
            try:
                db.session.delete(city)
                db.session.commit()
                return True
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Error deleting city {city_id}: {str(e)}")
                return False
        return False

    def get_all_cities_with_users(self):
        try:
            return City.query.options(joinedload(City.people)).all()  # Використовуємо people
        except SQLAlchemyError as e:
            logger.error(f"Error fetching cities with users: {str(e)}")
            return []
    def get_by_id_with_users(self, city_id):
        try:
            # Використовуємо joinedload для завантаження людей разом із містом
            return City.query.options(joinedload(City.people)).filter_by(id=city_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching city with users by ID {city_id}: {str(e)}")
            return None