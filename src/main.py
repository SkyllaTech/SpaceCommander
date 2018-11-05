#! /usr/bin/env python3

from mako.template import Template
import yaml
import os, glob, pathlib, sys
import hashlib


def generate_host_template(f, config, hashval):
    return Template(open(f).read()).render(connection_config=config['connection'],
                                           commands_config=config['commands'],
                                           device_config=config['device'],
                                           host_config=config['host'],
                                           hashval=hashval)


def generate_device_template(f, config, hashval):
    return Template(open(f).read()).render(connection_config=config['connection'],
                                           commands_config=config['commands'],
                                           device_config=config['device'],
                                           hashval=hashval)


def load_config(filename):
    with open(filename) as commands_file:
        file_data = commands_file.read()
        config = yaml.load(file_data)
        hashval = hashlib.md5(file_data.encode('ascii')).hexdigest()[:10]

        # check for mandatory and optional components in config
        def check_exists(option, parent, p=False):
            if not option in parent:
                print('ERROR: Required option {} missing'.format(option))
                sys.exit(-1)
            if p:
                print('Building with {}: {}'.format(option, parent[option]))

        def fill_defaults(option, parent, default):
            if not option in parent:
                parent[option] = default

        # Ensure connection exists
        check_exists('connection', config, True)
        check_exists('type', config['connection'], False)
        # Ensure device exists
        check_exists('device', config, True)
        check_exists('type', config['device'], False)
        fill_defaults('timeout', config['device'], 1)
        # Host configuration
        if 'host' in config:
            fill_defaults('timeout', config['host'], None)

        # Ensure commands exists
        check_exists('commands', config)
        for command in config['commands']:
            # Ensure name and host exist
            check_exists('name', command)
            check_exists('host', command)
            fill_defaults('description', command, 'Documentation missing')

            fill_defaults('inputs', command, [])
            for inp in command['inputs']:
                check_exists('name', inp)
                check_exists('type', inp)
                fill_defaults('description', inp, 'Documentation missing')

            fill_defaults('outputs', command, [])
            for oup in command['outputs']:
                check_exists('name', oup)
                check_exists('type', oup)
                fill_defaults('description', oup, 'Documentation missing')

        return config, hashval


def generate_templates(config, hashval):
    template_dir = os.path.dirname(os.path.realpath(__file__))

    device_template_dir = os.path.join(template_dir, '..', 'templates', 'device_templates', config['device']['type'])
    ret_dict = {}

    # Host file generation
    if 'host' in config:
        print(config['host'])
        host_template_dir = os.path.join(template_dir, '..', 'templates', 'host_templates', config['host']['type'])
        generated_host_dir = os.path.join('generated/host', config['host']['type'])
        pathlib.Path(generated_host_dir).mkdir(parents=True, exist_ok=True)

        for f in glob.glob(os.path.join(host_template_dir, '*.spcmd')):
            generated_file_path = os.path.join(generated_host_dir, os.path.basename(f)[:-6])
            open(generated_file_path, 'w').write(generate_host_template(f, config, hashval))
            print('Generated host output file: {}'.format(generated_file_path))

        for f in glob.glob(os.path.join(host_template_dir, '*.spdoc')):
            ret_dict['{} - {}'.format(os.path.basename(f)[:-6], config['host']['type'])] = generate_host_template(f, config, hashval)

    # Device file generation
    generated_device_dir = os.path.join('generated/device', config['device']['type'])
    pathlib.Path(generated_device_dir).mkdir(parents=True, exist_ok=True)

    for f in glob.glob(os.path.join(device_template_dir, '*.spcmd')):
        generated_file_path = os.path.join(generated_device_dir, os.path.basename(f)[:-6])
        open(generated_file_path, 'w').write(generate_device_template(f, config, hashval))
        print('Generated device output file: {}'.format(generated_file_path))

    for f in glob.glob(os.path.join(device_template_dir, '*.spdoc')):
        ret_dict['{} - {}'.format(os.path.basename(f)[:-6], config['device']['type'])] = generate_device_template(f, config, hashval)

    return ret_dict


if __name__ == '__main__':
    generate_templates(*load_config('commands.yaml'))
