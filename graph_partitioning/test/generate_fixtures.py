import os

from graph_partitioning.utils import generate_random_edges

FIXTURE_TYPES = (
    {
        'nodes': 10,
        'edges': 15
    },
    # {
    #     'nodes': 50,
    #     'edges': 65
    # },
    {
        'nodes': 100,
        'edges': 170
    },
    {
        'nodes': 1000,
        'edges': 15000
    }
)
FIXTURES_COUNT_PER_TYPE = 30

fixtures_folder = os.path.join(os.path.dirname(__file__), 'fixtures/')


def generate_random_graphs_fixtures():
    for fixture_number in range(1, FIXTURES_COUNT_PER_TYPE + 1):
        for fixture_type in FIXTURE_TYPES:
            file_name = (
                f"{fixture_type['nodes']}"
                f"_{fixture_type['edges']}"
                f"_{fixture_number}.txt"
            )
            random_edges = generate_random_edges(
                nodes_count=fixture_type['nodes'],
                edges_count=fixture_type['edges']
            )
            with open(os.path.join(fixtures_folder, file_name), 'w') as f:
                f.writelines(
                    ', '.join(str(s) for s in edge) + '\r\n'
                    for edge in random_edges
                )

generate_random_graphs_fixtures()