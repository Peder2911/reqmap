
import sys
from typing import List
import click
from toolz.functoolz import compose, reduce
import networkx as nx
from networkx import algorithms as nxa
from . import project

@click.group()
def cli():
    pass

@cli.command()
@click.option("-o","--output", type = click.File("w"), default = sys.stdout)
@click.argument("projects", nargs = -1)
def graph(projects: List[str], output):
    project_graph: nx.Graph = reduce(
            nxa.compose,
            map(compose(lambda prj: prj.graph, project.Project.from_folder),
                projects))
    nx.drawing.nx_pydot.write_dot(project_graph, output)
