python sweep_test.py \
--output_dir ./models/roberta-large \
--learning_rate 5e-05 \
--per_device_train_batch_size 8 \
--do_train \
--logging_steps 500 \
--evaluation_strategy "steps" \
--overwrite_cache \
--num_train_epochs 3 