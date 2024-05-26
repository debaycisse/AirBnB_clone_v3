#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pycodestyle
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        st = State()
        st.name = "Lagos"
        st.save()
        cts = ['Ketu', 'Maryland', 'Lagos Island']
        for i in range(3):
            ct = City()
            ct.name = cts[i]
            ct.state_id = st.id
            ct.save()
        all_objs_counts = all_state_obj_counts = all_city_obj_counts = 0
        for obj in models.storage.all():
            all_objs_counts += 1
        for state_obj in models.storage.all(State):
            all_state_obj_counts += 1
        for city_obj in models.storage.all(City):
            all_city_obj_counts += 1
        self.assertTrue(all_objs_counts > all_state_obj_counts)
        self.assertTrue(all_objs_counts > all_city_obj_counts)
        self.assertTrue(all_city_obj_counts > all_state_obj_counts)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_with_a_specified_class(self):
        """Test that all returns only the instances of the given class"""
        state_list = ['Lagos', 'Abuja', 'Abeokuta']
        city_list = ['Ketu', 'Gwagwalada', 'Kuto, Abeokuta']
        for i in range(3):
            st = State(name=state_list[i])
            st.save()
            ct = City(name=city_list[i], state_id=st.id)
            ct.save()
        for db_st_inst in models.storage.all(State):
            db_st_inst_cls = db_st_inst.split('.')[0]
            self.assertTrue(classes[db_st_inst_cls] is classes['State'])
        for db_ct_inst in models.storage.all(City):
            db_ct_inst_cls = db_ct_inst.split('.')[0]
            self.assertTrue(classes[db_ct_inst_cls] is classes['City'])

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        st = State()
        st.name = 'Lagos'
        models.storage.save()
        st_key = st.__class__.__name__ + '.' + st.id
        # checking if object exists before calling the new() method
        self.assertFalse(st_key in models.storage.all())
        models.storage.new(st)    # calling the new method
        models.storage.save()
        # checking if object exists after the calling new() method
        self.assertTrue(st_key in models.storage.all())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        st = State()
        st.name = 'Lagos'
        models.storage.new(st)
        st_key = st.__class__.__name__ + '.' + st.id
        # checking that object is added to the database, via its' key
        self.assertTrue(st_key in models.storage.all())
        # update and check an object's attribute after saving
        st.name = 'Abuja'
        models.storage.save()
        st_obj_from_db = models.storage.all(State)[st_key]
        self.assertTrue(st.name == st_obj_from_db.name)
