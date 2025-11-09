# ...existing code...
import os, traceback
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fightrec.settings")
import django
django.setup()

from django.apps import apps
from django.db.models import DecimalField
from django.db import connection

print("Scanning models for Decimal conversion failures...")

for model in apps.get_models():
    decimal_fields = [f for f in model._meta.get_fields() if isinstance(f, DecimalField)]
    if not decimal_fields:
        continue

    pk_name = model._meta.pk.name
    table = model._meta.db_table
    print(f"\nChecking model {model.__name__} (table {table}) fields: {[f.name for f in decimal_fields]}")

    # get all primary keys via raw SQL to avoid early conversion
    with connection.cursor() as cursor:
        try:
            cursor.execute(f'SELECT "{pk_name}" FROM "{table}";')
            pks = [r[0] for r in cursor.fetchall()]
        except Exception as e:
            print(f"  SKIP: could not read table {table}: {e!r}")
            continue

    for pk in pks:
        try:
            # This will trigger Django's converters; wrap to catch decimal errors
            obj = model.objects.get(**{pk_name: pk})
            for f in decimal_fields:
                try:
                    _ = getattr(obj, f.name)
                except Exception:
                    raise
        except Exception as exc:
            tb = traceback.format_exc(limit=5)
            # fetch raw value from DB for diagnostic
            raw_val = None
            with connection.cursor() as cursor:
                try:
                    select_columns = ', '.join([f'"{fld.name}"' for fld in decimal_fields])
                    sql = f'SELECT {select_columns} FROM "{table}" WHERE "{pk_name}" = ?;'
                    cursor.execute(sql, (pk,))
                    row = cursor.fetchone()
                    raw_val = row
                except Exception as e2:
                    raw_val = f"failed to read raw row: {e2!r}"

            print("=== ERROR ===")
            print(f"Model: {model.__name__}  table: {table}  pk: {pk_name}={pk}")
            print("Decimal fields:", [f.name for f in decimal_fields])
            print("Exception:", repr(exc))
            print("Traceback (short):\n", tb)
            print("Raw DB values for decimal fields:", raw_val)
            # suggested fix (example)
            print("Suggested sqlite SQL to set problematic columns to NULL (adjust pk literal if text):")
            pk_literal = f"'{pk}'" if isinstance(pk, str) else str(pk)
            for f in decimal_fields:
                print(f'  UPDATE "{table}" SET "{f.name}" = NULL WHERE "{pk_name}" = {pk_literal};')
            # stop after first found to avoid flooding
            raise SystemExit(1)

print("Scan complete — no conversion failures detected.")
# ...existing code...