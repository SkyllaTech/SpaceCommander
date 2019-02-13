
import os
import yaml
import hashlib

from data_types import DATA_TYPES

command_types = {
    'dict': dict,
    'list': list,
    'str': str,
    'int': int,
    'bool': bool,
}

# Maybe replace with a more advanced method of generating command numbers?x
def generate_command_indices(config):
    heartbeat_name = 'SPCMD_HEARTBEAT'
    hash_name = 'SPCMD_HASH'
    command_list = []
    # Add heartbeat command if needed
    if config['heartbeat'] is not None:
        command_list.append(heartbeat_name)
    # Add hash command
    command_list.append(hash_name)
    # Add remaining commands
    for command in config['commands']:
        command_list.append(command['name'])
    # Index commands
    command_dict = {x: i for i, x in enumerate(command_list)}
    # Set heartbeat command settings
    if config['heartbeat'] is not None:
        config['heartbeat']['NAME'] = heartbeat_name
        config['heartbeat']['index'] = command_dict[heartbeat_name]
    # Set hash command settings
    config['connection']['hash_name'] = hash_name
    config['connection']['hash_index'] = command_dict[hash_name]
    # Write command indices
    for key, val in command_dict.items():
        for i, command in enumerate(config['commands']):
            if key == command['name']:
                config['commands'][i]['NAME'] = '_'.join(['SPCMD', 'COMMAND', key.upper()])
                config['commands'][i]['index'] = val

    return config

# If node is dictionary, verify children
def validate_children(config_node, truth_node):
    for key, val in truth_node.items():
        # Skip information keys
        if key[0] == '_':
            continue

        # Check if child node is preset
        if key not in config_node:
            # Verify it is not required if it is missing
            if val['_required']:
                print("Error! Child {} is required but not present".format(key))
                return False
            # If default is available, use that
            if '_default' in truth_node[key]:
                config_node[key] = truth_node[key]['_default']
        else:
            # Verify child node
            # print("Validating:", key)
            if not validate_node(config_node[key], truth_node[key]):
                print("Error! Child {} is not valid".format(key))
                return False

    return True
    
# Validates a node recursively against the ground truth configuration
def validate_node(config_node, truth_node):
    # Verify type of node is correct
    if truth_node['_format'] == 'data_type':
        if config_node not in DATA_TYPES:
            print("Error! Node specifies data type {}, but that is not a valid data type".format(config_node))
            return False
    elif type(config_node) is not command_types[truth_node['_format']]:
        print("Error! Node is of type {}, but should be of type {}".format(
            type(config_node), truth_node['_format']
        ))
        return False

    # If node has specified options, ensure it matches
    if '_options' in truth_node:
        if type(config_node) is list:
            for item in config_node:
                if item not in truth_node['_options']:
                    print("Error! Node has item {}, but it is not a valid option from {}".format(
                        item, truth_node['_options']
                    ))
        if config_node not in truth_node['_options']:
            print("Error! Node has value {}, but is not in specified option list: {}".format(
                config_node, truth_node['_options']
            ))
            return False
    
    # If node is dictionary, verify children
    if type(config_node) is dict:
        if not validate_children(config_node, truth_node):
            return False

    # If node is list, verify items in list
    if type(config_node) is list:
        for item in config_node:
            if type(item) is dict:
                if not validate_children(item, truth_node):
                    return False
                
    return True

# Load the ground truth configuration file
def get_commands_format():
    commands_format = {}
    command_format_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "commands_format.yaml")
    with open(command_format_path) as f:
        commands_format = yaml.load(f.read())
        return commands_format

# Validate a loaded config
def validate_config(config):
    valid = get_commands_format()
    return validate_node(config, valid)

# Load config, validate, add hash
def load_config_from_string(s):
    config = yaml.load(s)
    if validate_config(config):
        # Hash configuration to prevent conflicts from invalid versions
        hash_val = hashlib.md5(yaml.dump(config).encode('ascii')).hexdigest()[:16]
        config['connection']['hash'] = hash_val
        config = generate_command_indices(config)
        return config
    else:
        print("Configuration invalid")
        return None

# Load config from file
def load_config_from_file(filename):
    with open(filename) as f:
        return load_config_from_string(f.read())
