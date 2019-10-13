import os
import pandas as pd
import numpy as np
import nltk
from embeddings import GloveEmbedding
from nltk.tokenize import word_tokenize
# from vocabulary import Vocab
from config import OLID_PATH # SAVE_DIR, PAD_TOKEN, SEP_TOEKN
from utils import save, load, pad_sents, sort_sents, get_lens, get_mask, truncate_sents
from transformers import BertTokenizer

# Uncomment this line if you haven't download nltk packages
# nltk.download()


def read_file(filepath: str):
    df = pd.read_csv(filepath, sep='\t')

    ids = np.array(df['id'].values)
    tweets = np.array(df['tweet'].values)
    label_a = np.array(df['subtask_a'].values)
    label_b = np.array(df['subtask_b'].values)
    label_c = np.array(df['subtask_c'].values)
    nums = len(df)

    return nums, ids, tweets, label_a, label_b, label_c

def read_test_file(task, truncate=-1):
    df1 = pd.read_csv(os.path.join(OLID_PATH, 'testset-level' + task + '.tsv'), sep='\t')
    df2 = pd.read_csv(os.path.join(OLID_PATH, 'labels-level' + task + '.csv'), sep=',')
    ids = np.array(df1['id'].values)
    tweets = np.array(df1['tweet'].values)
    labels = np.array(df2['label'].values)
    nums = len(df1)

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    token_ids = [tokenizer.encode(text=tweets[i], add_special_tokens=True) for i in range(nums)]
    mask = np.array(get_mask(token_ids))
    token_ids = np.array(pad_sents(token_ids, tokenizer.pad_token_id))

    if truncate > 0:
        token_ids = truncate_sents(token_ids, truncate)

    return ids, token_ids, mask, labels


def bert_all_tasks(filepath: str, truncate=-1):
    nums, ids, tweets, label_a, label_b, label_c = read_file(filepath)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    token_ids = [tokenizer.encode(text=tweets[i], add_special_tokens=True) for i in range(nums)]
    mask = np.array(get_mask(token_ids))
    token_ids = np.array(pad_sents(token_ids, tokenizer.pad_token_id))

    if truncate > 0:
        token_ids = truncate_sents(token_ids, truncate)

    return ids, token_ids, mask, label_a, label_b, label_c

def bert_task_a(filepath: str, truncate=-1):
    nums, ids, tweets, label_a, _, _ = read_file(filepath)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    token_ids = [tokenizer.encode(text=tweets[i], add_special_tokens=True) for i in range(nums)]
    mask = np.array(get_mask(token_ids))
    token_ids = np.array(pad_sents(token_ids, tokenizer.pad_token_id))

    if truncate > 0:
        token_ids = truncate_sents(token_ids, truncate)

    return ids, token_ids, mask, label_a

def bert_task_b(filepath: str, truncate=-1):
    nums, ids, tweets, _, label_b, _ = read_file(filepath)
    # Only part of the tweets are useful for task b
    useful = label_b != 'NULL'
    ids = ids[useful]
    tweets = tweets[useful]
    label_b = label_b[useful]
    nums = len(label_b)
    # Tokenize
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    token_ids = [tokenizer.encode(text=tweets[i], add_special_tokens=True) for i in range(nums)]
    # Get mask
    mask = np.array(get_mask(token_ids))
    # Pad tokens
    token_ids = np.array(pad_sents(token_ids, tokenizer.pad_token_id))

    if truncate > 0:
        token_ids = truncate_sents(token_ids, truncate)

    return ids, token_ids, mask, label_b

def bert_task_c(filepath: str, truncate=-1):
    nums, ids, tweets, _, _, label_c = read_file(filepath)
    # Only part of the tweets are useful for task c
    useful = label_c != 'NULL'
    ids = ids[useful]
    tweets = tweets[useful]
    label_c = label_c[useful]
    nums = len(label_c)
    # Tokenize
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    token_ids = [tokenizer.encode(text=tweets[i], add_special_tokens=True) for i in range(nums)]
    # Get mask
    mask = np.array(get_mask(token_ids))
    # Pad tokens
    token_ids = np.array(pad_sents(token_ids, tokenizer.pad_token_id))

    if truncate > 0:
        token_ids = truncate_sents(token_ids, truncate)

    return ids, token_ids, mask, label_c