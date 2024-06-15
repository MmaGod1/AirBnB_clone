#!/usr/bin/python3
"""Command interpreter for HBNB project."""
import cmd
import json
import shlex
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it to JSON, and print its id."""
        if not arg:
            print("** class name missing **")
            return
        
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id."""
        if not arg:
            print("** class name missing **")
            return
        
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return
        
        class_name = args[0]
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
        """Deletes an instance based on the class name and id, updates JSON file."""
        if not arg:
            print("** class name missing **")
            return
        
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return
        
        class_name = args[0]
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
        """Prints all string representations of all instances based on class name."""
        args = shlex.split(arg)
        if not arg or args[0] == "":
            all_instances = [str(obj) for obj in storage.all().values()]
            print(all_instances)
        else:
            try:
                eval(args[0])
            except NameError:
                print("** class doesn't exist **")
                return
            all_instances = [str(obj) for key, obj in storage.all().items()
                             if key.split('.')[0] == args[0]]
            print(all_instances)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or updating attribute."""
        if not arg:
            print("** class name missing **")
            return
        
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return
        
        class_name = args[0]
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

    def do_EOF(self, arg):
        """Handles EOF (Ctrl+D) signal."""
        print("")
        return True

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
