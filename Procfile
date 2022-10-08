web: uvicorn main:app --app-dir app --workers 1 --host 0.0.0.0 --port $PORT
worker: uvicorn main:app --app-dir app --workers 1 --host 0.0.0.0 --port 5000
worker: cd bot && python bot.py