import multiprocessing


bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 20

# workers = multiprocessing.cpu_count() * 2 + 1
workers = 2