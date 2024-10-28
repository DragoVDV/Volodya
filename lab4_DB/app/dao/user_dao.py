from sqlalchemy.exc import SQLAlchemyError
from app.models import Person, db
import logging

# Set up logging
logger = logging.getLogger(__name__)

class UserDAO:
    def get_all(self):
        try:
            return Person.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all users: {str(e)}")
            return []  # Return an empty list in case of error

    def get_by_id(self, user_id):
        try:
            return Person.query.get(user_id)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by ID {user_id}: {str(e)}")
            return None  # Return None if not found

    def create(self, name, city_id):
        user = Person(name=name, city_id=city_id)
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()  # Roll back the session on error
            logger.error(f"Error creating user: {str(e)}")
            return None  # Return None on failure

    def update(self, user_id, name=None, city_id=None):
        user = self.get_by_id(user_id)
        if user:
            try:
                if name:
                    user.name = name
                if city_id:
                    user.city_id = city_id
                db.session.commit()
                return user
            except SQLAlchemyError as e:
                db.session.rollback()  # Roll back on error
                logger.error(f"Error updating user {user_id}: {str(e)}")
                return None  # Return None on failure
        return None  # Return None if user not found

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return True  # Return True on successful deletion
            except SQLAlchemyError as e:
                db.session.rollback()  # Roll back on error
                logger.error(f"Error deleting user {user_id}: {str(e)}")
                return False  # Return False on failure
        return False  # Return False if user not found
