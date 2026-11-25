$env:APP_ENV = "local"

# **=> THE PORT IS **A VARIABLE** ✓✓ — **=> AND **THE UI DOES NOT CARE** ✓✓,
# **=> BECAUSE **THE API BASE IS **RELATIVE** ✓✓.
#
# **=> AND **8123** IS **ARBITRARY** ✓✓ — **=> BUT IT IS **ALWAYS THE SAME** ✓✓,
# **=> AND **THAT IS **THE POINT** ✓✓: **=> THE PREVIOUS PAGE YOU HAD OPEN
# **=> KEEPS WORKING** ✓✓, **=> BECAUSE **THE SERVER IS **STILL THERE** ✓✓.
#
# **=> AND THE OLD UI NAMED **PORT 3000** ✓✓, **=> WHICH MATCHED **NEITHER** OF
# **=> THE SERVER'S OWN PORTS** ✓✓ — **=> **8000** FOR STAGING **=> AND **8001**
# **=> FOR LIVE ✓✓ — **=> SO **THE UI'S FETCHES WERE GOING TO A PORT NOTHING
# **=> SERVED** ✓✓.
$env:APP_PORT = if ($env:APP_PORT) { $env:APP_PORT } else { "8123" }

Write-Host ""
Write-Host "  AgentPad is starting on http://127.0.0.1:$($env:APP_PORT)/ui"
Write-Host "  The API base is relative, so that address works from any port."
Write-Host "  To use another port:  `$env:APP_PORT = 3125; ./scripts/run_local.ps1"
Write-Host ""

python -m uvicorn server:app --host 127.0.0.1 --port $env:APP_PORT
