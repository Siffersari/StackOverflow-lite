import os
from .... import create_app
from ....db_con import init_db


class BaseModel(object):
    """ 
    This class contains methods that are shared across all other models
    """

    def __init__(self):
        self.db = init_db()

    def get_items_by_id(self, item, item_id):
        """ 
        returns a list of all items with the given id used by question
        and answer models 
        """

        table_name = "%ss" % (self._type().lower()[:-5])
        database = self.db
        item_name = table_name[:-1]
        curr = database.cursor()
        curr.execute("""SELECT %s_id, user_id, title FROM %s WHERE %s_id = %d;""" % (
            item_name, table_name, item, item_id))

        data = curr.fetchall()
        curr.close()

        # return a list of dictionaries
        resp = []
        for i, items in enumerate(data):
            item_id, user_id, title = items
            username = self.get_username_by_id(int(user_id))
            item_dict = {
                "%s_id" % (item_name): int(item_id),
                "username": username,
                "title": title
            }
            resp.append(item_dict)
        return resp

    def get_item_by_id(self, item_id):
        """ returns an entire record by searching for the id number """

        try:
            dbconn = self.db
            curr = dbconn.cursor()
            table_name = "%ss" % (self._type().lower()[:-5])
            item_name = table_name[:-1]
            curr.execute(""" SELECT * FROM %s WHERE %s_id = %d; """ %
                            (table_name, item_name, int(item_id)))
            data = curr.fetchone()
            curr.close()
            return data
        except Exception as e:
            return "Not Found"

    def delete_item(self, item_id, foreign_key):
        """
        This function takes an id and removes the corresponding itme from 
        the database
        """

        try:
            table_name = "%ss" % (self._type().lower()[:-5])
            item_name = table_name[:-1]
            dbconn = self.db
            curr = dbconn.cursor()
            purge_query = "DELETE FROM %s WHERE %s_id = %d;" % (
                foreign_key, item_name, int(item_id))
            curr.execute(purge_query)
            dbconn.commit()
            query = "DELETE FROM %s WHERE %s_id = %d;" % (
                table_name, item_name, int(item_id))

            curr.execute(query)
            curr.close()
            dbconn.commit()

        except Exception as e:
            return "Not Found"
        pass

    def update_item(self, field, data, item_id):
        """ update the field of an item given the item_id """

        try:
            if not isinstance(data, str):
                raise ValueError
            table_name = "%ss" % (self._type().lower()[:-5])
            item_name = table_name[:-1]
            dbconn = self.db
            curr = dbconn.cursor()
            curr.execute("UPDATE %s SET %s = '%s' WHERE %s_id = %d = RETURNING title;" % (
                table_name, field, data, item_name, item_id))

            updated_field = curr.fetchone()
            dbconn.commit()

            return updated_field

        except ValueError:
            return "Data must be a string"
        except Exception as e:
            return e

    def get_username_by_id(self, user_id):
        """ returns a username given the id """

        try:
            dbconn = self.db
            curr = dbconn.cursor()
            curr.execute(
                """ SELECT username FROM users WHERE user_id = %d;""" % (user_id))
            data = curr.fetchone()
            curr.close()

            return data[0]

        except Exception:
            return "Not Found"

    def check_text_exists(self, text):
        """ Checks if the question or answer passed by the user exists """

        table_name = "%ss" % (self._type().lower()[:-5])
        item_name = table_name[:-1]
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute(""" SELECT %s_id FROM %s WHERE body = '%s'; """ % (
            item_name, table_name, text))
        item = curr.fetchone()

        if not item:
            # no question found with that username
            return int(item[0])

    def _type(self):
        """ returns the name of the inheriting class """
        return self.__class__.__name__

    def close_db(self):
        """ This function closes the database connection """
        self.db.close()
        pass