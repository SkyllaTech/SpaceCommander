#! /usr/bin/env python3

import os, glob, pathlib, sys, argparse
import yaml
import hashlib
from mako.template import Template

import configuration


def generate_master_template(template, config, master):
    with open(template) as t:
        return Template(t.read()).render(connection=config['connection'],
                                         commands=config['commands'],
                                         heartbeat=config['heartbeat'],
                                         master=master)
    return None


def generate_slave_template(template, config, slave):
    with open(template) as t:
        return Template(t.read()).render(connection=config['connection'],
                                         commands=config['commands'],
                                         heartbeat=config['heartbeat'],
                                         slave=slave)
    return None


def generate_templates(config):
    template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'templates')
    generated_dir = 'generated'
    print("Loading templates from:", template_dir)
    # Master template generation
    for master in config['master']:
        print("Generating master:", master['type'])
        # print("Master Configuration:", master)
        generated_master_dir = os.path.join(generated_dir, '_'.join(['master', master['type']]))
        pathlib.Path(generated_master_dir).mkdir(parents=True, exist_ok=True)
        for template_path in glob.glob(os.path.join(template_dir, master['type'], 'master', '*.spcmd')):
            #print("Generating template file:", template_path)
            generated_file_path = os.path.join(generated_master_dir, os.path.basename(template_path)[:-6])
            with open(generated_file_path, 'w') as f:
                f.write(generate_master_template(template_path, config, master))
    # Slave template generation
    for slave in config['slave']:
        print("Generating slave:", slave['type'])
        # print("Slave configuration:", slave)
        generated_slave_dir = os.path.join(generated_dir, '_'.join(['slave', slave['type']]))
        pathlib.Path(generated_slave_dir).mkdir(parents=True, exist_ok=True)
        for template_path in glob.glob(os.path.join(template_dir, slave['type'], 'slave', '*.spcmd')):
            #print("Generating template file:", template_path)
            generated_file_path = os.path.join(generated_slave_dir, os.path.basename(template_path)[:-6])
            with open(generated_file_path, 'w') as f:
                f.write(generate_slave_template(template_path, config, slave))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    args = parser.parse_args()
    generate_templates(configuration.load_config_from_file(args.config_file))
