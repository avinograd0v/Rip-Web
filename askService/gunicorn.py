import multiprocessing

bind = '127.0.0.1:8081'
workers = multiprocessing.cpu_count() * 2 + 1
errorlog = '/home/andrew/Рабочий стол/webDev/askService/askService/gunicorn.log'