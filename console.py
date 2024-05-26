#!/usr/bin/python3
""" console """

import cmd
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex  # for splitting the line along spaces except in double quotes

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """ HBNB console or command-line interface application"""
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits the console"""
        return True

    def help_EOF(self):
        """closes the interactive command-line program"""
        print("closes the interactive command-line program")
        print("Usage: EOF")

    def emptyline(self):
        """ overwriting the emptyline method of the cmd.Cmd
        to handle empyty line"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def help_quit(self):
        print("closes the interactive command-line program")
        print("Usage: quit")

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings

        Args:
            args - a passed string that contains the command to be parsed
            for the creation of the key / value pair
        """
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except Exception as e:
                        try:
                            value = float(value)
                        except Exception as e:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a class

        Args:
            arg - a passed string that contains the name of the model
            whose instance is to be created
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def help_create(self):
        """handles the help command on the use of create commad"""

        print("creates a new instance of a model and saves it")
        print("Usage: create <instance_model_name>")

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""

        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def help_show(self):
        """handles the help command for the show command"""

        print("displays string representation of an instance, ", end="")
        print("based on the class name and id")
        print("Usage: show <instance_model_name> <instance_id>")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id

        Args:
            arg - a string that contains the passed
            instance's class name and id
        """

        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def help_destroy(self):
        """displays help instruction for the use of the destroy command"""

        print("deletes an instance based on the class name and id")
        print("Usage: destroy <instance_model_name> <instance_id>")

    def do_all(self, arg):
        """Prints string representations of a given instance

        Args:
            arg - contains the name of the class whose
            list of instances are to be displayed
        """
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def help_all(self):
        """displays help instruction for the use of the all command"""

        print("prints all string representation of all instances")
        print("Usage: all [<instance_model_name>]")

    def do_update(self, arg):
        """Update an instance based on the class name,
        id, attribute & value

        Args:
            arg - a string which contains the data (key and value)
            to be used for the update
        """
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except Exception as e:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except Exception as e:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def help_update(self):
        """displays the help instruction for the usage of update command"""

        print("updates an instance based on the class name and id, given")
        print("Usage: update <instance_model_name>", end="")
        print(" <instance_id> <attribute_name> <attribute_value>")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
