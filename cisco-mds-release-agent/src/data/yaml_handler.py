def read_yaml(file_path):
    import yaml
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def write_yaml(file_path, data):
    import yaml
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def update_yaml(file_path, new_data):
    import yaml
    data = read_yaml(file_path)
    data.update(new_data)
    write_yaml(file_path, data)

def get_upgrade_paths(file_path):
    data = read_yaml(file_path)
    return data.get('releases', {})

def get_recommended_releases(file_path):
    data = read_yaml(file_path)
    return data.get('recommended_releases', {})