import pandas as pd
import great_expectations as gx
import os
from pprint import pprint

# 1. Verificar que el archivo CSV existe
csv_path = "usuarios.csv"
if not os.path.isfile(csv_path):
    raise FileNotFoundError(f"No se encontró el archivo: {csv_path}")

# 2. Cargar los datos desde el CSV
df = pd.read_csv(csv_path)

# 3. Crear contexto efímero (modo Fluent por defecto en 0.18+)
context = gx.get_context()

# 4. Obtener o crear datasource de tipo pandas con Fluent API
datasource_name = "pandas_datasource"
datasource_exists = any(ds["name"] == datasource_name for ds in context.list_datasources())
if datasource_exists:
    datasource = context.get_datasource(datasource_name)
else:
    datasource = context.sources.add_pandas(name=datasource_name)

# 5. Registrar el DataFrame como un asset (eliminando si ya existe)
asset_name = "usuarios"
if asset_name in [a.name for a in datasource.assets]:
    datasource.delete_asset(asset_name)
asset = datasource.add_dataframe_asset(name=asset_name, dataframe=df)

# 6. Obtener un batch request
batch_request = asset.build_batch_request()

# 7. Crear o actualizar suite de expectativas
suite_name = "usuarios_suite"
context.add_or_update_expectation_suite(expectation_suite_name=suite_name)

# 8. Obtener el validador
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=suite_name
)

# 9. Agregar expectativas
validator.expect_column_to_exist("nombre")
validator.expect_column_values_to_not_be_null("edad")
validator.expect_column_values_to_be_between("edad", min_value=18, max_value=60)
validator.expect_column_values_to_match_regex("correo", r"[^@]+@[^@]+\.[^@]+")

# 10. Guardar la suite
validator.save_expectation_suite(discard_failed_expectations=False)

# 11. Validar los datos
results = validator.validate()

# 12. Mostrar resultados
pprint(results)

# 13. Generar reporte visual
context.build_data_docs()

# 14. Mostrar ruta del HTML
html_path = os.path.abspath(
    os.path.join("great_expectations", "uncommitted", "data_docs", "local_site", "index.html")
)
if os.path.isfile(html_path):
    print("\n✅ ¡Validación completada!")
    print(f"📄 Abre el reporte visual desde:\nfile://{html_path}")
else:
    print("\n⚠️ El reporte visual no se generó correctamente.")