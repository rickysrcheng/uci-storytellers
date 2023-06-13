# PREPROCESSING

## preprocess tatoeba_project dataset with custom conjunction mask
python create_ilm_examples.py train ./data/examples_tatoeba/exp_01 --data_name custom --data_dir "C:\Users\wjdgone\Documents\grad\2022-2023 Spring\272\uci-storytellers\data\tatoeba_project\parsed" --mask_cls ilm.mask.custom.MaskConjunction --max_num_retries_per_example 1

python create_ilm_examples.py valid ./data/examples_tatoeba/exp_01 --data_name custom --data_dir "C:\Users\wjdgone\Documents\grad\2022-2023 Spring\272\uci-storytellers\data\tatoeba_project\parsed" --mask_cls ilm.mask.custom.MaskConjunction --max_num_retries_per_example 1

python create_ilm_examples.py test ./data/examples_tatoeba/exp_01 --data_name custom --data_dir "C:\Users\wjdgone\Documents\grad\2022-2023 Spring\272\uci-storytellers\data\tatoeba_project\parsed" --mask_cls ilm.mask.custom.MaskConjunction --max_num_retries_per_example 1


# TRAINING

## train with tatoeba_project dataset with custom conjunction mask
python train_ilm.py exp_01 ./results_tatoeba/exp_01 ./data/examples_tatoeba/exp_01 --mask_cls ilm.mask.custom.MaskConjunction --train_batch_size 1 --train_num_epochs 10

