from setuptools import setup

setup(
    name='k8s-cli',
    version='0.1.0',
    packages=['k8s_cli'],
    install_requires=['omegaconf'],
    entry_points={'console_scripts': [
        'krun=k8s_cli.krun:krun',
        'kcancel=k8s_cli.kcancel:kcancel',
        'overwrite-yaml=k8s_cli.krun:overwrite_yaml',
    ]},
)
