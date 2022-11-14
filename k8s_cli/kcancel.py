from argparse import ArgumentParser
import subprocess

from k8s_cli.utils import filter_jobnames_by_keywords


def kcancel():
    """
    1) cancel dijobs by keywords

    e.g.
    $ kcancel -k k8s-cli-test
    delete dijob: zzh-k8s-cli-test? y
    dijob.diengine.opendilab.org "zzh-k8s-cli-test" deleted
    delete dijob: zzh-k8s-cli-test-0? y
    dijob.diengine.opendilab.org "zzh-k8s-cli-test-0" deleted
    delete dijob: others-k8s-cli-test? n
    """
    parser = ArgumentParser()
    parser.add_argument('-k', '--keyword', type=str)
    args = parser.parse_args()
    
    job_names = filter_jobnames_by_keywords(args.keyword)

    for job_name in job_names:

        response = input(f'delete dijob: {job_name}? ')
        while response not in ('y', 'yes', 'n', 'no'):
            response = input(f'y(es)/n(o): ')

        if response in ('n', 'no'):
            continue

        try:
            print(subprocess.check_output(
                f'kubectl delete dijob {job_name}', 
                shell=True
            ).decode('utf-8').rstrip())
        except subprocess.CalledProcessError as e:
            pass


if __name__ == '__main__':
    kcancel()
