# leafsdk/core/mission/mission_plan.py

from enum import Enum, auto
import json
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass
import uuid
import networkx as nx

from leafsdk import logger
from leafsdk.utils.logstyle import LogIcons
from leafsdk.core.mission.mission_step import MissionStep, step_from_dict
from petal_leafsdk.data_model import MissionConfig, JoystickMode


class MissionPlan:
    def __init__(self, name: str="UnnamedMission") -> None:
        self.name = name
        self.id = name + "_" + str(uuid.uuid4())  # Unique ID for each mission instance
        self.config = MissionConfig()
        self._graph = nx.MultiDiGraph()
        self._head_node = None
        self._tail_node = None
        self._validated = False


    @property
    def mission_graph(self) -> nx.MultiDiGraph:
        return self._graph


    def _add_step(self, name: str, step: MissionStep):
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
        for name, data in self._graph.nodes(data=True):
            yield name, data['step']


    def _to_node_link_data(self) -> Dict[str, Any]:
        self.validate()
        data = {
            "id": self.name,
            "joystick_mode": self.config.joystick_mode.value,
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


    def add(self, to_name: str, to_step: MissionStep, from_name: str=None, condition=None):
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
        data = self._to_node_link_data()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"{LogIcons.SUCCESS} MissionPlan file exported to: {filepath}")


    def as_dict(self) -> Dict[str, Any]:
        """Return the mission plan as a dictionary."""
        return self._to_node_link_data()
    

    def as_json(self) -> str:
        """Return the mission plan as a JSON string."""
        return json.dumps(self._to_node_link_data(), indent=2)


    def load(self, data: Union[dict, str]):
        """Load mission from a dictionary or JSON file path."""
        self.reset()

        if isinstance(data, str):
            with open(data, "r") as f:
                data = json.load(f)

        self.name = data.get("id", "UnnamedMission")

        # Load joystick mode if present
        if "joystick_mode" in data:
            try:
                self.config.joystick_mode = JoystickMode(data["joystick_mode"])
            except ValueError:
                logger.warning(f"{LogIcons.WARNING} Invalid joystick_mode '{data['joystick_mode']}' in mission plan. Defaulting to ENABLED.")
                self.config.joystick_mode = JoystickMode.ENABLED

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
        errors = []
        for node in self._graph.nodes:
            successors = list(self._graph.successors(node))
            if len(successors) > 1:
                seen_conditions = set()
                for succ in successors:
                    edge_data = self._graph.get_edge_data(node, succ)
                    condition = edge_data[0].get("condition")
                    if condition is None:
                        errors.append(f"Missing condition for edge {node} → {succ}")
                    elif condition in seen_conditions:
                        errors.append(f"Duplicate condition '{condition}' for branching at {node}")
                    else:
                        seen_conditions.add(condition)

        if errors:
            for e in errors:
                logger.error(f"{LogIcons.ERROR} [prepare] {e}")
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
        self.id = self.name + "_" + str(uuid.uuid4())
        logger.info(f"{LogIcons.SUCCESS} MissionPlan has been reset.")