#!/usr/bin/env bash
set -e
mkdir -p logs

shopt -s nullglob
magma_files=(computations/*.m)
sage_files=(computations/*.sage)

if [ ${#magma_files[@]} -gt 0 ]; then
    printf '%s\n' "${magma_files[@]}" | \
        parallel --joblog logs/magma_verify_joblog.txt -j "${1:-10}" \
        'magma -n {} >| logs/{/.}.txt'
fi

if [ ${#sage_files[@]} -gt 0 ]; then
    printf '%s\n' "${sage_files[@]}" | \
        parallel --joblog logs/sage_verify_joblog.txt -j "${1:-10}" \
        'command time -o logs/{/.}.timing.txt -v sage {} >| logs/{/.}.txt'
fi
