import great_expectations as gx
import os

def validar_dataframe(df):
    # Crear el contexto
    context = gx.get_context()

    # Agregar un datasource para Pandas
    datasource = context.sources.add_pandas(name="mi_datasource")

    # Agregar el DataFrame como un DataAsset
    asset = datasource.add_dataframe_asset(name="usuarios", dataframe=df)

    # Crear la suite usando la nueva forma
    suite = context.create_expectation_suite(expectation_suite_name="usuarios_suite")

    # Crear un validador para agregar expectativas
    validator = asset.build_batch_request().get_validator(expectation_suite=suite)

    # Añadir expectativas
    validator.expect_column_to_exist("nombre")
    validator.expect_column_values_to_not_be_null("edad")
    validator.expect_column_values_to_be_between("edad", min_value=18, max_value=60)
    validator.expect_column_values_to_match_regex("correo", r"[^@]+@[^@]+\.[^@]+")

    # Guardar la suite de expectativas
    validator.save_expectation_suite()

    # Crear y ejecutar el checkpoint
    checkpoint = context.add_or_update_checkpoint(
        name="usuarios_checkpoint",
        validations=[
            {
                "batch_request": asset.build_batch_request(),
                "expectation_suite_name": "usuarios_suite",
            }
        ]
    )

    results = checkpoint.run()
    context.build_data_docs()

    # Ruta al HTML del reporte
    html_path = os.path.join(
        context.root_directory,
        "uncommitted", "data_docs", "local_site", "index.html"
    )

    return results, html_path
