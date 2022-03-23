import ast
import argparse
import glob
from flask import Flask, render_template, request
from parse_graph import NodeTransformer
from layout import Graph
import json
import sys
import os

WIDTH = 200
HEIGHT = 200

def create_app(folder: str):
    app = Flask(__name__)

    def parse_graphs():
        graphs = []
        for file in glob.glob(f'{folder}/*'):
            with open(file) as f:
                data = f.read()
            nodes = ast.parse(data)
            node_transformer = NodeTransformer()

            node_transformer.visit(nodes)
            status = node_transformer.is_valid()
            graph_nodes = node_transformer.get_graph() if status == 'OK' else {}
            response = dict(graph_nodes=graph_nodes, 
                            status=status)
            graphs.append(response)
        return graphs

    @app.route('/')
    def index():
        graphs = parse_graphs()
        res_graphs = {}

        for i, graph in enumerate(graphs):
            app.logger.info(graph['status'])
            if graph['status'] == 'OK':
                force_graph = Graph(graph['graph_nodes'], width=WIDTH, height=HEIGHT)
                force_graph.compute_forces(T=100)
                graph_dict= force_graph.get_graph_dict()
                app.logger.info(json.dumps(graph_dict))
            else:
                graph_dict = {}
            res_graphs[i] = dict(graph_dict=graph_dict, 
                                status=graph['status'])
        return render_template('index.html', res_graphs=res_graphs, ct=len(res_graphs))

    @app.route('/get_window_size', methods=['POST'])
    def get_window_size():
        window_size = request.get_json()
        ct = len(os.listdir(folder))
        WIDTH = window_size['width'] // ct
        HEIGHT = window_size['height'] // ct

    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5050)
    parser.add_argument('--folder', type=str, required=True)

    args, _ = parser.parse_known_args()
    app = create_app(args.folder)
    app.run(debug=True, host=args.host, port=args.port)