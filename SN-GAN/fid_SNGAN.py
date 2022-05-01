import os
from tensorflow.python.summary.summary_iterator import summary_iterator
from tensorflow.python.framework import tensor_util
import numpy as np
from matplotlib import pyplot as plt


def smooth(scalars, weight):  # Weight between 0 and 1
    last = scalars[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
        smoothed.append(smoothed_val)  # Save it
        last = smoothed_val  # Anchor the last smoothed value

    return smoothed


event_root = './logs'

event_file_names = [
    'SNGAN-adabelief-train-2021_06_23_11_36_05/',
    'SNGAN-adabound-train-2021_06_29_12_12_50/',
    'SNGAN-adam-train-2021_06_29_12_16_03/',
    'SNGAN-fromage-train-2021_07_03_19_58_52/',
    'SNGAN-msvag-train-2021_06_29_12_16_21/',
    'SNGAN-radam-train-2021_07_04_11_50_48/',
    'SNGAN-rmsprop-train-2021_06_28_12_29_09/',
    'SNGAN-sgd-train-2021_06_29_12_10_44/',
    'SNGAN-yogi-train-2021_06_29_12_16_26/'
]

labels = [
    "AdaBelief",
    "AdaBound",
    "Adam",
    "Fromage",
    "MSVAG",
    "RAdam",
    "RMSProp",
    "SGD",
    "Yogi",
]


def get_tensor(fname):
    # print(fname)
    fid_scores = []
    for e in summary_iterator(fname):
        for v in e.summary.value:
            if v.tag == 'Losses':
                # print(v.simple_value)
                fid_scores.append(v.simple_value)
    # print(fid_scores)
    smooth_scores = smooth(fid_scores, 0.95)
    return np.array(smooth_scores)


ylim = 2.75


def make_plot(optimizer, gen_loss, dis_loss):
    # len = fid_arr.shape[0]
    # step_arr = np.linspace(2000, 100000, len)
    plt.figure(figsize=(12, 5))
    print()
    x_vals = [0, 199, 399, 599, 799, 999]
    diffs = []
    for x in x_vals:
        diffs.append(abs(gen_loss[x] - dis_loss[x]))

    print(gen_loss.shape)
    plt.plot(gen_loss, '-', label='Generator Loss', linewidth=1.5)
    plt.plot(dis_loss, '-', label='Discriminator Loss', linewidth=1.5)


    for index, x in enumerate(x_vals):
        for y in np.linspace(min(gen_loss[x], dis_loss[x]) + 0.025, max(gen_loss[x], dis_loss[x]) - 0.025, 100):
            plt.text(x-2, y, '.', color='red')

        plt.text(x, (gen_loss[x] + dis_loss[x])/2, str.format('{:.2f}', diffs[index]))


    plt.legend(fontsize=9, loc='upper left', ncol=2)
    # title = 'SN-GAN '+ optimizer + ' Generator Discriminator loss'
    # plt.title(title)

    y_axis_list = np.linspace(0, ylim, 12)
    x_axis_list = ['0k', '20k', '40k', '60k', '80k', '100k']
    plt.xticks([0, 199, 399, 599, 799, 999], x_axis_list)
    plt.yticks(y_axis_list)
    plt.ylim((0, ylim))

    plt.xlabel('Training Steps')
    plt.ylabel('Loss')

    plt.grid()

    print(gen_loss.shape)
    print(dis_loss.shape)
    print('reache dhere')
    # plt.savefig('SNGAN_Gen_Dis_loss_' + optimizer + '.png', bbox_inches='tight',pad_inches = 0.1, dpi = 200)
    plt.savefig('SNGAN_Gen_Dis_loss_' + optimizer + '_with_diff.png', bbox_inches='tight', pad_inches=0.1, dpi=200)
    # plt.show()
    print('saved fig')


generator_loss = []
discriminator_loss = []

max_fid = 0
min_fid = 1e9
for fname in event_file_names:
    fpath_dis_root = os.path.join(event_root, fname, 'Losses_discriminator')
    fpath_dis = os.path.join(fpath_dis_root, os.listdir(fpath_dis_root)[0])
    # print(fpath_dis)
    optim_discrim = get_tensor(fpath_dis)
    print(optim_discrim.shape)
    # optim_discrim = ewma_vectorized(optim_discrim, 0)
    # optim_discrim = smooth(optim_discrim, 0.9)
    discriminator_loss.append(optim_discrim)

    fpath_gen_root = os.path.join(event_root, fname, 'Losses_generator')
    fpath_gen = os.path.join(fpath_gen_root, os.listdir(fpath_gen_root)[0])
    optim_gen = get_tensor(fpath_gen)
    # optim_gen = smooth(optim_gen, 0.9)
    # optim_gen = ewma_vectorized(optim_gen, 0)
    generator_loss.append(optim_gen)
    print(optim_gen.shape)


print(generator_loss[0])
print(discriminator_loss[0])
for label, gen_loss, dis_loss in zip(labels, generator_loss, discriminator_loss):
    make_plot(label, gen_loss, dis_loss)

    print('made plt')






