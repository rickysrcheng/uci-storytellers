import os


in_dir = 'data/raw'
doc_paths = [os.path.join(in_dir, f) for f in os.listdir(in_dir)]
documents = []

for doc_path in doc_paths: 
    with open(doc_path, 'r') as f: 
        documents.append(f.read())

out = '\n\n\n'.join(documents)

# print(out)

out_dir = 'data/samples'
modes = ['train', 'valid', 'test']
for mode in modes: 
    with open(os.path.join(out_dir, f'{mode}.txt'), 'w') as f: 
        f.write(out)