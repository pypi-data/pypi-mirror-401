import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Type

from sxd_core import io

# Global registry for apps and their runtimes
_APP_REGISTRY: Dict[str, Any] = {}  # Map of app name to PipelineConfig


@dataclass
class WorkflowDefinition:
    """Definition of a registered workflow."""

    nickname: str
    workflow_class: Any  # Temporal workflow class
    input_type: Type[Any]  # Pydantic model or dataclass
    description: str = ""
    task_queue: str = "default"
    app_name: Optional[str] = None  # Link to the App container


# Global registry
_REGISTRY: Dict[str, WorkflowDefinition] = {}


def get_workflow(nickname: str) -> Optional[WorkflowDefinition]:
    """Get a workflow definition by nickname."""
    return _REGISTRY.get(nickname)


def get_app_config(app_name: str) -> Optional[Any]:
    """Get an app configuration by name."""
    return _APP_REGISTRY.get(app_name)


def list_workflows() -> Dict[str, WorkflowDefinition]:
    """List all registered workflows."""
    return _REGISTRY.copy()


# Activity Registry
@dataclass
class ActivityDefinition:
    """Definition of a registered activity."""

    name: str
    func: Callable
    task_queue: str = "default"
    description: str = ""


_ACTIVITY_REGISTRY: Dict[str, ActivityDefinition] = {}


def list_activities() -> Dict[str, ActivityDefinition]:
    """List all registered activities."""
    return _ACTIVITY_REGISTRY.copy()


def register_activity(
    func: Callable, name: Optional[str] = None, task_queue: str = "default"
):
    """Register an activity function."""
    activity_name = name or func.__name__
    _ACTIVITY_REGISTRY[activity_name] = ActivityDefinition(
        name=activity_name,
        func=func,
        task_queue=task_queue,
    )


def scan_for_temporal_definitions(module_name: str):
    """Scan a module for Temporal workflows and activities."""
    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        print(f"⚠️  Failed to scan module '{module_name}': {e}")
        return

    import inspect

    # Check all members
    for name, obj in inspect.getmembers(module):
        # Activities
        if hasattr(obj, "__temporal_activity_definition"):
            defn = getattr(obj, "__temporal_activity_definition")
            _ACTIVITY_REGISTRY[defn.name] = ActivityDefinition(
                name=defn.name,
                func=obj,
                task_queue="default",  # Unknown for pure Temporal unless inspected deeply
            )

        # Workflows
        if hasattr(obj, "__temporal_workflow_definition"):
            defn = getattr(obj, "__temporal_workflow_definition")
            # Try to infer input type from run method
            input_type = dict
            run_method = getattr(obj, "run", None)
            if run_method:
                sig = inspect.signature(run_method)
                # Skip 'self'
                params = list(sig.parameters.values())
                if len(params) > 1:
                    # First arg after self is usually input
                    input_arg = params[1]
                    if input_arg.annotation != inspect.Parameter.empty:
                        input_type = input_arg.annotation

            _REGISTRY[defn.name] = WorkflowDefinition(
                nickname=defn.name,
                workflow_class=obj,
                input_type=input_type,
                task_queue=str(
                    getattr(defn, "task_queue", None)
                    or getattr(obj, "task_queue", "default")
                ),
            )


def load_pipelines(
    root_dir: Optional[Path] = None, extra_modules: Optional[list[str]] = None
):
    """
    Dynamically load and scan pipelines, associating them with app-level runtimes.
    """
    import sys

    from sxd_sdk.pipeline import load_pipeline_config

    # helper to register an app from a directory
    def register_app_dir(app_dir: Path):
        sxd_yaml = app_dir / "sxd.yaml"
        if not sxd_yaml.exists():
            sxd_yaml = app_dir / "pipeline.yaml"

        if sxd_yaml.exists():
            try:
                config = load_pipeline_config(sxd_yaml)
                _APP_REGISTRY[config.name] = config
                # Add to path and scan
                if str(app_dir) not in sys.path:
                    sys.path.append(str(app_dir))

                # Scan package
                scan_for_temporal_definitions(app_dir.name)

                # Tag workflows from this scan with app_name
                for wf in _REGISTRY.values():
                    if wf.app_name is None:
                        wf.app_name = config.name
            except Exception as e:
                print(f"⚠️  Failed to load app config from {sxd_yaml}: {e}")
        else:
            # Fallback to pure scan if no yaml
            scan_for_temporal_definitions(app_dir.name)

    # 1. Load internal core components
    scan_for_temporal_definitions("sxd_core.workflows.upload_coordinator")
    scan_for_temporal_definitions("sxd_core.activities.upload")

    # 2. Load from extra modules list
    if extra_modules:
        for mod in extra_modules:
            scan_for_temporal_definitions(mod)

    # 2. Load from packages/ if root_dir is provided
    if root_dir:
        packages_dir = root_dir / "packages"
        if packages_dir.exists():
            for item in packages_dir.iterdir():
                if item.is_dir() and (item / "__init__.py").exists():
                    register_app_dir(item)

        # Backward compatibility for 'pipelines' dir
        pipelines_dir = root_dir / "packages/pipelines"
        if pipelines_dir.exists():
            for item in pipelines_dir.iterdir():
                if item.is_dir() and (item / "__init__.py").exists():
                    register_app_dir(item)

    # 3. Load from environment variable (SXD_PIPELINE_MODULES)
    env_modules = io.getenv("SXD_PIPELINE_MODULES")
    if env_modules:
        for mod in env_modules.split(","):
            scan_for_temporal_definitions(mod.strip())


def register_pipeline_metadata(config: Any):
    """
    Persist pipeline metadata to ClickHouse.
    """
    from sxd_core.clickhouse import ClickHouseManager

    ch = ClickHouseManager()
    ch.upsert_pipeline(
        {
            "name": config.name,
            "version": config.version,
            "description": config.description,
            "base_image": config.base_image,
            "gpu": config.gpu if hasattr(config, "gpu") else False,
            "timeout": config.timeout if hasattr(config, "timeout") else 3600,
        }
    )
