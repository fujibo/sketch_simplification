#!/usr/bin/env python
import argparse
import itertools
import os
import subprocess

"""
./apply hoge fuga --device 1 --index 0 --process_num 8
./apply hoge fuga --device 1 --index 1 --process_num 8
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    parser.add_argument('--device')
    parser.add_argument('--index', type=int, default=0)
    parser.add_argument('--n_procs', type=int, default=1)
    args = parser.parse_args()

    paths = sorted(os.listdir(args.input_dir))
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    cmd_tpl = 'CUDA_VISIBLE_DEVICES={} python simplify.py --img {} --out {}'
    paths = paths[args.index::args.n_procs]

    for i, path in enumerate(paths):
        cmd = cmd_tpl.format(
                args.device, os.path.join(args.input_dir, path), os.path.join(args.output_dir, path))

        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()


if __name__ == "__main__":
    main()
