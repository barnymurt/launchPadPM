$env:APP_ENV = "live"
$env:APP_PORT = "8001"

python -m uvicorn server:app --host 0.0.0.0 --port $env:APP_PORT
