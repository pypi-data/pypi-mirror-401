from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from pandas import DataFrame

from classiq.interface.backend.backend_preferences import (
    AliceBobBackendPreferences,
    AQTBackendPreferences,
    AwsBackendPreferences,
    AzureBackendPreferences,
    AzureCredential,
    BackendPreferencesTypes,
    ClassiqBackendPreferences,
    GCPBackendPreferences,
    IBMBackendPreferences,
    IntelBackendPreferences,
    IonqBackendPreferences,
)
from classiq.interface.backend.provider_config.provider_config import ProviderConfig
from classiq.interface.backend.provider_config.providers.alice_bob import AliceBobConfig
from classiq.interface.backend.provider_config.providers.aqt import AQTConfig
from classiq.interface.backend.provider_config.providers.azure import AzureConfig
from classiq.interface.backend.provider_config.providers.braket import BraketConfig
from classiq.interface.backend.provider_config.providers.ibm import IBMConfig
from classiq.interface.backend.provider_config.providers.ionq import IonQConfig
from classiq.interface.backend.quantum_backend_providers import (
    ClassiqNvidiaBackendNames,
    ClassiqSimulatorBackendNames,
)
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.model.preferences import create_random_seed
from classiq.interface.generator.model.preferences.preferences import (
    TranspilationOption,
)
from classiq.interface.hardware import Provider

from classiq import (
    ExecutionParams,
    QuantumProgram,
)
from classiq.execution import ExecutionSession
from classiq.execution.functions._logging import _logger
from classiq.execution.functions.constants import Verbosity
from classiq.execution.functions.parse_provider_backend import (
    _PROVIDER_TO_CANONICAL_NAME,
    _parse_provider_backend,
)


@dataclass
class _ProviderConfigToBackendPrefSpec:
    backend_preferences_class: type[BackendPreferencesTypes]
    config_class: type[ProviderConfig] | None = None
    # Maps the config dict (either passed in directly or dumped from config class) to a
    # dict that we can load into the given BackendPreferences class. This is in case
    # we need to rename fields or change structure.
    config_dict_to_backend_preferences_dict: (
        Callable[[dict[str, Any]], dict[str, Any]] | None
    ) = None
    # Maps from SDK names to names our backend recognizes, raising a useful error
    # if the name is unrecognized.
    backend_name_mapper: Callable[[str], str] | None = None


def _classiq_backend_name_mapper(backend_name: str) -> str:
    backend_name = backend_name.lower()
    if backend_name in [
        ClassiqSimulatorBackendNames.SIMULATOR,
        ClassiqSimulatorBackendNames.SIMULATOR_MATRIX_PRODUCT_STATE,
        ClassiqSimulatorBackendNames.SIMULATOR_DENSITY_MATRIX,
    ]:
        return backend_name
    if backend_name == "nvidia_simulator":
        return ClassiqNvidiaBackendNames.SIMULATOR
    if any(keyword in backend_name for keyword in ["gpu", "nvidia"]):
        suggested_backend_name = "nvidia_simulator"
    else:
        suggested_backend_name = "simulator"
    raise ValueError(
        f"Unsupported backend name {backend_name}. Did you mean '{suggested_backend_name}'?"
    )


def _ibm_backend_name_mapper(backend_name: str) -> str:
    ibm_prefix: Literal["ibm_"] = "ibm_"
    backend_name = backend_name.lower()
    if backend_name.startswith(ibm_prefix):
        backend_name_no_prefix = backend_name.removeprefix(ibm_prefix)
        raise ValueError(
            f"IBM backend names shouldn't start with ibm_. Try 'ibm/{backend_name_no_prefix}'."
        )
    return ibm_prefix + backend_name


def _azure_config_dict_to_backend_preferences_dict(
    config_dict: dict[str, Any],
) -> dict[str, Any]:
    if "location" not in config_dict:
        raise ValueError("Azure config must have 'location' property")
    credentials = None
    if all(
        config_dict.get(key) is not None
        for key in ["tenant_id", "client_id", "client_secret", "resource_id"]
    ):
        credentials = AzureCredential.model_validate(
            {
                "tenant_id": config_dict["tenant_id"],
                "client_id": config_dict["client_id"],
                "client_secret": config_dict["client_secret"],
                "resource_id": config_dict["resource_id"],
            }
        )
    return {
        "location": config_dict["location"],
        "credentials": credentials,
        "ionq_error_mitigation_flag": config_dict.get("ionq_error_mitigation"),
    }


def _braket_config_dict_to_backend_preferences_dict(
    config_dict: dict[str, Any],
) -> dict[str, Any]:
    config_dict["aws_access_key_id"] = config_dict.pop("braket_access_key_id", None)
    config_dict["aws_secret_access_key"] = config_dict.pop(
        "braket_secret_access_key", None
    )
    return config_dict


_PROVIDER_CONFIG_TO_BACKEND_PREFERENCES_SPEC = {
    Provider.CLASSIQ: _ProviderConfigToBackendPrefSpec(
        backend_preferences_class=ClassiqBackendPreferences,
        backend_name_mapper=_classiq_backend_name_mapper,
    ),
    Provider.GOOGLE: _ProviderConfigToBackendPrefSpec(
        backend_preferences_class=GCPBackendPreferences
    ),
    Provider.INTEL: _ProviderConfigToBackendPrefSpec(
        backend_preferences_class=IntelBackendPreferences
    ),
    Provider.IBM_QUANTUM: _ProviderConfigToBackendPrefSpec(
        backend_preferences_class=IBMBackendPreferences,
        config_class=IBMConfig,
        backend_name_mapper=_ibm_backend_name_mapper,
    ),
    Provider.AMAZON_BRAKET: _ProviderConfigToBackendPrefSpec(
        backend_preferences_class=AwsBackendPreferences,
        config_dict_to_backend_preferences_dict=_braket_config_dict_to_backend_preferences_dict,
        config_class=BraketConfig,
    ),
    Provider.IONQ: _ProviderConfigToBackendPrefSpec(
        backend_preferences_class=IonqBackendPreferences,
        config_class=IonQConfig,
    ),
    Provider.ALICE_AND_BOB: _ProviderConfigToBackendPrefSpec(
        backend_preferences_class=AliceBobBackendPreferences,
        config_class=AliceBobConfig,
    ),
    Provider.AQT: _ProviderConfigToBackendPrefSpec(
        backend_preferences_class=AQTBackendPreferences,
        config_class=AQTConfig,
    ),
    Provider.AZURE_QUANTUM: _ProviderConfigToBackendPrefSpec(
        backend_preferences_class=AzureBackendPreferences,
        config_dict_to_backend_preferences_dict=_azure_config_dict_to_backend_preferences_dict,
        config_class=AzureConfig,
    ),
}


def _get_backend_preferences_from_specifier(
    backend_spec: str, config: dict[str, Any] | ProviderConfig
) -> BackendPreferencesTypes:
    provider, backend_name = _parse_provider_backend(backend_spec)

    if provider not in _PROVIDER_CONFIG_TO_BACKEND_PREFERENCES_SPEC:
        raise NotImplementedError(
            f"Unsupported provider '{_PROVIDER_TO_CANONICAL_NAME.get(provider) or provider}'"
        )

    provider_spec = _PROVIDER_CONFIG_TO_BACKEND_PREFERENCES_SPEC[provider]
    if isinstance(config, ProviderConfig):
        if provider_spec.config_class is None:
            raise ValueError(
                f"This provider does not support any ProviderConfig classes. Received '{config.__class__.__name__}'"
            )
        if not isinstance(config, provider_spec.config_class):
            raise ValueError(
                f"{_PROVIDER_TO_CANONICAL_NAME[provider]} devices require {provider_spec.config_class.__name__}, got {config.__class__.__name__}"
            )
        config_dict = config.model_dump()
    else:
        config_dict = config
    if provider_spec.backend_name_mapper is not None:
        backend_name = provider_spec.backend_name_mapper(backend_name)

    if provider_spec.config_dict_to_backend_preferences_dict is not None:
        config_dict = provider_spec.config_dict_to_backend_preferences_dict(config_dict)

    config_dict["backend_name"] = backend_name
    return provider_spec.backend_preferences_class.model_validate(config_dict)


_DEFAULT_BACKEND_NAME = "simulator"


def _new_sample(
    qprog: QuantumProgram,
    backend: str | None = None,
    *,
    parameters: ExecutionParams | None = None,
    config: dict[str, Any] | ProviderConfig | None = None,
    num_shots: int | None = None,
    random_seed: int | None = None,
    transpilation_option: TranspilationOption = TranspilationOption.DECOMPOSE,
    verbosity: Verbosity = Verbosity.INFO,
) -> "DataFrame":
    """
    Sample a quantum program.

    Args:
        qprog: The quantum program
        backend: The device (hardware or simulator) on which to run the quantum program. Specified as "provider/device_id"
        parameters: The classical parameters for the quantum program
        config: Provider-specific configuration, such as api keys
        num_shots: The number of times to sample
        random_seed: The random seed used for transpilation and simulation
        transpilation_option: Advanced configuration for hardware-specific transpilation
        verbosity: What level of information should be logged

    Returns: A dataframe containing the histogram
    """
    if num_shots is not None and num_shots < 1:
        raise ValueError(f"Argument num_shots must be greater than 0, got {num_shots}")
    if config is None:
        config = {}
    if backend is None:
        backend = _DEFAULT_BACKEND_NAME
    backend_preferences = _get_backend_preferences_from_specifier(backend, config)
    ep = ExecutionPreferences(
        backend_preferences=backend_preferences,
        num_shots=num_shots,
        random_seed=create_random_seed() if random_seed is None else random_seed,
        transpile_to_hardware=transpilation_option,
    )
    if verbosity != Verbosity.QUIET:
        _logger.info(f"Submitting job to {backend}")
    with ExecutionSession(qprog, execution_preferences=ep) as session:
        job = session.submit_sample(parameters)
        if verbosity != Verbosity.QUIET:
            _logger.info(f"Job id: {job.id}")
        result = job.get_sample_result()

    df = result.dataframe
    return df
