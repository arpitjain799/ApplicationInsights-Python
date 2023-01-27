# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from unittest.mock import Mock, call, patch

from azure.monitor.opentelemetry.distro import (
    _SUPPORTED_INSTRUMENTED_LIBRARIES,
    _get_resource,
    _setup_instrumentations,
    _setup_logging,
    _setup_tracing,
    configure_azure_monitor,
)
from opentelemetry.semconv.resource import ResourceAttributes


class TestConfigure(unittest.TestCase):
    @patch(
        "azure.monitor.opentelemetry.distro._setup_instrumentations",
    )
    @patch(
        "azure.monitor.opentelemetry.distro._setup_logging",
    )
    @patch(
        "azure.monitor.opentelemetry.distro._setup_tracing",
    )
    @patch(
        "azure.monitor.opentelemetry.distro._get_resource",
    )
    def test_configure_azure_monitor(
        self,
        resource_mock,
        tracing_mock,
        logging_mock,
        instrumentation_mock,
    ):
        kwargs = {
            "connection_string": "test_cs",
            "disable_logging": False,
            "disable_tracing": False,
            "logging_export_interval_millis": 10000,
            "logging_level": "test_logging_level",
            "logger_name": "test_logger_name",
            "service_name": "test_service_name",
            "service_namespace": "test_namespace",
            "service_instance_id": "test_id",
            "sampling_ratio": 0.5,
            "tracing_export_interval_millis": 15000,
        }
        resource_init_mock = Mock()
        resource_mock.return_value = resource_init_mock
        configure_azure_monitor(**kwargs)
        resource_mock.assert_called_once_with(kwargs)
        tracing_mock.assert_called_once_with(resource_init_mock, kwargs)
        logging_mock.assert_called_once_with(resource_init_mock, kwargs)
        instrumentation_mock.assert_called_once_with(kwargs)

    @patch(
        "azure.monitor.opentelemetry.distro._setup_instrumentations",
    )
    @patch(
        "azure.monitor.opentelemetry.distro._setup_logging",
    )
    @patch(
        "azure.monitor.opentelemetry.distro._setup_tracing",
    )
    @patch(
        "azure.monitor.opentelemetry.distro._get_resource",
    )
    def test_configure_azure_monitor_disable_tracing(
        self,
        resource_mock,
        tracing_mock,
        logging_mock,
        instrumentation_mock,
    ):
        kwargs = {
            "connection_string": "test_cs",
            "disable_logging": False,
            "disable_tracing": True,
            "logging_export_interval_millis": 10000,
            "logging_level": "test_logging_level",
            "logger_name": "test_logger_name",
            "service_name": "test_service_name",
            "service_namespace": "test_namespace",
            "service_instance_id": "test_id",
            "sampling_ratio": 0.5,
            "tracing_export_interval_millis": 15000,
        }
        resource_init_mock = Mock()
        resource_mock.return_value = resource_init_mock
        configure_azure_monitor(**kwargs)
        resource_mock.assert_called_once_with(kwargs)
        tracing_mock.assert_not_called()
        logging_mock.assert_called_once_with(resource_init_mock, kwargs)
        instrumentation_mock.assert_called_once_with(kwargs)

    @patch(
        "azure.monitor.opentelemetry.distro._setup_instrumentations",
    )
    @patch(
        "azure.monitor.opentelemetry.distro._setup_logging",
    )
    @patch(
        "azure.monitor.opentelemetry.distro._setup_tracing",
    )
    @patch(
        "azure.monitor.opentelemetry.distro._get_resource",
    )
    def test_configure_azure_monitor_disable_logging(
        self,
        resource_mock,
        tracing_mock,
        logging_mock,
        instrumentation_mock,
    ):
        kwargs = {
            "connection_string": "test_cs",
            "disable_logging": True,
            "disable_tracing": False,
            "logging_export_interval_millis": 10000,
            "logging_level": "test_logging_level",
            "logger_name": "test_logger_name",
            "service_name": "test_service_name",
            "service_namespace": "test_namespace",
            "service_instance_id": "test_id",
            "sampling_ratio": 0.5,
            "tracing_export_interval_millis": 15000,
        }
        resource_init_mock = Mock()
        resource_mock.return_value = resource_init_mock
        configure_azure_monitor(**kwargs)
        resource_mock.assert_called_once_with(kwargs)
        tracing_mock.assert_called_once_with(resource_init_mock, kwargs)
        logging_mock.assert_not_called()
        instrumentation_mock.assert_called_once_with(kwargs)

    @patch(
        "azure.monitor.opentelemetry.distro.Resource",
    )
    def test_get_resource(self, resource_mock):
        configuration = {
            "service_name": "test_service_name",
            "service_namespace": "test_namespace",
            "service_instance_id": "test_id",
        }
        _get_resource(configuration)
        resource_mock.create.assert_called_once_with(
            {
                ResourceAttributes.SERVICE_NAME: "test_service_name",
                ResourceAttributes.SERVICE_NAMESPACE: "test_namespace",
                ResourceAttributes.SERVICE_INSTANCE_ID: "test_id",
            }
        )

    @patch(
        "azure.monitor.opentelemetry.distro.BatchSpanProcessor",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.AzureMonitorTraceExporter",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.get_tracer_provider",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.set_tracer_provider",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.TracerProvider",
        autospec=True,
    )
    @patch(
        "azure.monitor.opentelemetry.distro.ApplicationInsightsSampler",
    )
    def test_setup_tracing(
        self,
        sampler_mock,
        tp_mock,
        set_tracer_provider_mock,
        get_tracer_provider_mock,
        trace_exporter_mock,
        bsp_mock,
    ):
        resource_mock = Mock()
        sampler_init_mock = Mock()
        sampler_mock.return_value = sampler_init_mock
        tp_init_mock = Mock()
        tp_mock.return_value = tp_init_mock
        get_tracer_provider_mock.return_value = tp_init_mock
        trace_exp_init_mock = Mock()
        trace_exporter_mock.return_value = trace_exp_init_mock
        bsp_init_mock = Mock()
        bsp_mock.return_value = bsp_init_mock

        configurations = {
            "connection_string": "test_cs",
            "disable_tracing": False,
            "sampling_ratio": 0.5,
            "tracing_export_interval_millis": 15000,
        }
        _setup_tracing(resource_mock, configurations)
        sampler_mock.assert_called_once_with(sampling_ratio=0.5)
        tp_mock.assert_called_once_with(
            resource=resource_mock,
            sampler=sampler_init_mock,
        )
        set_tracer_provider_mock.assert_called_once_with(tp_init_mock)
        get_tracer_provider_mock.assert_called()
        trace_exporter_mock.assert_called_once()
        bsp_mock.assert_called_once_with(
            trace_exp_init_mock, export_timeout_millis=15000
        )
        tp_init_mock.add_span_processor(bsp_init_mock)

    @patch(
        "azure.monitor.opentelemetry.distro.getLogger",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.LoggingHandler",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.BatchLogRecordProcessor",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.AzureMonitorLogExporter",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.get_logger_provider",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.set_logger_provider",
    )
    @patch(
        "azure.monitor.opentelemetry.distro.LoggerProvider",
        autospec=True,
    )
    def test_setup_logging(
        self,
        lp_mock,
        set_logger_provider_mock,
        get_logger_provider_mock,
        log_exporter_mock,
        blrp_mock,
        logging_handler_mock,
        get_logger_mock,
    ):
        resource_mock = Mock()

        lp_init_mock = Mock()
        lp_mock.return_value = lp_init_mock
        get_logger_provider_mock.return_value = lp_init_mock
        log_exp_init_mock = Mock()
        log_exporter_mock.return_value = log_exp_init_mock
        blrp_init_mock = Mock()
        blrp_mock.return_value = blrp_init_mock
        logging_handler_init_mock = Mock()
        logging_handler_mock.return_value = logging_handler_init_mock
        logger_mock = Mock()
        get_logger_mock.return_value = logger_mock

        configurations = {
            "connection_string": "test_cs",
            "disable_logging": False,
            "logging_export_interval_millis": 10000,
            "logging_level": "test_logging_level",
            "logger_name": "test_logger_name",
        }
        _setup_logging(resource_mock, configurations)

        lp_mock.assert_called_once_with(resource=resource_mock)
        set_logger_provider_mock.assert_called_once_with(lp_init_mock)
        get_logger_provider_mock.assert_called()
        log_exporter_mock.assert_called_once()
        blrp_mock.assert_called_once_with(
            log_exp_init_mock, export_timeout_millis=10000
        )
        lp_init_mock.add_log_record_processor.assert_called_once_with(
            blrp_init_mock
        )
        logging_handler_mock.assert_called_once_with(
            level="test_logging_level", logger_provider=lp_init_mock
        )
        get_logger_mock.assert_called_once_with("test_logger_name")
        logger_mock.addHandler.assert_called_once_with(
            logging_handler_init_mock
        )

    @patch("azure.monitor.opentelemetry.distro.getattr")
    def test_setup_instrumentations(
        self,
        getattr_mock,
    ):
        for lib_name in _SUPPORTED_INSTRUMENTED_LIBRARIES:
            with patch("importlib.import_module") as import_module_mock:
                configurations = {"instrumentations": [lib_name]}
                instrument_mock = Mock()
                instrumentor_mock = Mock()
                instrumentor_mock.return_value = instrument_mock
                getattr_mock.return_value = instrumentor_mock
                _setup_instrumentations(configurations)
                self.assertEqual(import_module_mock.call_count, 2)
                instr_lib_name = "opentelemetry.instrumentation." + lib_name
                import_module_mock.assert_has_calls(
                    [call(lib_name), call(instr_lib_name)]
                )
                instrumentor_mock.assert_called_once()
                instrument_mock.instrument.assert_called_once()

    @patch("azure.monitor.opentelemetry.distro.getattr")
    def test_setup_instrumentations_lib_not_found(
        self,
        getattr_mock,
    ):
        with patch("importlib.import_module") as import_module_mock:
            configurations = {"instrumentations": ["non_supported_lib"]}
            instrument_mock = Mock()
            instrumentor_mock = Mock()
            instrumentor_mock.return_value = instrument_mock
            getattr_mock.return_value = instrumentor_mock
            _setup_instrumentations(configurations)
            import_module_mock.assert_not_called()
            instrumentor_mock.assert_not_called()
            instrument_mock.instrument.assert_not_called()

    @patch("azure.monitor.opentelemetry.distro.getattr")
    def test_setup_instrumentations_import_lib_failed(
        self,
        getattr_mock,
    ):
        for lib_name in _SUPPORTED_INSTRUMENTED_LIBRARIES:
            with patch(
                "importlib.import_module", side_effect=ImportError()
            ) as import_module_mock:
                configurations = {"instrumentations": [lib_name]}
                instrument_mock = Mock()
                instrumentor_mock = Mock()
                instrumentor_mock.return_value = instrument_mock
                getattr_mock.return_value = instrumentor_mock
                _setup_instrumentations(configurations)
                import_module_mock.assert_called_once()
                instrumentor_mock.assert_not_called()
                instrument_mock.instrument.assert_not_called()

    @patch("azure.monitor.opentelemetry.distro.getattr")
    def test_setup_instrumentations_import_instr_failed(
        self,
        getattr_mock,
    ):
        for lib_name in _SUPPORTED_INSTRUMENTED_LIBRARIES:
            with patch("importlib.import_module") as import_module_mock:
                configurations = {"instrumentations": [lib_name]}
                instrument_mock = Mock()
                instrumentor_mock = Mock()
                instrumentor_mock.return_value = instrument_mock
                getattr_mock.return_value = instrumentor_mock
                import_module_mock.side_effect = [None, ImportError()]
                _setup_instrumentations(configurations)
                instr_lib_name = "opentelemetry.instrumentation." + lib_name
                import_module_mock.assert_has_calls(
                    [call(lib_name), call(instr_lib_name)]
                )
                instrumentor_mock.assert_not_called()
                instrument_mock.instrument.assert_not_called()

    @patch("azure.monitor.opentelemetry.distro.getattr")
    def test_setup_instrumentations_failed_general(
        self,
        getattr_mock,
    ):
        for lib_name in _SUPPORTED_INSTRUMENTED_LIBRARIES:
            with patch("importlib.import_module") as import_module_mock:
                configurations = {"instrumentations": [lib_name]}
                instrument_mock = Mock()
                instrumentor_mock = Mock()
                instrumentor_mock.return_value = instrument_mock
                getattr_mock.side_effect = Exception()
                _setup_instrumentations(configurations)
                self.assertEqual(import_module_mock.call_count, 2)
                instr_lib_name = "opentelemetry.instrumentation." + lib_name
                import_module_mock.assert_has_calls(
                    [call(lib_name), call(instr_lib_name)]
                )
                instrumentor_mock.assert_not_called()
                instrument_mock.instrument.assert_not_called()
