#! /usr/bin/env python3

import os, glob, pathlib, sys, argparse
import yaml
import hashlib
from mako.template import Template

import configuration

def generate_master_template(template, config):
    with open(template) as t:
        return Template(t.read()).render(connection=config['connection'],
                                         commands=config['commands'],
                                         heartbeat=config['heartbeat'],
                                         master=config['master'])
    return None

def generate_slave_template(template, config, slave):
    with open(template) as t:
        return Template(t.read()).render(connection=config['connection'],
                                         commands=config['commands'],
                                         heartbeat=config['heartbeat'],
                                         slave=slave)

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


def generate_templates(config):
    print("Configuration:", config)
    template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'templates')
    generated_dir = 'generated'
    print("Loading templates from:", template_dir)
    # Master template generation
    print("Master Configuration:", config['master'])
    generated_master_dir = os.path.join(generated_dir, '_'.join(['master', config['master']['type']]))
    pathlib.Path(generated_master_dir).mkdir(parents=True, exist_ok=True)
    for template_path in glob.glob(os.path.join(template_dir, config['master']['type'], 'master', '*.spcmd')):
        print("Generating template file:", template_path)
        generated_file_path = os.path.join(generated_master_dir, os.path.basename(template_path)[:-6])
        with open(generated_file_path, 'w') as f:
            f.write(generate_master_template(template_path, config))
    # Slave template generation
    for slave in config['slave']:
        print("Slave configuration:", slave)
        generated_slave_dir = os.path.join(generated_dir, '_'.join(['slave', slave['type']]))
        pathlib.Path(generated_slave_dir).mkdir(parents=True, exist_ok=True)
        for template_path in glob.glob(os.path.join(template_dir, slave['type'], 'slave', '*.spcmd')):
            print("Generating template file:", template_path)
            generated_file_path = os.path.join(generated_slave_dir, os.path.basename(template_path)[:-6])
            with open(generated_file_path, 'w') as f:
                f.write(generate_slave_template(template_path, config, slave))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    args = parser.parse_args()
    generate_templates(configuration.load_config_from_file(args.config_file))
