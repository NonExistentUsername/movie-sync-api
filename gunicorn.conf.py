import multiprocessing


bind = "localhost:80"
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120

# workers = multiprocessing.cpu_count() * 2 + 1
workers = 2