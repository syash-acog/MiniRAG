# from huggingface_hub import login
# your_token = "INPUT YOUR TOKEN HERE"
# login(your_token)

import os
from minirag import MiniRAG, QueryParam
from minirag.llm.hf import (
    hf_model_complete,
    hf_embed,
)
from minirag.utils import EmbeddingFunc
from transformers import AutoModel, AutoTokenizer

EMBEDDING_MODEL = "FremyCompany/BioLORD-2023" #nuvocare/WikiMedical_sent_biobert

import argparse


def get_args():
    parser = argparse.ArgumentParser(description="MiniRAG")
    parser.add_argument("--model", type=str, default="bio")
    parser.add_argument("--outputpath", type=str, default="./logs/Default_output.csv")
    parser.add_argument("--workingdir", type=str, default="./input")
    parser.add_argument("--datapath", type=str, default="./dataset")
    parser.add_argument(
        "--querypath", type=str, default="./dataset/LiHua-World/qa/query_set.csv"
    )
    args = parser.parse_args()
    return args


args = get_args()


if args.model == "PHI":
    LLM_MODEL = "microsoft/Phi-3.5-mini-instruct"
elif args.model == "GLM":
    LLM_MODEL = "THUDM/glm-edge-1.5b-chat"
elif args.model == "MiniCPM":
    LLM_MODEL = "openbmb/MiniCPM3-4B"
elif args.model == "biol":
    LLM_MODEL = "ashishkgpian/BioLlama_codes"
elif args.model == "bio":
    LLM_MODEL = "PrunaAI/stanford-crfm-BioMedLM-bnb-4bit-smashed" 
else:
    print("Invalid model name")
    exit(1)

WORKING_DIR = args.workingdir
DATA_PATH = args.datapath
QUERY_PATH = args.querypath
OUTPUT_PATH = args.outputpath
print("USING LLM:", LLM_MODEL)
print("USING WORKING DIR:", WORKING_DIR)


if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = MiniRAG(
    working_dir=WORKING_DIR,
    llm_model_func=hf_model_complete,
    llm_model_max_token_size=200,
    llm_model_name=LLM_MODEL,
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=1000,
        func=lambda texts: hf_embed(
            texts,
            tokenizer=AutoTokenizer.from_pretrained(EMBEDDING_MODEL),
            embed_model=AutoModel.from_pretrained(EMBEDDING_MODEL),
        ),
    ),
)


def find_single_txt_file(root_path):
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".txt"):
                return os.path.join(root, file)
    return None

txt_file = find_single_txt_file(DATA_PATH)
if txt_file is None:
    print(f"No .txt file found in {DATA_PATH}")
    exit(1)

print(f"Reading file: {txt_file}")
with open(txt_file, "r", encoding="utf-8") as f:
    content = f.read()
    if not content.strip():
        print("File is empty")
        exit(1)
    rag.insert(content)

# # A toy query
# query = 'What does LiHua predict will happen in "The Rings of Power"?'
# answer = (
#     rag.query(query, param=QueryParam(mode="mini")).replace("\n", "").replace("\r", "")
# )
# print(answer)
