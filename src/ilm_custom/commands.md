# PREPROCESSING

## preprocess conll2003 dataset with custom conjunction mask
python create_ilm_examples.py train ./data/examples/exp_06 --data_name custom --data_dir "..\data\conll2003\ilm_format_filtermax" --mask_cls ilm.mask.custom.MaskConjunction

python create_ilm_examples.py valid ./data/examples/exp_06 --data_name custom --data_dir "..\conll2003\ilm_format_filtermax" --mask_cls ilm.mask.custom.MaskConjunction

python create_ilm_examples.py test ./data/examples/exp_06 --data_name custom --data_dir "..\conll2003\ilm_format_filtermax" --mask_cls ilm.mask.custom.MaskConjunction


# TRAINING

## train with conll2003 dataset with custom conjunction mask
python train_ilm.py exp_06 ./results/exp_06 ./data/examples/exp_06 --train_num_epochs 500 --mask_cls ilm.mask.custom.MaskConjunction
