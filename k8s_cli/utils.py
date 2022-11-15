from typing import Text, List
import subprocess


def filter_jobnames_by_keywords(keyword: Text) -> List:
    # TODO: regex
    job_names = []
    try:
        out = subprocess.check_output(
            f'kubectl get dijob | grep {keyword}', shell=True
        )
    except subprocess.CalledProcessError as e:
        pass
    else:
        for line in out.decode("utf-8").split('\n'):
            try:
                job_names.append(line.split()[0]) 
            except IndexError:
                pass
    finally:
        return job_names


def create_unique_jobname(name: Text) -> Text:
    used_names = filter_jobnames_by_keywords(name)
    if name not in used_names:
        return name
    else:
        new_name = f'{name}-{0}'
        i = 0
        while new_name in used_names:
            new_name = f'{name}-{i}'
            i += 1
        return new_name


def str2none(func):
    if func == type(None):
        return str
    def newfunc(value):
        return None if value == 'None' else func(value)
    return newfunc
