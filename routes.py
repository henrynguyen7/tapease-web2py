'''
This code adds and removes the application name from the URLs.
So, "/tapease/a/b/c" becomes "/a/b/c".

This file needs to be placed into the Web2py root directory to function.
'''
routers = {
    'BASE' : {
        'default_application': 'tapease'
    }
}