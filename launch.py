from argparse import ArgumentParser
import subprocess
import sys

from omegaconf import OmegaConf


if __name__ == '__main__':

    parser = ArgumentParser()

    # TODO: nnodes
    parser.add_argument('-c', '--config', type=str, required=True)
    parser.add_argument('--name',  type=str)
    parser.add_argument('--u',  type=str)
    parser.add_argument('--ngpus', type=str)
    parser.add_argument('--ncpus', type=str)
    parser.add_argument('--memory',type=str)
    parser.add_argument('--image', type=str)
    parser.add_argument('--command', type=str)

    args = parser.parse_known_args()[0]
    args_dict: dict = vars(args)

    args_dict = {k: v for k, v in args_dict.items() if v is not None}

    yaml = OmegaConf.load(args_dict.pop('config'))
    yaml.merge_with({'default': args_dict})

    tmp_path = subprocess.check_output('mktemp', shell=True).decode('utf-8').rstrip()
    # print(f"Save yaml to {tmp_path}")
    OmegaConf.save(yaml, tmp_path, resolve=True)
    print(tmp_path)
    sys.exit(0)
