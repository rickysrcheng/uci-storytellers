
import os
import pickle
import ilm.tokenize_util
import torch
from transformers import GPT2LMHeadModel
from ilm.infer import infill_with_ilm

# MODEL_DIR = './results/exp_00'
# MASK_CLS = 'ilm.mask.hierarchical.MaskHierarchical'

# MODEL_DIR = './results/exp_08'
# MASK_CLS = 'ilm.mask.hierarchical.MaskHierarchical'

# MODEL_DIR = './results/exp_06'
# MASK_CLS = 'ilm.mask.custom.MaskConjunction'

# MODEL_DIR = './results/exp_07'
# MASK_CLS = 'ilm.mask.custom.MaskProperNoun'

MODEL_DIR = './results_tatoeba/exp_01'
MASK_CLS = 'ilm.mask.custom.MaskConjunction'

# Prepare tokenizer
tokenizer = ilm.tokenize_util.Tokenizer.GPT2
with open(os.path.join(MODEL_DIR, 'additional_ids_to_tokens.pkl'), 'rb') as f:
    additional_ids_to_tokens = pickle.load(f)
additional_tokens_to_ids = {v:k for k, v in additional_ids_to_tokens.items()}
try:
    ilm.tokenize_util.update_tokenizer(additional_ids_to_tokens, tokenizer)
except ValueError:
    print('Already updated')
print(additional_tokens_to_ids)

# Load model
print('loading model')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GPT2LMHeadModel.from_pretrained(MODEL_DIR)
model.eval()
_ = model.to(device)


# Create context
print('creating context')
all_context = [
    """Chris was good at studying. _ he ended up passing the test.""".strip(),
    """They went through their evening routine. _ they left for the hospital.""".strip(),
    """We fear it, frankly. _ we do not understand it.""".strip(),
    """I don't know what he's doing. _ I think it's something illegal.""".strip(),
    """There were too many things she'd wanted to do before dying. _ that someone might kill her, she realized how unready she really was.""".strip(),
    """Soldiers were passing in a constant stream along the street blocking it completely. _ that Alpatych could not pass out and had to wait.""".strip(),
    """Think of it; a one million dollar reward was offered. _ no one was successful but you.""".strip(),
    ]

for context in all_context: 
    context_ids = ilm.tokenize_util.encode(context, tokenizer)
    print(len(context_ids))

    # Replace blanks with appropriate tokens from left to right
    _blank_id = ilm.tokenize_util.encode(' _', tokenizer)[0]
    # print(_blank_id)
    # print(context_ids.index(_blank_id))

    # if MODEL_DIR in ('./results/exp_00', './results/exp_08'): 
    #     context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|infill_word|>']
    # elif MODEL_DIR == './results/exp_07': 
    #     context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|infill_proper_noun|>']
    # elif MODEL_DIR in ('./results/exp_06', './results/exp_01'): 
    #     context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|infill_conjunction|>']
    # # print(ilm.tokenize_util.decode(context_ids, tokenizer))

    context_ids[context_ids.index(_blank_id)] = additional_tokens_to_ids['<|infill_conjunction|>']

    print('infilling')
    generated = infill_with_ilm(
        model,
        additional_tokens_to_ids,
        context_ids,
        # num_infills=3)
        num_infills=1)
    for g in generated:
        print('-' * 80)
        print(ilm.tokenize_util.decode(g, tokenizer))