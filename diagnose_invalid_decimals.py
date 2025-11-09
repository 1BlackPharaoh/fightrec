# ...existing code...
import os, decimal
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fightrec.settings")
import django
django.setup()

from django.apps import apps
from django.db.models import DecimalField
from django.db import connection

bad = []

for model in apps.get_models():
    for field in model._meta.get_fields():
        if isinstance(field, DecimalField):
            pk_name = model._meta.pk.name
            table = model._meta.db_table
            col = getattr(field, 'column', field.name)
            # use raw SQL to avoid Django/sqlite decimal converters
            sql = f'SELECT "{pk_name}", "{col}" FROM "{table}";'
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
            except Exception as e:
                # could be permissions/no table etc; skip and record
                bad.append((table, model.__name__, pk_name, None, col, None, f"SQL error: {e!r}"))
                continue

            for pk, val in rows:
                if val is None:
                    continue
                try:
                    decimal.Decimal(str(val))
                except Exception as e:
                    bad.append((table, model.__name__, pk_name, pk, col, val, repr(e)))

if not bad:
    print("No invalid Decimal values found.")
else:
    print("Invalid Decimal values found:\n")
    for table, model_name, pk_name, pk, col, val, err in bad:
        print(f"Table: {table}  Model: {model_name}  {pk_name}={pk}  Column: {col}  Value: {val!r}  Error: {err}")
        pk_literal = f"'{pk}'" if isinstance(pk, str) else str(pk) if pk is not None else "<unknown_pk>"
        print(f"  Suggested sqlite SQL: UPDATE {table} SET {col}=NULL WHERE {pk_name}={pk_literal};")
        print()
# ...existing code...