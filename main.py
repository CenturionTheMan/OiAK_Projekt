import math
import random
import numpy as np
import os

def tens_to_bin(num):
    bits_arr = [int(i) for i in list('{0:0b}'.format(num))]
    return bits_arr


def bin_to_tens(bits_arr):
    res = 0
    base = 0
    for bit in reversed(bits_arr):
        res = res + bit * pow(2, base)
        base = base + 1
    return res


def split_bit_array_into_subvectors(bits_array, subvectors_amount):
    result_array = np.array_split(bits_array, subvectors_amount)
    return result_array


def extend_bin_with_zeros(bits_arr, zeros_amount):
    zeros_to_add = []
    for i in range(zeros_amount):
        zeros_to_add.append(0)
    zeros_to_add.extend(bits_arr)
    return zeros_to_add


def calculate_s(bits_arr, p, r, k):
    s = 0
    i = 1
    for i in range(1,k+1):
        sub_X = bits_arr.pop()
        sub_x = bin_to_tens(sub_X)
        cons = int(pow(2, r * (i - 1))) % p
        s = s + sub_x * cons
    return s


def modulo_computation_algorithm(x, p):
    X = tens_to_bin(x)
    r = int(math.ceil(math.log2(p)))
    k = int(math.ceil(len(X) / r))

    if len(X) < k * r:
        X = extend_bin_with_zeros(X, k * r - len(X))

    X = split_bit_array_into_subvectors(X, k)
    s1 = calculate_s(X, p, r, k)

    s_temp = s1
    loop_counter = 0
    while s_temp >= 2 * p:
        loop_counter = loop_counter + 1
        S_temp = tens_to_bin(s_temp)
        n_temp = len(S_temp)
        k_temp = int(math.ceil(n_temp/r))
        if len(S_temp) < k_temp * r:
            S_temp = extend_bin_with_zeros(S_temp, k_temp * r - len(S_temp))
        S_temp = split_bit_array_into_subvectors(S_temp, k_temp)
        s_temp = calculate_s(bits_arr=S_temp, p=p, r=r, k=k_temp)

    if p <= s_temp:
        return s_temp - p, loop_counter
    else:
        return s_temp, loop_counter


def save_in_file(x, p, counter):
    f = open(f'mod_{p}.csv', "a")
    f.write(f'{x};{p};{counter}\n')
    f.close()


def save_in_file_with_name(x, p, counter, file_name):
    f = open(file_name, "a")
    f.write(f'{x};{p};{counter}\n')
    f.close()


def perform_calculations(x_max, x_min, x_step, p_max, p_min, p_step):
    max_iterations = -1
    if os.path.exists("current_max.csv"):
        f = open("current_max.csv", "r")
        content = f.read()
        lines = content.split("\n")
        lines.pop()
        val_str = lines.pop().split(";")[2]
        max_iterations = int(val_str)

    for p in range(p_min, p_max, p_step):
        if os.path.exists(f'mod_{p}.csv'):
            os.remove(f'mod_{p}.csv')
        for x in range(x_min, x_max, x_step):
            if x % (x_step * 1000) == 0:
                print(f'p = {p} | x = {x} | perc = {(x*100/X):0.2f}%')
            x_mod_p, counter = modulo_computation_algorithm(x, p)
            save_in_file(x, p, counter)
            if counter > max_iterations:
                max_iterations = counter
                save_in_file_with_name(x,p,counter,"current_max.csv")

if __name__ == '__main__':
    maxX = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    maxP = [1,1,1,1,1,1,1,1]
    X = bin_to_tens(maxX)
    P = bin_to_tens(maxP)
    x_step = 1_000_000_000_000_000
    print("BEGINS...")
    perform_calculations(X, 0, x_step, P, 3, 1)
    print('END')

