import os, json

opt = json.loads(open('/home/config.json','r').read())
basedir = os.path.abspath(os.path.dirname(__name__))
homedir = opt['dir_loc']

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        "Vv.MBI7nIZq1i7{"
    FLASK_ENV = os.environ.get("FLASK_ENV") or \
        'development'

from rich.console import Console
console = Console()

def print_log(string):
    console.log(f'[cyan]Progress[/cyan] [aquamarine1]{string}[/aquamarine1]')
def print_error(string):
    console.log(f'[light_pink4]Error[/light_pink4] [red]{string}[/red]')
def print_success(string):
    console.log(f'[spring_green1]Success[/spring_green1] [green1]{string}[/green1]')
def read_json(jsonfile):
    if os.path.exists(jsonfile):
        with open(jsonfile, 'r') as file:
            data = json.loads(file.read())
        return data
    return None
