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
        """Custom method dispatcher to handle <class name>.update(<id>, 
        <attribute name>, <attribute value>) and <class name>.update(<id>, 
        <dictionary>) syntax."""
        args = line.split('.', 1)
        if len(args) == 2:
            class_name = args[0]
            if class_name in storage_classes:
                command = args[1].strip()
                if command.startswith("update(") and command.endswith(")"):
                    params = command[7:-1].strip()
                
                    if params.startswith("{") and params.endswith("}"):
                        # Handle dictionary update
                        try:
                            id_and_dict = params.split(", ", 1)
                            if len(id_and_dict) != 2:
                                print("** attribute name or value missing **")
                                return
                        
                            instance_id = id_and_dict[0].strip('"')
                            attributes = eval(id_and_dict[1])
                        
                            if not isinstance(attributes, dict):
                                print("** attribute name or value missing **")
                                return

                            key = f"{class_name}.{instance_id}"
                            if key in storage.all():
                                obj = storage.all()[key]
                                for attr, value in attributes.items():
                                    setattr(obj, attr, value)
                                obj.save()
                                return
                            else:
                                print("** no instance found **")
                                return
                        except Exception as e:
                            print(f"** error: {e} **")
                            return
                    else:
                        # Handle regular update
                        params = params.split(", ", 2)
                        if len(params) == 3:
                            instance_id = params[0].strip('"')
                            attribute_name = params[1].strip('"')
                            attribute_value = params[2].strip('"')
                        
                            key = f"{class_name}.{instance_id}"
                            if key in storage.all():
                                obj = storage.all()[key]
                            
                                # Try to convert attribute_value to the correct type
                                try:
                                    attribute_value = eval(attribute_value)
                                except (NameError, SyntaxError):
                                    pass
  
                                setattr(obj, attribute_name, attribute_value)
                                obj.save()
                                return
                            else:
                                print("** no instance found **")
                                return
                        else:
                            print("** attribute name or value missing **")
                            return
                else:
                    print("*** Unknown syntax:", line)
                    return
            else:
                print("** class doesn't exist **")
                return
        else:
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
