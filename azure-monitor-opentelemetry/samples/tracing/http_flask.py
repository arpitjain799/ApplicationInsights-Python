# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License in the project root for
# license information.
# --------------------------------------------------------------------------
import flask
from azure.monitor.opentelemetry import configure_azure_monitor

# Configure Azure monitor collection telemetry pipeline
configure_azure_monitor(
    connection_string="<your-connection-string>",
    disable_logging=True,
    disable_metrics=True,
    instrumentation_config={
        "flask": {
            "excluded_urls": "http://localhost:8080/ignore",
        }
    },
    tracing_export_interval_ms=15000,
)

app = flask.Flask(__name__)


# Requests sent to the flask application will be automatically captured
@app.route("/")
def test():
    return "Test flask request"


# Exceptions that are raised within the request are automatically captured
@app.route("/exception")
def exception():
    raise Exception("Hit an exception")


# Requests sent to this endpoint will not be tracked due to
# flask_config configuration
@app.route("/ignore")
def ignore():
    return "Request received but not tracked."


if __name__ == "__main__":
    app.run(host="localhost", port=8080)
