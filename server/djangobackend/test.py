import environ

env = environ.Env()
environ.Env.read_env()

MONGODB_USERNAME=env('MONGODB_USERNAME')
print(MONGODB_USERNAME)
