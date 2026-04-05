param(
    [switch]$SkipTests,
    [switch]$UsePysonar
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$envFile = Join-Path $projectRoot ".env"
if (-not (Test-Path $envFile)) {
    throw "Arquivo .env nao encontrado. Crie-o a partir de .env.example."
}

Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#")) {
        return
    }

    $parts = $line -split "=", 2
    if ($parts.Count -eq 2) {
        [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1])
        Set-Item -Path "Env:$($parts[0])" -Value $parts[1]
    }
}

if (-not $env:SONAR_TOKEN) {
    throw "SONAR_TOKEN nao definido no .env."
}

if (-not $env:SONAR_PROJECT_KEY) {
    throw "SONAR_PROJECT_KEY nao definido no .env."
}

Write-Host "Subindo SonarQube..."
docker compose up -d sonarqube

if (-not $SkipTests) {
    Write-Host "Gerando coverage.xml..."
    pytest --cov=app --cov-report=xml
}

if ($UsePysonar) {
    Write-Host "Executando pysonar..."
    pysonar `
        --sonar-host-url=$env:SONAR_HOST_URL `
        --sonar-token=$env:SONAR_TOKEN `
        --sonar-project-key=$env:SONAR_PROJECT_KEY
}
else {
    Write-Host "Executando sonar-scanner em container..."
    $env:SONAR_DOCKER_HOST_URL = "http://sonarqube:9000"
    docker compose run --rm sonar-scanner
}

Write-Host ""
Write-Host "Dashboard:"
Write-Host "http://localhost:9000/dashboard?id=$($env:SONAR_PROJECT_KEY)"
