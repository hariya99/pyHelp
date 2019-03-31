import io
import sys, os
import subprocess as sp

class ModulesHelp:
    '''
        class to capture help function output of modules
        and display it in defaul text editor on the platform.
    '''
    def __init__(self):
        '''
            user passes in the module name which is a string
            import_module captures the import module
            stdout_original captures the original stdout state
            instance_StringIO captures temporary redirection of stdout
        '''
        self.module = ''
        self.default_editor = ''
        self.import_module = None 
        self.stdout_original = None
        self.instance_StringIO = None 

    def get_module(self):
        '''
            get the module which user wants to check help of. 
            import the module, chop off the child part if given by user 
            while importing. 
        '''
        try:
            self.module = str(input("Which python fucntion's doc you want to see? "))
            #create an instance of import class
            self.import_module = __import__(self.module.split('.')[0])
        except:
            print(sys.exc_info()[1])
            sys.exit()

    def set_stdout(self):
        '''
            stdout redirection
        '''
        # Temporarily redirect stdout to a StringIO.
        self.stdout_original   = sys.stdout
        self.instance_StringIO = io.StringIO()
        sys.stdout = self.instance_StringIO

    def call_help(self):

        # call help now to get the output into s 
        try:
            help(self.module)
            self._restore_stdout()
        except:
            print(sys.exc_info()[1])
            sys.exit()

    def _restore_stdout(self):
        sys.stdout = self.stdout_original

    def write_to_file(self):
        self.instance_StringIO.seek(0)

        with open('help.txt', 'w') as hfile:
            hfile.write(self.instance_StringIO.read())

    def get_default_editor(self):
        if sys.platform.startswith('linux'):
            #set it based on linux flavor
            self.default_editor = 'textpad'
        elif sys.platform.startswith('win32'):
            self.default_editor = 'notepad'
        elif sys.platform.startswith('darwin'):
            self.default_editor = 'TextEdit'
        else:
            self.default_editor = ''

    def open_editor(self):
        ''' 
            open the file with default editor on platform. if none found then 
            print the output on command line itself.
        '''
        try:
            if self.default_editor == '' and sys.platform.startswith('linux'):
                process = sp.run(['cat', 'help.txt'])
            elif self.default_editor == '' and sys.platform.startswith('win32'):
                process = sp.run(['type', 'help.txt'])
            else:
                process = sp.run(['open' , '-a' , self.default_editor, 'help.txt'])
        except:
            print(sys.exc_info()[1])
            sys.exit()
        finally:
            try:
                process.check_returncode()
                print("Process Completed")
            except:
                print("Error")
                print(sys.exc_info()[1]) 
                sys.exit()           


if __name__ == "__main__":
    helpObj = ModulesHelp()
    helpObj.get_module()
    helpObj.set_stdout()
    helpObj.call_help()
    helpObj.write_to_file()
    helpObj.get_default_editor()
    helpObj.open_editor()