# leafsdk/core/mission/mission_plan.py

from enum import Enum, auto
import json
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass
import uuid
import networkx as nx

from leafsdk import logger
from leafsdk.utils.logstyle import LogIcons
from leafsdk.core.mission.mission_plan_step import MissionPlanStep, step_from_dict

class JoystickMode(Enum):
    """Joystick mode matching MAVLink JoystickMode enum."""
    DISABLED = 0
    ENABLED_ALWAYS = 1  # Joystick is always enabled
    ENABLED_ON_PAUSE = 2
    
    @staticmethod
    def str_to_enum(value: str) -> 'JoystickMode':
        try:
            return JoystickMode[value.upper()]
        except KeyError:
            return JoystickMode.ENABLED_ON_PAUSE

class MissionLoadBehavior(Enum):
    ERROR_IF_MISSION_IN_PROGRESS = auto()
    QUEUE_IF_MISSION_IN_PROGRESS = auto()
    REPLACE_IF_MISSION_IN_PROGRESS = auto() #

class AllowDuplicateNames(Enum):
    ALLOW = auto()
    OVERRIDE = auto()
    FAIL = auto()

class AutoStartBehavior(Enum):
    WAIT_FOR_COMMAND = auto()
    AUTOSTART_ON_LOAD_IMMEDIATELY = auto()

class StartingPointBehavior(Enum):
    START_FROM_LANDING = auto()
    START_FROM_CURRENT_POSITION = auto()

class PauseBehavior(Enum):
    PAUSE_IMMEDIATELY = auto()
    PAUSE_AFTER_CURRENT_STEP = auto()
    NO_PAUSE = auto()

class MissionSuccessfulCompletionBehavior(Enum):
    DEQUEUE_AND_LOAD_NEXT = auto()

class MissionUnsuccessfulCompletionBehavior(Enum):
    DEQUEUE_AND_LOAD_NEXT = auto()

class MissionConfig:
    """Configuration for mission execution."""
    def __init__(
        self, 
        joystick_mode: JoystickMode = JoystickMode.ENABLED_ON_PAUSE,
        mission_load_behavior: MissionLoadBehavior = MissionLoadBehavior.QUEUE_IF_MISSION_IN_PROGRESS,
        allow_duplicate_names: AllowDuplicateNames = AllowDuplicateNames.ALLOW,
        auto_start_behavior: AutoStartBehavior = AutoStartBehavior.WAIT_FOR_COMMAND,
        starting_point_behavior: StartingPointBehavior = StartingPointBehavior.START_FROM_LANDING,
        pause_behavior: PauseBehavior = PauseBehavior.PAUSE_IMMEDIATELY,
        successful_completion_behavior: MissionSuccessfulCompletionBehavior = MissionSuccessfulCompletionBehavior.DEQUEUE_AND_LOAD_NEXT,
        unsuccessful_completion_behavior: MissionUnsuccessfulCompletionBehavior = MissionUnsuccessfulCompletionBehavior.DEQUEUE_AND_LOAD_NEXT
    ):
        self.joystick_mode = joystick_mode
        self.mission_load_behavior = mission_load_behavior
        self.allow_duplicate_names = allow_duplicate_names
        self.auto_start_behavior = auto_start_behavior
        self.starting_point_behavior = starting_point_behavior
        self.pause_behavior = pause_behavior
        self.successful_completion_behavior = successful_completion_behavior
        self.unsuccessful_completion_behavior = unsuccessful_completion_behavior
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "joystick_mode": self.joystick_mode.name,
            "mission_load_behavior": self.mission_load_behavior.name,
            "allow_duplicate_names": self.allow_duplicate_names.name,
            "auto_start_behavior": self.auto_start_behavior.name,
            "starting_point_behavior": self.starting_point_behavior.name,
            "pause_behavior": self.pause_behavior.name,
            "successful_completion_behavior": self.successful_completion_behavior.name,
            "unsuccessful_completion_behavior": self.unsuccessful_completion_behavior.name
        }
    
    def copy(self) -> 'MissionConfig':
        """Create a copy of this config."""
        return MissionConfig(
            joystick_mode=self.joystick_mode,
            mission_load_behavior=self.mission_load_behavior,
            allow_duplicate_names=self.allow_duplicate_names,
            auto_start_behavior=self.auto_start_behavior,
            starting_point_behavior=self.starting_point_behavior,
            pause_behavior=self.pause_behavior,
            successful_completion_behavior=self.successful_completion_behavior,
            unsuccessful_completion_behavior=self.unsuccessful_completion_behavior
        )
    
    @staticmethod
    def _str_to_enum(enum_class, value: str, default):
        """Helper to convert string to enum with fallback to default."""
        if isinstance(value, enum_class):
            return value
        try:
            return enum_class[value.upper()]
        except (KeyError, AttributeError):
            return default
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'MissionConfig':
        """Create config from dictionary."""
        return MissionConfig(
            joystick_mode=JoystickMode.str_to_enum(data.get("joystick_mode", "ENABLED_ON_PAUSE")),
            mission_load_behavior=MissionConfig._str_to_enum(
                MissionLoadBehavior, 
                data.get("mission_load_behavior", "QUEUE_IF_MISSION_IN_PROGRESS"),
                MissionLoadBehavior.QUEUE_IF_MISSION_IN_PROGRESS
            ),
            allow_duplicate_names=MissionConfig._str_to_enum(
                AllowDuplicateNames,
                data.get("allow_duplicate_names", "ALLOW"),
                AllowDuplicateNames.ALLOW
            ),
            auto_start_behavior=MissionConfig._str_to_enum(
                AutoStartBehavior,
                data.get("auto_start_behavior", "WAIT_FOR_COMMAND"),
                AutoStartBehavior.WAIT_FOR_COMMAND
            ),
            starting_point_behavior=MissionConfig._str_to_enum(
                StartingPointBehavior,
                data.get("starting_point_behavior", "START_FROM_LANDING"),
                StartingPointBehavior.START_FROM_LANDING
            ),
            pause_behavior=MissionConfig._str_to_enum(
                PauseBehavior,
                data.get("pause_behavior", "PAUSE_IMMEDIATELY"),
                PauseBehavior.PAUSE_IMMEDIATELY
            ),
            successful_completion_behavior=MissionConfig._str_to_enum(
                MissionSuccessfulCompletionBehavior,
                data.get("successful_completion_behavior", "DEQUEUE_AND_LOAD_NEXT"),
                MissionSuccessfulCompletionBehavior.DEQUEUE_AND_LOAD_NEXT
            ),
            unsuccessful_completion_behavior=MissionConfig._str_to_enum(
                MissionUnsuccessfulCompletionBehavior,
                data.get("unsuccessful_completion_behavior", "DEQUEUE_AND_LOAD_NEXT"),
                MissionUnsuccessfulCompletionBehavior.DEQUEUE_AND_LOAD_NEXT
            )
        )

class GraphFunctions:
    @staticmethod
    def get_steps_from_graph(graph: nx.MultiDiGraph):
        for name, data in graph.nodes(data=True):
            yield name, data['step']
    
    def validate_graph(graph: nx.MultiDiGraph, logger = None) -> [str]:
        errors = []
        for node in graph.nodes:
            successors = list(graph.successors(node))
            if len(successors) > 1:
                seen_conditions = set()
                for succ in successors:
                    edge_data = graph.get_edge_data(node, succ)
                    condition = edge_data[0].get("condition")
                    if condition is None:
                        errors.append(f"Missing condition for edge {node} → {succ}")
                    elif condition in seen_conditions:
                        errors.append(f"Duplicate condition '{condition}' for branching at {node}")
                    else:
                        seen_conditions.add(condition)
        if logger is not None:
            logger.debug("Validating mission plan graph...")
            if errors:
                logger.debug(f"Found {len(errors)} validation errors.")
                for e in errors:
                    logger.debug(f"{LogIcons.ERROR} [prepare] {e}")
            else:
                logger.debug("No validation errors found.")
        return errors



class MissionPlan:
    def __init__(self, name: str="UnnamedMission", append_uuid: bool = True) -> None:
        # MissionPlan only has a name (with optional UUID appended for uniqueness)
        # The Mission class will generate its own independent ID
        if append_uuid:
            self.name = f"{name}_{str(uuid.uuid4())[:8]}"
        else:
            self.name = name
        self.config = MissionConfig()
        self._graph = nx.MultiDiGraph()
        self._head_node = None
        self._tail_node = None
        self._validated = False


    @property
    def mission_graph(self) -> nx.MultiDiGraph:
        return self._graph


    def _add_step(self, name: str, step: MissionPlanStep):
        if name in self._graph:
            raise ValueError(f"Node name '{name}' already exists in mission plan '{self.name}'.")
        self._graph.add_node(name, step=step)


    def _add_transition(self, from_step: str, to_step: str, condition=None):
        self._graph.add_edge(from_step, to_step, condition=condition, key=None)


    def _set_start(self, name: str):
        if name not in self._graph:
            raise ValueError(f"Start node '{name}' not found in mission graph.")
        self._head_node = name
    

    def _get_steps(self):
        yield from GraphFunctions.get_steps_from_graph(self._graph)
        # for name, data in self._graph.nodes(data=True):
        #     yield name, data['step']


    def _to_mission_plan_DTO(self) -> Dict[str, Any]:
        self.validate()
        data = {
            "id": self.name,
            "config": self.config.to_dict(),
            "nodes": [
                {
                    "name": name,
                    "type": step.__class__.__name__,
                    "params": step.to_dict()
                }
                for name, step in self._get_steps()
            ],
            "edges": [
                {"from": u, "to": v, "condition": self._graph.edges[u, v, k].get("condition")}
                for u, v, k in self._graph.edges
            ]
        }

        return data


    def add(self, to_name: str, to_step: MissionPlanStep, from_name: str=None, condition=None):
        first_node = not self._graph.nodes
        self._add_step(to_name, to_step)
        if first_node:
            self._set_start(to_name)
        if from_name:
            self._add_transition(from_name, to_name, condition)
        elif self._tail_node:
            self._add_transition(self._tail_node, to_name, condition)
        self._tail_node = to_name


    def add_subplan(self, subplan, prefix: str, connect_from: str=None, condition=None):
        if connect_from is None:
            connect_from = self._tail_node
        renamed_nodes = {}
        for name, data in subplan._graph.nodes(data=True):
            new_name = f"{prefix}_{name}"
            self._graph.add_node(new_name, **data)
            renamed_nodes[name] = new_name

        for u, v, edata in subplan._graph.edges(data=True):
            self._graph.add_edge(renamed_nodes[u], renamed_nodes[v], **edata)

        self._add_transition(connect_from, renamed_nodes[subplan._head_node])
    

    def save_to_json_file(self, filepath: str):
        """Save the mission plan to a JSON file."""
        data = self._to_mission_plan_DTO()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"{LogIcons.SUCCESS} MissionPlan file exported to: {filepath}")


    def as_dict(self) -> Dict[str, Any]:
        """Return the mission plan as a dictionary."""
        return self._to_mission_plan_DTO()
    

    def as_json(self) -> str:
        """Return the mission plan as a JSON string."""
        return json.dumps(self._to_mission_plan_DTO(), indent=2)


    def load(self, data: Union[dict, str]):
        """Load mission from a dictionary or JSON file path."""
        self.reset()

        if isinstance(data, str):
            with open(data, "r") as f:
                data = json.load(f)

        # Set mission name from data["name"] - UUID suffix already added in constructor
        # We replace the default "UnnamedMission_xxx" with the actual name + UUID
        base_name = data.get("name", "UnnamedMission")
        # Keep the UUID suffix from constructor, just update the base name
        name_parts = self.name.split("_")
        if len(name_parts) >= 2:
            # Keep the last part (UUID), replace everything before it
            self.name = f"{base_name}_{name_parts[-1]}"
        else:
            # Fallback if name format is unexpected
            self.name = f"{base_name}_{str(uuid.uuid4())[:8]}"
        
        # Load config first to check allow_duplicate_names setting
        if "config" in data:
            self.config = MissionConfig.from_dict(data["config"])
        elif "joystick_mode" in data:
            # Backward compatibility: support old format
            self.config.joystick_mode = JoystickMode.str_to_enum(data["joystick_mode"])
            logger.info(f"{LogIcons.SUCCESS} Loaded joystick_mode from legacy format: {self.config.joystick_mode.name}")

        for i, node in enumerate(data["nodes"]):
            step = step_from_dict(node["type"], node["params"])
            self._add_step(node["name"], step)
            if i == 0:
                self._set_start(node["name"])

        for edge in data["edges"]:
            self._add_transition(edge["from"], edge["to"], edge.get("condition"))

        logger.info(f"{LogIcons.SUCCESS} MissionPlan '{self.name}' loaded successfully.")


    def export_dot(self, filepath: str):
        try:
            from networkx.drawing.nx_pydot import write_dot
        except ImportError:
            logger.error(f"{LogIcons.ERROR} pydot or pygraphviz is required to export DOT files. Please install via pip.")

        # Add 'label' attributes to edges using the 'condition' attribute
        for u, v, data in self._graph.edges(data=True):
            if 'condition' in data:
                condition = data['condition']
                data['label'] = str(condition) if condition is not None else ''

        write_dot(self._graph, filepath)
        logger.info(f"{LogIcons.SUCCESS} DOT file exported to: {filepath}")


    def validate(self):
        errors = GraphFunctions.validate_graph(self._graph, logger)
        if errors:
            raise ValueError("Mission plan validation failed. See errors above.")
        else:
            self._validated = True
            logger.info(f"{LogIcons.SUCCESS} Mission plan has been validated.")

    
    def reset(self):
        """Reset the mission plan to its initial state."""
        self._graph.clear()
        self._validated = False
        self._head_node = None
        self._tail_node = None
        # Name stays as-is (with UUID suffix from constructor)
        logger.info(f"{LogIcons.SUCCESS} MissionPlan has been reset.")