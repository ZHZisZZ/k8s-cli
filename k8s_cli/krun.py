from argparse import ArgumentParser
import sys
import subprocess

import omegaconf
from omegaconf import OmegaConf

from k8s_cli.utils import create_unique_jobname, str2none


NODE_PREFIX = 'sh-idc1-10-140-0-{}'


def overwrite_yaml(krun=False):
    """
    1) overwrite default parameters in *.yaml from command line and create a temporary config file

    e.g.
    $ kubectl create -f $(overwrite-yaml -c sample.yaml --name k8s-cli-test --ncpus 32 --ngpus 8) -n di --validate=false
    """
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=str, required=True)
    config_path = parser.parse_known_args()[0].config
    yaml = OmegaConf.load(config_path)

    assert 'default_cli_args' in yaml, 'default_cli_args missing in yaml.'
    for k, v in yaml.default_cli_args.items():
        if isinstance(v, omegaconf.listconfig.ListConfig):
            parser.add_argument('--{}'.format(k), type=str2none(type(v[0]) if len(v) > 0 else str), default=v, nargs='+')
        else:
            parser.add_argument('--{}'.format(k), type=str2none(type(v)), default=v)

    args = parser.parse_args()

    # create an unique jobname if `name` in `default_cli_args`
    if 'name' in args:
        args.name = create_unique_jobname(args.name)
    if 'affinity' in args:
        args.affinity = [NODE_PREFIX.format(node_id) for node_id in args.affinity]

    args = vars(args); args.pop('config')
    yaml.merge_with({'default_cli_args': args})

    # if `tolerations` in `default_cli_args` and empty
    if not yaml.default_cli_args.get('tolerations', True):
        yaml.spec.tasks[0].template.spec.pop('tolerations')

    # if `affinity` in `default_cli_args` and is an empty list
    if not yaml.default_cli_args.get('affinity', True):
        yaml.spec.tasks[0].template.spec.pop('affinity')

    tmp_path = subprocess.check_output('mktemp', shell=True).decode('utf-8').rstrip()
    OmegaConf.save(yaml, tmp_path, resolve=True)

    if krun:
        return tmp_path
    else:
        print(tmp_path)
        sys.exit(0)


def krun():
    """
    1) overwrite default parameters in *.yaml from command line and create a dijob
    e.g.
    $ krun -c sample.yaml --name k8s-cli-test --ncpus 32 --ngpus 8

    2) simple grid search by creating multiple dijobs
    e.g. in `train.sh`
    for seed in 0 1 2; do
        for lr in 1e-1 1e-2 1e-3; do 
            krun -c sample.yaml \
                --name train-seed.${seed}-lr.${lr} \
                --command "python train.py --seed ${seed} --lr ${lr}"
        done
    done
    """
    try:
        print(subprocess.check_output(
            'kubectl create -f {} -n di --validate=false'.format(overwrite_yaml(krun=True)), 
            shell=True
        ).decode('utf-8').rstrip())
    except subprocess.CalledProcessError as e:
        pass


if __name__ == '__main__':
    krun()
