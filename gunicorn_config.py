import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = '0.0.0.0:8001'
daemon = True
errorlog = 'logs/gunicorn_error.log'
loglevel = 'debug'
