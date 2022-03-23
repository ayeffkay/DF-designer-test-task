from argparse import ArgumentParser
import glob
from parse_graph import NodeTransformer
from layout import Graph
import ast
import logging
import os

logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--folder')
    parser.add_argument('--iterations', type=int, help="""Iterations for spring embedder to run.""", default=100)
    parser.add_argument('--width', type=int, default=10)
    parser.add_argument('--height', type=int, default=10)

    args = parser.parse_args()

    for file in glob.glob(f'{args.folder}/*'):
        with open(file) as f:
            data = f.read()

        # parsing
        nodes = ast.parse(data)
        node_transformer = NodeTransformer()
        node_transformer.visit(nodes)
        status = node_transformer.is_valid()
        graph_nodes = node_transformer.get_graph() if status == 'OK' else {}
        # layout compution
        if status == "OK":
            force_graph = Graph(graph_nodes, width=args.width, height=args.height)
            force_graph.compute_forces(T=args.iterations)
            graph_dict = force_graph.get_graph_dict()
        else:
            graph_dict = {}

        filename = os.path.split(file)[-1]
        logger.info(f"{filename} was parsed. Status: {status}")
        if status == "OK":
            logger.info(graph_nodes)