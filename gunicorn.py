import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = 'localhost:8001'
