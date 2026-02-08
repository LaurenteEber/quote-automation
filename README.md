# Staff Quoter Internal Dev Repo

Repositorio interno para desarrollo del sistema automatizado de cotizaciones Staff (MACHINING + FABRICATION), orientado a implementación en Google Sheets y tooling Python.

## Estructura
- `src/staff_quoter/`: código fuente del proyecto.
- `scripts/`: scripts operativos (bootstrap, validaciones, utilidades).
- `tests/`: pruebas automatizadas.
- `docs/`: documentación técnica del repo de desarrollo.

## Datos y artefactos externos
Los artefactos de análisis y workbooks quedaron organizados en la carpeta padre:
- `../artifacts/workbooks/`
- `../artifacts/reports/`
- `../artifacts/foundation_master_data/`
- `../artifacts/rebuild_template_csv/`

## Inicio rápido
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configurar remoto Git
```bash
./scripts/git_remote_setup.sh <remote_url> [branch_name]
```

## Seguridad de secretos
1. Crear `.env` local y proteger permisos:
```bash
cp .env.example .env
chmod 600 .env
```
2. Activar hook local anti-secretos:
```bash
./scripts/setup_hooks.sh
```
3. Escaneo manual:
```bash
python3 scripts/scan_secrets.py
```

Guia detallada: `docs/secrets_management.md`

## Ejecutar pipeline de cotizacion
```bash
source .venv/bin/activate
python scripts/run_quote_pipeline.py --workbook ../artifacts/workbooks/Staff_Quoter_Rebuild_Foundation_v1.xlsx
```

Opciones:
- `--run-recalc`: ejecuta recalc LibreOffice antes de validar formulas.
- `--allow-formula-issues`: no falla el pipeline si se detectan issues.

## Primer sync a Google Sheets
```bash
source .venv/bin/activate
python scripts/sync_csv_to_gsheet.py --csv-dir ../artifacts/rebuild_template_csv
```
