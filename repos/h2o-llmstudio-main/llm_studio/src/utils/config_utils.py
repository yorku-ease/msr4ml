import dataclasses
import importlib
from types import ModuleType
from typing import Any, Dict, List, Type

import yaml

from llm_studio.python_configs.text_causal_language_modeling_config import (
    ConfigNLPAugmentation,
    ConfigNLPCausalLMArchitecture,
    ConfigNLPCausalLMDataset,
    ConfigNLPCausalLMEnvironment,
    ConfigNLPCausalLMLogging,
    ConfigNLPCausalLMPrediction,
    ConfigNLPCausalLMTokenizer,
    ConfigNLPCausalLMTraining,
    ConfigProblemBase,
)
from llm_studio.src.utils.modeling_utils import generate_experiment_name
from llm_studio.src.utils.type_annotations import KNOWN_TYPE_ANNOTATIONS


def rreload(module):
    """Recursively reload modules.

    Args:
        module: module to reload
    """

    for attribute_name in dir(module):
        if "Config" in attribute_name:
            attribute1 = getattr(module, attribute_name)
            for attribute_name in dir(attribute1):
                attribute2 = getattr(attribute1, attribute_name)
                if type(attribute2) is ModuleType:
                    importlib.reload(attribute2)


def _load_cls(module_path: str, cls_name: str) -> Any:
    """Loads the python class.

    Args:
        module_path: path to the module
        cls_name: name of the class

    Returns:
        Loaded python class
    """

    module_path_fixed = module_path
    if module_path_fixed.endswith(".py"):
        module_path_fixed = module_path_fixed[:-3]
    module_path_fixed = module_path_fixed.replace("/", ".")

    module = importlib.import_module(module_path_fixed)
    module = importlib.reload(module)
    rreload(module)
    module = importlib.reload(module)

    assert hasattr(module, cls_name), "{} file should contain {} class".format(
        module_path, cls_name
    )

    cls = getattr(module, cls_name)

    return cls


def load_config_py(config_path: str, config_name: str = "Config"):
    """Loads the config class.

    Args:
        config_path: path to the config file
        config_name: name of the config class

    Returns:
        Loaded config class
    """

    return _load_cls(config_path, config_name)()


def _get_type_annotation_error(v: Any, type_annotation: Type) -> ValueError:
    return ValueError(
        f"Cannot show {v}: not a dataclass"
        f" and {type_annotation} is not a known type annotation."
    )


def convert_cfg_to_nested_dictionary(cfg: ConfigProblemBase) -> dict:
    """Returns a grouped config settings dict for a given configuration

    Args:
        cfg: configuration
        q: Q

    Returns:
        Dict of configuration settings
    """

    cfg_dict = cfg.__dict__
    type_annotations = cfg.get_annotations()
    cfg_dict = {key: cfg_dict[key] for key in cfg._get_order()}

    grouped_cfg_dict = {}

    for k, v in cfg_dict.items():
        if k.startswith("_"):
            continue

        if any([x in k for x in ["api", "secret"]]):
            raise AssertionError(
                "Config item must not contain the word 'api' or 'secret'"
            )

        type_annotation = type_annotations[k]

        if type_annotation in KNOWN_TYPE_ANNOTATIONS:
            grouped_cfg_dict.update({k: v})
        elif dataclasses.is_dataclass(v):
            group_items = parse_cfg_dataclass(cfg=v)
            group_items = {
                k: list(v) if isinstance(v, tuple) else v
                for d in group_items
                for k, v in d.items()
            }
            grouped_cfg_dict.update({k: group_items})
        else:
            raise _get_type_annotation_error(v, type_annotations[k])

    return grouped_cfg_dict


def get_parent_element(cfg: ConfigProblemBase):
    if hasattr(cfg, "_parent_experiment") and cfg._parent_experiment != "":
        key = "Parent Experiment"
        value = cfg._parent_experiment
        return {key: value}

    return None


def parse_cfg_dataclass(cfg: ConfigProblemBase) -> List[Dict]:
    """Returns all single config settings for a given configuration

    Args:
        cfg: configuration
    """

    items = []

    parent_element = get_parent_element(cfg)
    if parent_element:
        items.append(parent_element)

    cfg_dict = cfg.__dict__
    type_annotations = cfg.get_annotations()
    cfg_dict = {key: cfg_dict[key] for key in cfg._get_order()}

    for k, v in cfg_dict.items():
        if k.startswith("_"):
            continue

        if any([x in k for x in ["api"]]):
            continue

        type_annotation = type_annotations[k]

        if type_annotation in KNOWN_TYPE_ANNOTATIONS:
            if type_annotation == float:
                v = float(v)
            t = [{k: v}]
        elif dataclasses.is_dataclass(v):
            elements_group = parse_cfg_dataclass(cfg=v)
            t = elements_group
        else:
            continue

        items += t

    return items


def save_config_yaml(path: str, cfg: ConfigProblemBase) -> None:
    """Saves config as yaml file

    Args:
        path: path of file to save to
        cfg: config to save
    """
    cfg_dict = convert_cfg_to_nested_dictionary(cfg)
    cfg_dict["experiment_name"] = cfg.experiment_name
    cfg_dict["output_directory"] = cfg.output_directory
    cfg_dict["llm_backbone"] = cfg.llm_backbone
    cfg_dict["problem_type"] = "text_causal_language_modeling"
    with open(path, "w") as fp:
        yaml.dump(cfg_dict, fp, indent=4)


def load_config_yaml(path: str) -> ConfigProblemBase:
    """Loads config from yaml file

    Args:
        path: path of file to load from
    Returns:
        config object
    """
    with open(path, "r") as fp:
        cfg_dict = yaml.load(fp, Loader=yaml.FullLoader)

    cfg = ConfigProblemBase(
        output_directory=cfg_dict.get(
            "output_directory", ConfigProblemBase.output_directory
        ),
        experiment_name=cfg_dict.get("experiment_name", generate_experiment_name()),
        llm_backbone=cfg_dict.get("llm_backbone", ConfigProblemBase.llm_backbone),
        dataset=ConfigNLPCausalLMDataset.from_dict(cfg_dict.get("dataset", {})),
        tokenizer=ConfigNLPCausalLMTokenizer.from_dict(cfg_dict.get("tokenizer", {})),
        augmentation=ConfigNLPAugmentation.from_dict(cfg_dict.get("augmentation", {})),
        architecture=ConfigNLPCausalLMArchitecture.from_dict(
            cfg_dict.get("architecture", {})
        ),
        training=ConfigNLPCausalLMTraining.from_dict(cfg_dict.get("training", {})),
        prediction=ConfigNLPCausalLMPrediction.from_dict(
            cfg_dict.get("prediction", {})
        ),
        environment=ConfigNLPCausalLMEnvironment.from_dict(
            cfg_dict.get("environment", {})
        ),
        logging=ConfigNLPCausalLMLogging.from_dict(cfg_dict.get("logging", {})),
    )
    return cfg
