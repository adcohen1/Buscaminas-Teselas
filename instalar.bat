@echo off
echo ===================================================
echo     Instalador de Dependencias - Buscaminas
echo ===================================================
echo.

:: Comprobar si 'uv' está instalado
where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [OK] 'uv' detectado. Instalando dependencias con uv...
    uv sync
    echo.
    echo [EXITO] Entorno virtual configurado en .venv con todas las dependencias.
) else (
    echo [ADVERTENCIA] 'uv' no esta instalado en este sistema.
    echo Se procedera a instalar de forma clasica con pip y venv...
    echo.
    
    if not exist ".venv" (
        echo Creando entorno virtual .venv...
        python -m venv .venv
    )
    
    echo Activando entorno virtual e instalando dependencias...
    call .venv\Scripts\activate.bat
    pip install -e .
    echo.
    echo [EXITO] Dependencias instaladas en .venv.
)

echo.
pause
