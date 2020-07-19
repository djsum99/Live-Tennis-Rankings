import os
import json
from services.io import readJsonFile

configPath = os.path.abspath(os.path.dirname(os.path.join(os.path.abspath(__file__), '../../configs/')))
configPathname = '{}/config.json'.format(configPath)

def appendOsEnvironmentVariables(pathname: str = configPathname) -> None:
    '''
    Sets the OS environment variables from the specified configuration file

    Parameters:
        pathname (str): The pathname of the configuration file where the environment variables are stored
    
    Returns:
        None
    '''

    try:
        environmentVariables = readJsonFile(pathname)['environment']
    except FileNotFoundError as msg:
        print(msg)
        print('Make sure you have the environment config file in the proper place')
        print('environment.json pathname: ' + pathname, end='\n\n')
        exit(0)

    # Note previous environment variables will be overwritten
    os.environ = {**os.environ, **environmentVariables}