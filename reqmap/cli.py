
import io
from typing import List
import click
from toolz.functoolz import compose, reduce
from structout import gprint
import networkx as nx
from networkx import algorithms as nxa
from . import project

@click.group()
def cli():
    pass

@cli.command()
@click.argument("projects", nargs = -1)
def graph(projects: List[str]):
    project_graph: nx.Graph = reduce(
            nxa.compose,
            map(compose(lambda prj: prj.graph, project.Project.from_folder),
                projects))
    strio = io.StringIO()
    nx.drawing.nx_pydot.write_dot(project_graph, strio)
    click.echo(strio.getvalue())
