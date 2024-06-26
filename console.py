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
        """Custom method dispatcher to handle <class name>.all(),
        <class name>.count(), <class name>.show(), <class name>.destroy(),
        and <class name>.update() syntax."""
        args = line.split('.')
        if len(args) < 2:
            print("*** Unknown syntax: {}".format(line))
            return

        class_name, command = args[0], args[1]

        if class_name not in storage_classes:
            print("** class doesn't exist **")
            return

        command_parts = command.split('(')
        if len(command_parts) < 2:
            print("*** Unknown syntax: {}".format(line))
            return

        command_name = command_parts[0]
        command_content = command_parts[1].strip(')')

        if command_name == "all":
            all_instances = [
                str(obj) for key, obj in storage.all().items()
                if key.split('.')[0] == class_name
            ]
            print(all_instances)
            return

        if command_name == "count":
            count = sum(
                1 for obj in storage.all().values()
                if obj.__class__.__name__ == class_name
            )
            print(count)
            return

        if command_name == "show":
            instance_id = command_content.strip('"\'')
            key = "{}.{}".format(class_name, instance_id)
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")
            return

        if command_name == "destroy":
            instance_id = command_content.strip('"\'')
            key = "{}.{}".format(class_name, instance_id)
            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")
            return

        if command_name == "update":
            command_args = shlex.split(command_content)
            if (len(command_args) == 2 and
                    command_args[1].startswith('{') and
                    command_args[1].endswith('}')):
                instance_id = command_args[0].strip('"\'')
                try:
                    update_dict = json.loads(command_args[1])
                    for key, value in update_dict.items():
                        self.do_update(
                            f"{class_name} {instance_id} {key} {value}")
                except json.JSONDecodeError:
                    print("** invalid JSON format **")
                return

            if len(command_args) < 3:
                print("** attribute name or value missing **")
                return

            instance_id = command_args[0].strip('"\'')
            attribute_name = command_args[1].strip('"\'')
            attribute_value = command_args[2].strip('"\'')
            self.do_update(
                f"{class_name} {instance_id} "
                f"{attribute_name} {attribute_value}"
            )
            return

        print("*** Unknown syntax: {}".format(line))

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

        if (len(args) == 3 and
               args[2].startswith('{') and
               args[2].endswith('}')):
            try:
                attribute_dict = eval(args[2])
                for attribute_name, attribute_value in attribute_dict.items():
                    setattr(storage.all()[key], attribute_name,
                            attribute_value)
                storage.all()[key].save()
                return
            except (SyntaxError, ValueError):
                print("** invalid dictionary format **")
                return
            if len(args) < 4:
                print("** value missing **")
                return
            attribute_name = args[2]
            attribute_value = args[3]

            obj = storage.all()[key]
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

    def emptyline(self):
        """Override default `empty line + return` behaviour."""
        pass

    def do_EOF(self, arg):
        """Handles EOF (Ctrl+D) signal."""
        print("")
        return True

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
