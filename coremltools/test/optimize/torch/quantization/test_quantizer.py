#  Copyright (c) 2024, Apple Inc. All rights reserved.
#
#  Use of this source code is governed by a BSD-3-clause license that can be
#  found in the LICENSE.txt file or at https://opensource.org/licenses/BSD-3-Clause

from collections import OrderedDict

import cattrs
import pytest
import torch
import torch.ao.quantization
import torch.nn as nn
import torch.nn.intrinsic
import torch.nn.intrinsic.qat
import torch.nn.quantized
import torch.nn.quantized.modules.utils

import coremltools.optimize.torch.quantization.modules.qat_modules as _qat
from coremltools.optimize.torch._utils.metadata_utils import CompressionMetadata, CompressionType
from coremltools.optimize.torch.quantization import (
    LinearQuantizer,
    LinearQuantizerConfig,
    ModuleLinearQuantizerConfig,
    ObserverType,
    QuantizationScheme,
)
from coremltools.optimize.torch.quantization.modules.learnable_fake_quantize import (
    LearnableFakeQuantize,
)


@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
@pytest.mark.parametrize(
    "option_and_value", [
        ("weight_dtype", torch.int32),
        ("activation_dtype", torch.int8),
        ("milestones", [0, 2])
    ]
)
def test_config_illegal_options(algorithm, option_and_value):
    option, value = option_and_value
    with pytest.raises(cattrs.errors.ClassValidationError):
        LinearQuantizerConfig.from_dict({"global_config": {algorithm: algorithm, option: value}})


@pytest.mark.parametrize(
    "config_dict",
    [
        {"module_type_configs": {nn.Linear: {"weight_dtype": torch.quint8}}},
        {"module_type_configs": {nn.ConvTranspose2d: {"weight_dtype": torch.quint8}}},
        {"module_name_configs": {"conv2d": {"weight_dtype": torch.quint8}}},
        {"global_config": {"weight_dtype": torch.quint8, "algorithm": "vanilla"}},
        {"global_config": {"weight_dtype": torch.quint8, "algorithm": "learnable"}},
        {},
    ],
)
def test_linear_quantizer_config_global_config_set(config_dict):
    config = LinearQuantizerConfig.from_dict(config_dict)
    if len(config_dict) == 0:
        assert config.global_config == ModuleLinearQuantizerConfig()
    else:
        keys = ["global_config", "module_type_configs", "module_name_configs"]
        for key in keys:
            if key not in config_dict:
                param_in_config = getattr(config, key)
                assert param_in_config is None or len(param_in_config) == 0
        if "global_config" in config_dict:
            assert config.global_config.weight_dtype == config_dict["global_config"]["weight_dtype"]
            assert config.global_config.algorithm == config_dict["global_config"]["algorithm"]
        if "module_name_configs" in config_dict:
            for key in config_dict["module_name_configs"]:
                assert config.module_name_configs[key].weight_dtype == \
                       config_dict["module_name_configs"][key]["weight_dtype"]
        if "module_type_configs" in config_dict:
            for key in config_dict["module_type_configs"]:
                assert config.module_type_configs[key].weight_dtype == \
                       config_dict["module_type_configs"][key]["weight_dtype"]


@pytest.mark.parametrize(
    "config_dict",
    [
        {
            "global_config": {"quantization_scheme": "affine"},
            "module_name_configs": {"conv1": {"quantization_scheme": "symmetric"}},
        },
        {
            "global_config": {"quantization_scheme": "affine"},
            "module_type_configs": {nn.Linear: {"quantization_scheme": "symmetric"}},
        },
        {
            "global_config": {"quantization_scheme": "affine", "algorithm": "vanilla"},
            "module_name_configs": {
                "conv1": {"quantization_scheme": "symmetric", "algorithm": "vanilla"}
            },
        },
        {
            "global_config": {
                "quantization_scheme": "affine",
                "algorithm": "learnable",
            },
            "module_name_configs": {
                "conv1": {"quantization_scheme": "symmetric", "algorithm": "learnable"}
            },
        },
        {
            "global_config": {"quantization_scheme": "affine"},
            "module_type_configs": {nn.Linear: {"quantization_scheme": "symmetric"}},
        },
        {
            "global_config": {"algorithm": "vanilla"},
            "module_type_configs": {nn.Linear: {"algorithm": "learnable"}},
        },
        {
            "global_config": {"algorithm": "learnable"},
            "module_type_configs": {nn.Linear: {"algorithm": "vanilla"}},
        },
        {
            "module_name_configs": {
                "conv1": {"quantization_scheme": "affine"},
                "conv2": {"quantization_scheme": "symmetric"},
            }
        },
        {
            "module_type_configs": {
                nn.Linear: {"quantization_scheme": "symmetric"},
                "Conv2d": {"quantization_scheme": "affine"},
                "ConvTranspose2d": {"quantization_scheme": "affine"},
            }
        },
        {
            "module_type_configs": {nn.Linear: {"quantization_scheme": "symmetric"}},
            "module_name_configs": {"conv1": {"quantization_scheme": "affine"}},
        },
    ],
)
def test_linear_quantizer_config_failure_modes(config_dict):
    with pytest.raises(Exception):
        LinearQuantizerConfig.from_dict(config_dict)


@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
def test_linear_quantizer_config_different_config_success(algorithm):
    config_dict = {
        "global_config": {"quantization_scheme": "affine", "algorithm": algorithm},
        "module_name_configs": {
            "conv1": {"quantization_scheme": "affine", "algorithm": algorithm},
            "conv2": {"quantization_scheme": "affine", "algorithm": algorithm},
        },
        "module_type_configs": {
            nn.Linear: {"quantization_scheme": "affine", "algorithm": algorithm},
            nn.ConvTranspose2d: {
                "quantization_scheme": "affine",
                "algorithm": algorithm,
            },
        },
    }
    LinearQuantizerConfig.from_dict(config_dict)


@pytest.mark.parametrize(
    "config_dict",
    [
        {
            "global_config": {"quantization_scheme": "affine"},
            "module_name_configs": {
                "conv1": {"quantization_scheme": "affine"},
                "conv2": {"quantization_scheme": "affine"},
            },
            "module_type_configs": {nn.Linear: {"quantization_scheme": "affine"}},
        },
        {
            "global_config": {
                "quantization_scheme": "affine",
                "algorithm": "learnable",
            },
            "module_name_configs": {
                "conv1": {"quantization_scheme": "affine", "algorithm": "learnable"},
                "conv2": {"quantization_scheme": "affine", "algorithm": "learnable"},
            },
            "module_type_configs": {
                nn.Linear: {"quantization_scheme": "affine", "algorithm": "learnable"}
            },
        },
        {
            "module_name_configs": {
                "conv1": {"quantization_scheme": "affine"},
                "conv2": {"quantization_scheme": "affine"},
            }
        },
        {"module_type_configs": {nn.Linear: {"quantization_scheme": "affine"}}},
        {},
    ],
)
def test_linear_quantizer_quantization_scheme_setting(config_dict):
    model = nn.Sequential(OrderedDict({
        'conv': nn.Conv2d(1, 20, (3, 3)),
        'relu': nn.ReLU(),
    }))
    config = LinearQuantizerConfig.from_dict(config_dict)
    quantizer = LinearQuantizer(model, config)

    def_quantization_scheme = ModuleLinearQuantizerConfig().quantization_scheme.value
    quantization_scheme = quantizer._quantization_scheme.value
    if len(config_dict) == 0:
        assert def_quantization_scheme == quantization_scheme
    else:
        assert quantization_scheme == "affine"


@pytest.mark.parametrize(
    "model_config",
    [
        (
            nn.Sequential(
                OrderedDict(
                    {
                        "conv": nn.Conv2d(1, 20, (3, 3)),
                        "relu": nn.ReLU(),
                    }
                )
            ),
            torch.nn.intrinsic.qat.ConvReLU2d,
        ),
        (
            nn.Sequential(
                OrderedDict(
                    {
                        "conv": nn.ConvTranspose2d(1, 20, (3, 3)),
                        "relu": nn.ReLU(),
                    }
                )
            ),
            _qat.ConvTransposeAct2d,
        ),
    ],
)
@pytest.mark.parametrize("quantization_scheme", ["symmetric", "affine"])
@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
def test_activation_defaults(algorithm, quantization_scheme, model_config):

    config = LinearQuantizerConfig.from_dict(
        {
            "global_config": {
                "algorithm": algorithm,
                "quantization_scheme": quantization_scheme,
                "milestones": [0, 2, 3, 3],
            }
        }
    )

    model, model_conv_instance = model_config
    quantizer = LinearQuantizer(model, config)
    model = quantizer.prepare(example_inputs=(torch.randn(1, 1, 28, 28),))

    assert isinstance(model.conv, model_conv_instance)
    assert model.activation_post_process_0.dtype == torch.quint8
    if quantization_scheme == "symmetric":
        assert model.activation_post_process_0.qscheme == torch.per_tensor_symmetric
    else:
        assert model.activation_post_process_0.qscheme == torch.per_tensor_affine
    assert model.activation_post_process_1.dtype == torch.quint8
    assert model.activation_post_process_1.qscheme == torch.per_tensor_affine


@pytest.mark.parametrize(
    "model_config",
    [
        (
            nn.Sequential(
                OrderedDict(
                    {
                        "conv": nn.Conv2d(1, 20, (3, 3)),
                        "bn": nn.BatchNorm2d(20),
                        "relu": nn.ReLU(),
                    }
                )
            ),
            True,
        ),
        (
            nn.Sequential(
                OrderedDict(
                    {
                        "conv": nn.ConvTranspose2d(1, 20, (3, 3)),
                        "bn": nn.BatchNorm2d(20),
                        "relu": nn.ReLU(),
                    }
                )
            ),
            False,
        ),
    ],
)
@pytest.mark.parametrize("quantization_scheme", ["symmetric", "affine"])
@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
def test_linear_quantizer_step_mechanism(algorithm, quantization_scheme, model_config):

    config = LinearQuantizerConfig.from_dict(
        {
            "global_config": {
                "algorithm": algorithm,
                "quantization_scheme": quantization_scheme,
                "milestones": [0, 1, 2, 3],
            }
        }
    )

    model, pytorch_builtin_mod = model_config
    quantizer = LinearQuantizer(model, config)
    model = quantizer.prepare(example_inputs=(torch.randn(1, 1, 28, 28),))

    if pytorch_builtin_mod:
        bn_module_to_check = model.conv
    else:
        bn_module_to_check = model.conv.conv

    assert not model.activation_post_process_0.observer_enabled
    assert not model.activation_post_process_0.fake_quant_enabled
    assert not model.activation_post_process_1.observer_enabled
    assert not model.activation_post_process_1.fake_quant_enabled

    for idx in range(4):
        quantizer.step()
        if idx == 0:
            assert not getattr(bn_module_to_check, "freeze_bn")
            assert model.activation_post_process_0.observer_enabled
            assert not model.activation_post_process_0.fake_quant_enabled
            assert model.activation_post_process_1.observer_enabled
            assert not model.activation_post_process_1.fake_quant_enabled
        if idx == 1:
            assert not getattr(bn_module_to_check, "freeze_bn")
            assert model.activation_post_process_0.observer_enabled
            assert model.activation_post_process_0.fake_quant_enabled
            assert model.activation_post_process_1.observer_enabled
            assert model.activation_post_process_1.fake_quant_enabled
        if idx == 2:
            assert not getattr(bn_module_to_check, "freeze_bn")
            assert not model.activation_post_process_0.observer_enabled
            assert model.activation_post_process_0.fake_quant_enabled
            assert not model.activation_post_process_1.observer_enabled
            assert model.activation_post_process_1.fake_quant_enabled
        if idx == 3:
            assert getattr(bn_module_to_check, "freeze_bn")
            assert not model.activation_post_process_0.observer_enabled
            assert model.activation_post_process_0.fake_quant_enabled
            assert not model.activation_post_process_1.observer_enabled
            assert model.activation_post_process_1.fake_quant_enabled


@pytest.mark.parametrize(
    "model_dict",
    [
        OrderedDict(
            {
                "conv": nn.Conv2d(1, 20, (3, 3)),
                "bn": nn.BatchNorm2d(20),
                "relu": nn.ReLU(),
            }
        ),
        OrderedDict(
            {
                "conv": nn.ConvTranspose2d(1, 20, (3, 3)),
                "bn": nn.BatchNorm2d(20),
                "relu": nn.ReLU(),
            }
        ),
    ],
)
@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
def test_linear_quantizer_preserved_attributes(algorithm, model_dict):
    """
    Test if methods and attributes on the model are preserved by passing
    preserved_attributes to the config.
    """

    class MyModel(nn.Sequential):
        def __init__(self, model_dict):
            super().__init__(model_dict)
            self.conv.weight.data = torch.ones_like(self.conv.weight.data)

        def my_method(self):
            return self.weight + torch.ones_like(self.weight)

        @property
        def weight(self):
            return (
                self.conv.weight
                if hasattr(self.conv, "weight")
                else self.conv.get_submodule("0").weight
            )

    preserved_attrs = ["key_1", "key_2", "my_method", "weight"]

    model = MyModel(model_dict)
    model.key_1 = 5
    model.key_2 = torch.tensor(5)

    config = LinearQuantizerConfig.from_dict(
        {
            "global_config": {
                "algorithm": algorithm,
                "milestones": [0, 3, 4, 5],
            },
            "preserved_attributes": preserved_attrs,
        }
    )
    quantizer_1 = LinearQuantizer(model, LinearQuantizerConfig())
    prepared_model = quantizer_1.prepare(example_inputs=(torch.randn(1, 1, 28, 28),), inplace=False)
    for attr in preserved_attrs:
        assert not hasattr(prepared_model, attr)

    quantizer_2 = LinearQuantizer(model, config)
    prepared_model = quantizer_2.prepare(example_inputs=(torch.randn(1, 1, 28, 28),), inplace=False)
    for attr in preserved_attrs:
        assert hasattr(prepared_model, attr)
    assert torch.all(
        prepared_model.my_method() == 2 * torch.ones_like(prepared_model.conv.weight.data)
    )

    quantizer_2.step()
    prepared_model(torch.randn(2, 1, 28, 28))
    final_model = quantizer_2.finalize()
    for attr in preserved_attrs:
        assert hasattr(final_model, attr)
    assert torch.all(
        final_model.my_method()
        == final_model.weight.data + torch.ones_like(prepared_model.weight.data)
    )


@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
@pytest.mark.parametrize("weight_dtype", ["qint8", "quint8", "qint4", "quint4"])
@pytest.mark.parametrize("weight_per_channel", [True, False])
@pytest.mark.parametrize(
    "quantization_scheme", [QuantizationScheme.symmetric, QuantizationScheme.affine]
)
def test_linear_quantizer_report(
    mnist_model_conv_transpose,
    algorithm,
    weight_dtype,
    weight_per_channel,
    quantization_scheme,
):
    print("\nTESTING REPORT WITH")
    print("ALGORITHM", algorithm)
    print("WEIGHT_DTYPE", weight_dtype)
    print("WEIGHT_PER_CHANNEL", weight_per_channel)
    print("QUANTIZATION_SCHEME", quantization_scheme)

    config = LinearQuantizerConfig.from_dict(
        {
            "global_config": {
                "milestones": [0, 1, 1, 3],
                "algorithm": algorithm,
                "weight_dtype": weight_dtype,
                "weight_per_channel": weight_per_channel,
                "quantization_scheme": quantization_scheme,
            },
            "module_name_configs": {
                "dense2": {
                    "milestones": [0, 1, 1, 3],
                    "activation_dtype": torch.float32,
                    "algorithm": algorithm,
                    "weight_dtype": weight_dtype,
                    "weight_per_channel": weight_per_channel,
                    "quantization_scheme": quantization_scheme,
                }
            },
        }
    )

    quantizer = LinearQuantizer(mnist_model_conv_transpose, config)
    prepared_model = quantizer.prepare(example_inputs=(torch.randn(1, 1, 28, 28),))

    report = quantizer.report()

    print("\nREPORT\n" + str(report))


@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
@pytest.mark.parametrize(
    "dtype",
    [
        pytest.param("qint4", marks=pytest.mark.xfail(reason="rdar://134169158")),
        "qint8",
    ],
)
@pytest.mark.parametrize("scheme", ["symmetric", "affine"])
@pytest.mark.parametrize("conv_transpose", [False, True])
def test_linear_quantizer_compression_metadata(algorithm, dtype, scheme, conv_transpose):
    """
    Test that calling finalize on the module leads to compression metadata being added to the model
    """
    model = nn.Sequential(
        OrderedDict(
            [
                (
                    "conv1",
                    (nn.Conv2d(1, 20, 3) if not conv_transpose else nn.ConvTranspose2d(1, 20, 3)),
                ),
                ("relu", nn.ReLU()),
                ("fc1", nn.Linear(20, 100)),
            ]
        )
    )
    config = LinearQuantizerConfig.from_dict(
        {
            "global_config": {"algorithm": algorithm, "quantization_scheme": scheme},
            "module_name_configs": {
                "conv1": {
                    "algorithm": algorithm,
                    "weight_dtype": dtype,
                    "quantization_scheme": scheme,
                },
                "fc1": None,
            },
        }
    )
    quantizer = LinearQuantizer(model, config)
    quantizer.prepare(inplace=True, example_inputs=(torch.randn(1, 1, 28, 28),))
    for _ in range(4):
        quantizer.step()
    model = quantizer.finalize()

    # Verify metadata version is added to model
    assert "_COREML_/metadata_version" in model.state_dict()

    # Verify compression metadata is added for conv1
    metadata_dict = CompressionMetadata.from_state_dict(model.conv1[0].state_dict())
    assert len(metadata_dict) == 1
    assert "weight" in metadata_dict

    metadata = metadata_dict["weight"]
    assert metadata.compression_type == [CompressionType.quantization.value]
    assert metadata.quantization_n_bits == 4 if dtype == "qint4" else 8
    scale_zero_point_shape = (20, 1) if not conv_transpose else (1, 20)
    assert metadata.quantization_scale.shape == scale_zero_point_shape
    assert metadata.zero_point.shape == scale_zero_point_shape
    if scheme == "symmetric":
        assert torch.all(metadata.zero_point == 0)

    # Verify no compression metadata is added for fc1
    metadata_dict = CompressionMetadata.from_state_dict(model.fc1.state_dict())
    assert len(metadata_dict) == 0


@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
@pytest.mark.parametrize(
    "dtype,n_bits",
    [
        ["qint4", 4],
        ["quint4", 4],
        ["qint8", 8],
        ["quint8", 8],
        [torch.qint8, 8],
        [torch.quint8, 8],
    ],
)
def test_linear_quantizer_config_n_bits(algorithm, dtype, n_bits):
    config = ModuleLinearQuantizerConfig.from_dict(
        {
            "algorithm": algorithm,
            "weight_dtype": dtype,
        }
    )
    assert config.weight_n_bits == n_bits


@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
@pytest.mark.parametrize("weight_dtype", ["qint8", "quint8", "qint4", "quint4"])
@pytest.mark.parametrize("weight_per_channel", [True, False])
@pytest.mark.parametrize(
    "quantization_scheme", [QuantizationScheme.symmetric, QuantizationScheme.affine]
)
def test_linear_quantizer_fq_insert(
    mnist_model_conv_transpose,
    algorithm,
    weight_dtype,
    weight_per_channel,
    quantization_scheme,
):
    print("\nTESTING FAKE QUANTIZE MODULE INSERTION WITH")
    print("ALGORITHM", algorithm)
    print("WEIGHT_DTYPE", weight_dtype)
    print("WEIGHT_PER_CHANNEL", weight_per_channel)
    print("QUANTIZATION_SCHEME", quantization_scheme)

    config = LinearQuantizerConfig.from_dict(
        {
            "global_config": {
                "milestones": [0, 1, 1, 3],
                "algorithm": algorithm,
                "weight_dtype": weight_dtype,
                "weight_per_channel": weight_per_channel,
                "quantization_scheme": quantization_scheme,
            },
            "module_name_configs": {
                "dense2": {
                    "milestones": [0, 1, 1, 3],
                    "activation_dtype": torch.float32,
                    "algorithm": algorithm,
                    "weight_dtype": weight_dtype,
                    "weight_per_channel": weight_per_channel,
                    "quantization_scheme": quantization_scheme,
                }
            },
        }
    )

    quantizer = LinearQuantizer(mnist_model_conv_transpose, config)
    prepared_model = quantizer.prepare(example_inputs=(torch.randn(1, 1, 28, 28),))

    for name, module in prepared_model.named_modules(remove_duplicate=True):
        if hasattr(module, "weight_fake_quant") and module.weight_fake_quant is not None:
            if algorithm == "vanilla":
                assert isinstance(module.weight_fake_quant, torch.ao.quantization.FakeQuantize)
            else:
                assert algorithm == "learnable"
                assert isinstance(module.weight_fake_quant, LearnableFakeQuantize)
        elif (
            not name.endswith(".weight_fake_quant")
            and isinstance(module, (torch.ao.quantization.FakeQuantize, LearnableFakeQuantize))
            and hasattr(module, "activation_post_process")
            and module.activation_post_process is not None
        ):
            if algorithm == "vanilla":
                assert isinstance(module, torch.ao.quantization.FakeQuantize)
            else:
                assert algorithm == "learnable"
                assert isinstance(module, LearnableFakeQuantize)


@pytest.mark.parametrize("algorithm", ["vanilla", "learnable"])
@pytest.mark.parametrize(
    "test_config, observer_type, expected_synchronize",
    [
        ("default", ObserverType.ema_min_max, True),
        ("disable_sync", ObserverType.ema_min_max, False),
        ("disable_then_enable_sync", ObserverType.ema_min_max, True),
        ("disable_then_enable_sync", ObserverType.moving_average_min_max, None),
    ],
)
def test_linear_quantizer_observer_sync(
    mnist_model_conv_transpose,
    algorithm,
    test_config,
    observer_type,
    expected_synchronize,
):
    print("\nTESTING OBSERVER SYNC WITH")
    print("ALGORITHM", algorithm)
    print("TEST_CONFIG", test_config)
    print("OBSERVER_TYPE", observer_type)

    config = LinearQuantizerConfig.from_dict(
        {
            "global_config": {
                "milestones": [0, 1, 1, 3],
                "algorithm": algorithm,
                "weight_dtype": torch.qint8,
                "weight_per_channel": True,
                "weight_observer": observer_type,
                "activation_observer": observer_type,
            },
            "module_name_configs": {
                "dense2": {
                    "milestones": [0, 1, 1, 3],
                    "activation_dtype": torch.float32,
                    "algorithm": algorithm,
                    "weight_dtype": torch.qint8,
                    "weight_per_channel": True,
                    "weight_observer": observer_type,
                }
            },
        }
    )

    quantizer = LinearQuantizer(mnist_model_conv_transpose, config)
    prepared_model = quantizer.prepare(example_inputs=(torch.randn(1, 1, 28, 28),))

    if test_config == "disable_sync" or test_config == "disable_then_enable_sync":
        quantizer.disable_observer_sync()
    if test_config == "disable_then_enable_sync":
        quantizer.enable_observer_sync()

    if expected_synchronize is not None:
        for name, module in prepared_model.named_modules(remove_duplicate=True):
            if hasattr(module, "weight_fake_quant") and module.weight_fake_quant is not None:
                assert (
                    module.weight_fake_quant.activation_post_process.synchronize
                    == expected_synchronize
                )
            elif (
                not name.endswith(".weight_fake_quant")
                and isinstance(module, (torch.ao.quantization.FakeQuantize, LearnableFakeQuantize))
                and hasattr(module, "activation_post_process")
                and module.activation_post_process is not None
            ):
                assert module.activation_post_process.synchronize == expected_synchronize
