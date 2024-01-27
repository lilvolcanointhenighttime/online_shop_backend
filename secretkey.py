from django.core.management.utils import get_random_secret_key
# Generates secret_key and add it to .env
with open('./.env', 'r') as dotenv:
    vars = dotenv.read()

secretkey ='DJANGO_SECRET_KEY=' + str(get_random_secret_key())
splited_vars = vars.split('\n')
splited_vars[splited_vars.index("DJANGO_SECRET_KEY=")] = secretkey

splited_vars = [i+'\n' for i in splited_vars]
vars = ''.join(splited_vars)

with open('./.env', 'w') as dotenv:
    dotenv.write(vars)