
def extract_node_prefix(node_name: str) -> str:
    """Extract the prefix from the node name."""
    return node_name.split("_")[0] if "_" in node_name else node_name
