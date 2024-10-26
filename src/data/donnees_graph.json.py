import json

graph_data = {
    "nodes": [
        {"id": 1, "label": "Node 1"},
        {"id": 2, "label": "Node 2"},
        {"id": 3, "label": "Node 3"}
    ],
    "edges": [
        {"from": 1, "to": 2},
        {"from": 2, "to": 3},
        {"from": 1, "to": 3}
    ]
}

print(json.dumps(graph_data))