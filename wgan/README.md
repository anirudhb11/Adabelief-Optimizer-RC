### Steps to train WGAN 

This folder contains code to train WGANs on CIFAR-10 dataset

### Command to run

>python main.py --optimizer adabelief --eps 1e-12 --Train --dataset cifar10 

The hyper-parameters for different optimizers and runtime for the experiments can be looked up from [root README.md](../README.md).
We train WGAN using 9 different optimizers.

### Collage of generated images
![wgan_generated](generated/wgan_generated.png)