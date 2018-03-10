#! /usr/bin/env python3

from mako.template import Template
import yaml
import os, glob, pathlib, sys
import hashlib

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

        check_exists('device', config, False)
        check_exists('type', config['device'], True)
        check_exists('baudrate', config['device'], True)
        check_exists('commands', config)
        for command in config['commands']:
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

    if 'host' in config:
        print(config['host'])
        host_template_dir = os.path.join(template_dir, '..', 'templates', 'host_templates', config['host']['type'])
        generated_host_dir = os.path.join('generated', config['host']['type'])
        pathlib.Path(generated_host_dir).mkdir(parents=True, exist_ok=True)
        print(host_template_dir)
        for f in glob.glob(os.path.join(host_template_dir, '*.spcmd')):
            generated_file_path = os.path.join(generated_host_dir, os.path.basename(f)[:-6])
            open(generated_file_path, 'w').write(Template(open(f).read()).render(commands=config['commands'], device_config=config['device'], host_config=config['host'], hashval=hashval))
            print('host output file: {}'.format(generated_file_path))
        for f in glob.glob(os.path.join(host_template_dir, '*.spdoc')):
            ret_dict['{} - {}'.format(os.path.basename(f)[:-6], config['host']['type'])] = Template(open(f).read()).render(commands=config['commands'], device_config=config['device'], host_config=config['host'], hashval=hashval)
    generated_device_dir = os.path.join('generated', config['device']['type'])
    pathlib.Path(generated_device_dir).mkdir(parents=True, exist_ok=True)
    for f in glob.glob(os.path.join(device_template_dir, '*.spcmd')):
        generated_file_path = os.path.join(generated_device_dir, os.path.basename(f)[:-6])
        open(generated_file_path, 'w').write(Template(open(f).read()).render(commands=config['commands'], device_config=config['device'], hashval=hashval))
        print('device output file: {}'.format(generated_file_path))
    for f in glob.glob(os.path.join(device_template_dir, '*.spdoc')):
        print(f)
        print(config)
        ret_dict['{} - {}'.format(os.path.basename(f)[:-6], config['device']['type'])] = Template(open(f).read()).render(commands=config['commands'], device_config=config['device'], hashval=hashval)
    return ret_dict

if __name__ == '__main__':
    generate_templates(*load_config('commands.yaml'))
