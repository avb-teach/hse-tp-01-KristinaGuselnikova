#!/bin/bash


if [ "$#" -lt 2 ]; then
    echo "Недостаточно аргументов, должны быть указаны входящая и исходящая директории"
    exit 1
fi

input_dir="$1"
output_dir="$2"


if [ ! -d "$input_dir" ]; then
    echo "Входящая директория не существует, укажите правильную директороию"
    exit 1
fi

if [ ! -d "$output_dir" ]; then
    echo "Исходящая директория не существует, будет создана автамотически"
    mkdir -p "$output_dir"
fi
find "$input_dir" -type f -exec cp -t "$output_dir" -- {} +

