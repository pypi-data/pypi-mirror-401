# exceptions.py

# Base Class
class ModManagerError(Exception):
    """Base exception class for the Mod Manager package."""
    
    def __init__(self, module, line_num, msg=None):
        self.module = module
        self.line_num = line_num

        if msg == None:
            msg = 'ModManagerError: A default error has occured.'

        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return self.msg
    

# Sub-classes

## register_obj() exceptions
class ObjectRegistrationError(ModManagerError):
    """Raised when not passing a valid object"""
    def __init__(self, module, line_num):

        msg = (f'Object registration error in module "{module}" : '
        f'{line_num}.\n '
        '.. This occurs when an object name is provided as a `str` '
        'literal and not the object itself.'
        )
        
        super().__init__(module, line_num, msg)


## get_obj() exceptions
class RegistryKeyError(ModManagerError):
    """Raised when a requested objects's key is not found in the 
    :attr:`_REGISTRY`'s `dict{}`."""
    def __init__(self, module, line_num):
        
        msg = (f'Registry key error in module "{module}" : '
        f'{line_num}. \n '
        f'.. An `object` was not registered with the `_REGISTRY`'
        ' or spelled incorrectly. It could also be that you\'re '
        'trying to access the wrong module namespace.'
        )
        
        super().__init__(module, line_num, msg)



## import_modlist() exceptions

class MissingModuleError(ModManagerError):
    """Raised when `import_modlist()` cant find a specified module."""
    def __init__(self, module, line_num):
        #self._import = _import

        msg = (f'A Module was not found by `import_modlist()` in '
        f'"{module}" on "{line_num}". Make sure to check the '
        'spelling of the Modules.'
        )

        super().__init__(module, line_num, msg)
