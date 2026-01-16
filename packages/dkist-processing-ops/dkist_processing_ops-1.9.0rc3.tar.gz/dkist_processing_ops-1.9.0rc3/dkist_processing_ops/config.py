"""Configurations for the dkist-processing-ops package."""

from dkist_processing_common.config import DKISTProcessingCommonConfiguration


class DKISTProcessingOpsConfigurations(DKISTProcessingCommonConfiguration):
    pass  # nothing custom yet


dkist_processing_ops_configurations = DKISTProcessingOpsConfigurations()
dkist_processing_ops_configurations.log_configurations()
