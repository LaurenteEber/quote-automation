# Implementacion Inicial - Repo Interno

Fecha: 2026-02-08

## 1) Remoto Git
Se agrego script para configurar remoto y push inicial:

- `scripts/git_remote_setup.sh`

Uso:

```bash
./scripts/git_remote_setup.sh <remote_url> [branch_name]
```

Nota: falta ejecutar porque se requiere URL del remoto.

## 2) Integracion Google Sheets (base)
Se agrego modulo reusable:

- `src/staff_quoter/google_sheets/client.py`

Capacidades:
- listar tabs
- leer records y rangos
- limpiar tab
- escribir records (header + rows) en modo `USER_ENTERED`

Script operativo de sync CSV -> Tabs:

- `scripts/sync_csv_to_gsheet.py`

Uso:

```bash
source .venv/bin/activate
python scripts/sync_csv_to_gsheet.py --csv-dir ../artifacts/rebuild_template_csv
```

Requiere `.env` con `GOOGLE_CREDENTIALS_FILE` y `GOOGLE_SHEETS_ID`.

## 3) Pipeline validacion + JSON + PDF
Se agrego pipeline:

- `src/staff_quoter/pipeline/formula_validator.py`
- `src/staff_quoter/pipeline/quote_builder.py`
- `src/staff_quoter/pipeline/pdf_renderer.py`
- `src/staff_quoter/pipeline/runner.py`
- `scripts/run_quote_pipeline.py`

Ejecucion:

```bash
source .venv/bin/activate
python scripts/run_quote_pipeline.py --workbook ../artifacts/workbooks/Staff_Quoter_Rebuild_Foundation_v1.xlsx
```

Salida esperada:
- JSON: `output/json/<quote_id>.json`
- PDF: `output/pdf/<quote_id>.pdf`

## Estado validado
- `scripts/check_env.py` OK
- tests: `4 passed`
- run real del pipeline sobre workbook reconstruido: OK
  - formulas detectadas: 149
  - issues: 0
  - outputs generados: `output/json/Q-0001.json`, `output/pdf/Q-0001.pdf`

## Observaciones
- El workbook actual contiene formulas, pero los valores calculados (`data_only`) aun salen en 0 para algunas salidas. Para cifras finales reales, ejecutar recalc antes del pipeline:

```bash
python scripts/run_quote_pipeline.py --workbook ../artifacts/workbooks/Staff_Quoter_Rebuild_Foundation_v1.xlsx --run-recalc
```

