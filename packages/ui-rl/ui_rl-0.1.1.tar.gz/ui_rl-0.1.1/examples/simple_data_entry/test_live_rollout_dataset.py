from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AutoProcessor
from utils import Qwen2_5_VLCollate
from train_rl_5_rows import LiveRolloutDataset, reward_fn
from pathlib import Path
import torch.multiprocessing as mp

processor = AutoProcessor.from_pretrained("ByteDance-Seed/UI-TARS-1.5-7B")
collator = Qwen2_5_VLCollate(processor)

counter = mp.Value("i", 0)

ds = LiveRolloutDataset(
    Path("/tmp/rollouts"),
    processor,
    reward_fn=reward_fn,
    global_len_counter=counter,
    rank=1,
    world_size=2
)

dl = DataLoader(ds, batch_size=1, collate_fn=collator, num_workers=1)

for batch in tqdm(dl):
    pass

print(counter.value)
