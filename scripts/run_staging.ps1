$env:APP_ENV = "staging"
$env:APP_PORT = "8000"

while ($true) {
  python -m uvicorn server:app --host 0.0.0.0 --port $env:APP_PORT
  Start-Sleep -Seconds 1
}


