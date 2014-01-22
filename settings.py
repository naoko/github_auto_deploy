import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
PORT = 8001

# logging format
FORMAT = "[%(levelname)s] %(asctime)s %(module)s %(message)s"

LOG_FILE = os.path.join(SITE_ROOT, 'deploy.log')

