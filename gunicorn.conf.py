import multiprocessing


bind = "127.0.0.1:8000"
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 60

# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
threads = multiprocessing.cpu_count() * 2 + 1
