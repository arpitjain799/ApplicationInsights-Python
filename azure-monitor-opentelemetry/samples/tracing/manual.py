# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License in the project root for
# license information.
# --------------------------------------------------------------------------
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import create_engine, text

configure_azure_monitor(
    connection_string="<your-connection-string>",
    tracing_export_interval_ms=15000,
    disable_logging=True,
    disable_metrics=True,
)

engine = create_engine("sqlite:///:memory:")
# SQLAlchemy instrumentation is not officially supported by this package
# However, you can use the OpenTelemetry instument method manually in
# conjunction with configure_azure_monitor
SQLAlchemyInstrumentor().instrument(
    engine=engine,
)

# Database calls using the SqlAlchemy library will be automatically captured
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

input()
