#!/bin/bash
nohup python -u run.py \
    --test_file ./data/tasks_test.jsonl \
    --max_iter 2 \
    --api_key "$OPENAI_API_KEY"\
    --headless \
    --max_attached_imgs 5 \
    --temperature 2.0 \
    --fix_box_color \
    --seed 42 > test_tasks.log &
