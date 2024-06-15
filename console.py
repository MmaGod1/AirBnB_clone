#!/usr/bin/python3
"""Defines a command interpreter for interaction with BaseModel class."""
import cmd
from models import storage, BaseModel


class HBNBCommand(cmd.Cmd):
    """Handle user commands for interacting with BaseModel instances."""

    prompt = "(hbnb) "

    def do_create(self, arg):
        """Creates a new BaseModel instance.

        Args:
            arg (str): The class name (optional).
        """
        if not arg:
            print("** class name missing **")
            return
        try:
            new_obj = eval(arg)()
        except NameError:
            print("** class doesn't exist **")
            return
        storage.new(new_obj)
        storage.save()
        print(f"** {new_obj.__class__.__name__} created: {new_obj.id} **")

    def do_show(self, arg):
        """Prints the string representation of an instance.

        Args:
            arg (str): Arguments separated by spaces, first is class name, second is id (optional).
        """
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_id = args[1]
        obj = storage.all().get(f"{cls.__name__}.{obj_id}")
        if not obj:
            print("** no instance found **")
            return
        print(obj)

    def do_destroy(self, arg):
        """Destroys an instance based on the class name and id.

        Args:
            arg (str): Arguments separated by spaces, first is class name, second is id (optional).
        """
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_id = args[1]
        obj = storage.all().get(f"{cls.__name__}.{obj_id}")
        if not obj:
            print("** no instance found **")
            return
        storage.delete(obj)
        storage.save()
        print(f"** {obj.__class__.__name__} {obj.id} deleted **")

    def do_all(self, arg):
        """Prints the string representation of all instances based on class name (optional).

        Args:
            arg (str): The class name (optional).
        """
        if arg:
            try:
                cls = eval(arg)
            except NameError:
                print("** class doesn't exist **")
                return
            objects = [str(obj) for obj in storage.all().values() if isinstance(obj, cls)]
        else:
            objects = [str(obj) for obj in storage.all().values()]
        print(objects)

    def do_update(self, arg):
        """Updates an instance based on the class name and id.

        Args:
            arg (str): Arguments separated by spaces: class name, id, attribute name, attribute value.
        """
        args = arg.split()
        if len(args) < 4:
            print("** Attribute name or value missing **")
            return
        if len(args) > 4:
            print("** Too many arguments **")
            return

        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_id = args[1]
        obj = storage.all().get(f"{cls.__name__}.{obj_id}")
        if not obj:
            print("** no instance found **")
            return

        attr_name = args[2]
        if attr

        def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print("")  # Print a newline for better UX
        return True

    def emptyline(self):
        """Do nothing on empty input line"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
