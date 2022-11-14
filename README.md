# What is this?
This is a cli for k8s whose usage is similar to `slurm` cli. Through `krun`, users can overwrite parameters in `*.yaml` by command line arguments and launch multiple dijobs. Through `kcancel`, users can cancel multiple dijobs by keywords.

# Why we need this?
`*.yaml` file contains default parameters for an dijob. Let's say one particular dijob takes 8 gpus. However, when resources on the cluster are limited, we may decide to decrease the number of gpus **temporarily** without changing the default parameters. In such cases, modifying `*.yaml` file inplace and then undoing the modification leaves a huge mental burden. Instead, it is better to have a way to overwrite the default parameters by command line arguments so that the changes are not permanent.

Also, overwriting parameters in `*.yaml` from command line arguments gives a way to run multiple dijobs (grid search for example) easily without having to create multiple `*.yaml` files or resort to `configmap`. 


# Install
```
pip install -e .
```

# krun
1. overwrite parameters in `sample.yaml` from command line arguments and create an dijob
```
$ krun -c sample.yaml
dijob.diengine.opendilab.org/zzh-k8s-cli-test created

# when name conflict, krun will automatically create an unique job name
$ krun -c sample.yaml
dijob.diengine.opendilab.org/zzh-k8s-cli-test-0 created

$ krun -c sample.yaml --name others-k8s-cli-test --ncpus 32 --ngpus 8
dijob.diengine.opendilab.org/others-k8s-cli-test created
```

2. grid search
```
for seed in 0 1 2; do
    for lr in 1e-1 1e-2 1e-3; do 
        krun -c sample.yaml \
            --name train-seed.${seed}-lr.${lr} \
            --command "python train.py --seed ${seed} --lr ${lr}"
    done
done
```

# kcancel
```
$ kcancel -k k8s-cli-test
delete dijob: zzh-k8s-cli-test? y
dijob.diengine.opendilab.org "zzh-k8s-cli-test" deleted
delete dijob: zzh-k8s-cli-test-0? y
dijob.diengine.opendilab.org "zzh-k8s-cli-test-0" deleted
delete dijob: others-k8s-cli-test? n
```
