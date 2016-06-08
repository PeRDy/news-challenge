#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Run script.
"""
import argparse
import inspect
import shlex
import subprocess
import sys


class Main(object):
    INPUT_COMMANDS = ('runserver', 'shell',)

    COMMAND_NAMES = INPUT_COMMANDS + (
        'build',
        'menu',
    )

    # Get all except menu
    COMMANDS = dict(zip(range(1, len(COMMAND_NAMES)), COMMAND_NAMES))

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.add_arguments()
        self.args = self.parser.parse_args()

    def add_arguments(self):
        self.parser.add_argument('command', help='Command to be executed', nargs='?', type=str)
        self.parser.add_argument('args', help='Command args', nargs=argparse.REMAINDER, type=str)

    def get_python(self):
        return 'python'

    def django_admin(self):
        return shlex.split(self.get_python() + " manage.py")

    def runserver(self):
        return shlex.split(self.get_python() + " manage.py runserver 0.0.0.0:8000")

    def migrate(self):
        return shlex.split(self.get_python() + " manage.py migrate")

    def collectstatic(self):
        return shlex.split(self.get_python() + " manage.py collectstatic")

    def shell(self):
        return shlex.split(self.get_python() + " manage.py shell_plus")

    def _print_menu(self):
        menu = "Select a command:\n" + \
               "\n".join(["{:d}) {}".format(k, v.replace('_', ' ').capitalize()) for k, v in self.COMMANDS.items()]) + \
               "\n0) Exit"
        print(menu)

    def menu(self):
        option = None
        while option != 0 and option not in self.COMMANDS.keys():
            self._print_menu()
            try:
                option = input()
            except:
                option = None

        return self.COMMANDS.get(option, '')

    def get_method(self, name):
        try:
            return [method for (n, method) in inspect.getmembers(self, predicate=inspect.ismethod) if n == name][0]
        except IndexError:
            raise ValueError("Command not found: {}".format(name))

    def run_command(self, input_command, *args):
        # Get method
        method = self.get_method(input_command)
        command = method()
        command.extend(args)

        # Run command
        p = subprocess.Popen(args=command)
        while p.returncode is None:
            try:
                p.wait()
            except KeyboardInterrupt:
                pass

        return p.returncode

    def run(self):
        # Call menu ?
        input_command = self.args.command.lower()
        if input_command == 'menu':
            input_command = self.menu()
        try:
            if input_command == 'build':
                self.run_command('django_admin', 'migrate', '--fake-initial')
                return_code = self.run_command('django_admin', 'collectstatic', '--noinput')
            elif input_command in self.INPUT_COMMANDS:
                return_code = self.run_command(input_command, *self.args.args)
            elif input_command is not None:
                # If input_command is not a predefined one, passing it to django_admin command
                return_code = self.run_command('django_admin', input_command, *self.args.args)
            else:
                # Missing input command
                print('Missing or unknown command')
                return_code = 1
        except Exception as e:
            return_code = -1
        return return_code


if __name__ == '__main__':
    main = Main()
    sys.exit(main.run())
