from dataclasses import dataclass
from time import process_time


@dataclass
class Data:
    size: int
    id: int = None
    def is_empty(d):
        return d.id is None
    def is_file(d):
        return not d.is_empty()


def get_input():
    with open("input.txt", "r") as f:
        return f.readline().strip()


def analyse_disk(encoded_blocks: str):
    disk_map = list()
    file_id = 0
    is_file = True
    encoded_blocks = list(map(int, encoded_blocks))
    for i in range(0, len(encoded_blocks)):
        size = encoded_blocks[i]
        if is_file:
            data = Data(size, file_id)
            file_id += 1
        else:
            data = Data(size)
        for _ in range(0, size):
            disk_map.append(data)
        is_file = not is_file
    return disk_map


def find_empty(disk_map: list[Data], req_size, idx=0):
    while idx < len(disk_map):
        data = disk_map[idx]
        if data.is_empty() and data.size >= req_size:
            # print(f"Found free space at {i}: {data_at_block}")
            return idx, data
        idx += data.size
    return None, None


def defrag(disk_map: list[Data]):
    empty_idx = 0
    i = len(disk_map) - 1
    while i > -1:
        block = disk_map[i]
        i -= block.size
        if block.is_empty():
            continue
        block_idx = i + 1
        empty_idx, data_ref = find_empty(disk_map, block.size)
        if data_ref is None or empty_idx >= block_idx:
            continue
        data_ref.size = data_ref.size - block.size
        new_freespace = Data(block.size)
        for offset in range(0, block.size):
            disk_map[empty_idx + offset] = block
            disk_map[block_idx + offset] = new_freespace
        # print(f"Moved file {block.id} to {free_space_idx}")


start = process_time()
res = 0
disk_map = analyse_disk(get_input())
defrag(disk_map)
for i, block in enumerate(disk_map):
    if isinstance(block, FreeSpace):
        continue
    res += i * block.id
end = process_time()
print(res)
print(f"Took {end-start}s")
