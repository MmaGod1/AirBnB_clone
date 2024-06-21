#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import shlex
import uuid
import json
from models.base_model import BaseModel
from models.user import User
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


# Define the storage classes available
storage_classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Review": Review
}


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the HBNB project."""
    prompt = '(hbnb) '

    def default(self, line):
        """Custom method dispatcher to handle <class name>.all() and <class name>.count() syntax."""
        args = line.split('.')
        if len(args) > 1:
            class_name = args[0]
            command = args[1]

            if class_name in storage_classes:
                if command == "all()":
                    all_instances = [str(obj) for key, obj in storage.all().items()
                                     if key.split('.')[0] == class_name]
                    print(all_instances)
                    return

                if command == "count()":
                    count = sum(1 for obj in storage.all().values()
                                if obj.__class__.__name__ == class_name)
                    print(count)
                    return

                if command.startswith("update(") and command.endswith(")"):
                    command_args = shlex.split(command[7:-1].strip('"\''))

                    if len(command_args) < 3:
                        print("** attribute name or value missing **")
                        return

                    instance_id = command_args[0]
                    attribute_name = command_args[1]
                    attribute_value = command_args[2]

                    try:
                        uuid.UUID(instance_id)
                    except ValueError:
                        print("** no instance found **")
                        return

                    key = "{}.{}".format(class_name, instance_id)
                    if key in storage.all():
                        obj = storage.all()[key]

                        setattr(obj, attribute_name, attribute_value)
                        obj.save()
                    else:
                        print("** no instance found **")
                    return

        print("*** Unknown syntax:", line)
    def do_create(self, arg):
        """Usage: create <class>
        Creates a new instance of BaseModel, saves
        it (to the JSON file) and prints the id.
        """
        if not arg:
            print("** class name missing **")
            return

        if arg not in storage_classes:
            print("** class doesn't exist **")
            return

        new_instance = storage_classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Usage: show <class> <id>
        Prints the string representation of an
        instance based on the class name and id.
        """
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in storage_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)

        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Usage: destroy <class> <id>
        Deletes an instance based on the class name and
        id (save the change into the JSON file).
        """
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in storage_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)

        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Usage: all or all <class>
        Prints all string representation of all instances
        based or not on the class name.
        If no class is specified, displays all instantiated objects.
        """
        args = shlex.split(arg)
        if not args:
            all_instances = [str(obj) for obj in storage.all().values()]
            print(all_instances)
        else:
            class_name = args[0]
            if class_name not in storage_classes:
                print("** class doesn't exist **")
                return
            all_instances = [str(obj) for key, obj in storage.all().items()
                             if key.split('.')[0] == class_name]
            print(all_instances)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value>
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        """
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in storage_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)

        if key not in storage.all():
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attribute_name = args[2]
        attribute_value = args[3]

        obj = storage.all()[key]

        # Try to convert attribute_value to the correct type
        try:
            attribute_value = eval(attribute_value)
        except (NameError, SyntaxError):
            pass

        setattr(obj, attribute_name, attribute_value)
        obj.save()

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in storage_classes:
            print("** class doesn't exist **")
            return

        count = sum(1 for obj in storage.all().values()
                    if obj.__class__.__name__ == class_name)
        print(count)

    def do_EOF(self, arg):
        """Handles EOF (Ctrl+D) signal."""
        print("")
        return True

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
