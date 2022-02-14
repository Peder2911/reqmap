from typing import List
import re
import os
from operator import add
from functools import reduce
import networkx as nx
import toml
import git
from . import dependency

class Project():
    def __init__(self, git_repo: git.Repo):
        self.repo: git.Repo = git_repo

    @classmethod
    def from_folder(cls, folder: str):
        return cls(git.Repo(folder))


    @property
    def path(self) -> str:
        dir, _ = os.path.split(self.repo.git_dir)
        return dir


    @property
    def requirements(self) -> List[dependency.Dependency]:
        return reduce(add, [self._vanilla_requirements, self._pyproject_dependencies], [])


    @property
    def _vanilla_requirements(self) -> List[dependency.Dependency]:
        def _try_to_split(ln: str) -> str:
            try:
                return re.split(r"[^a-zA-Z_\-0-9]=", ln)[0]
            except Exception:
                return ln

        try:
            with open(os.path.join(self.path, "requirements.txt")) as requirements_file:

                lines = requirements_file.readlines()
                return [dependency.Dependency(_try_to_split(ln)) for ln in lines]
        except FileNotFoundError:
            return []


    @property
    def _pyproject_dependencies(self) -> List[dependency.Dependency]:
        try:
            with open(os.path.join(self.path, "pyproject.toml")) as project_file:
                project = toml.load(project_file)
                return [dependency.Dependency(k) for k,v in project["tool"]["poetry"]["dependencies"].items()]
        except (FileNotFoundError, KeyError):
            return []


    @property
    def name(self):
        _, name = os.path.split(self.path)
        return name


    @property
    def graph(self):
        graph = nx.Graph()
        graph.add_node(self.name, kind = "package", shape = "square", color = "blue")
        for dep in self.requirements:
            graph.add_node(dep.name, kind = "dependency")
            graph.add_edge(self.name, dep.name)
        return graph
