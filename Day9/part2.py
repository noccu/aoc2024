from dataclasses import dataclass
from time import process_time


@dataclass
class FreeSpace:
    size: int


@dataclass
class File:
    size: int
    id: int = 0


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
            data = File(size, file_id)
            file_id += 1
        else:
            data = FreeSpace(size)
        for _ in range(0, size):
            disk_map.append(data)
        is_file = not is_file
    return disk_map


def find_free_space(disk_map: list, req_size):
    i = 0
    while i < len(disk_map):
        data_at_block = disk_map[i]
        if isinstance(data_at_block, FreeSpace) and data_at_block.size >= req_size:
            # print(f"Found free space at {i}: {data_at_block}")
            return i, data_at_block
        i += data_at_block.size
    return None, None


def defrag(disk_map: list):
    free_space_idx = 0
    i = len(disk_map) - 1
    while i > -1:
        block = disk_map[i]
        i -= block.size
        first_block_idx = i + 1
        if isinstance(block, FreeSpace):
            continue
        free_space_idx, data_ref = find_free_space(disk_map, block.size)
        if data_ref is None or free_space_idx >= first_block_idx:
            continue
        data_ref.size = data_ref.size - block.size
        new_freespace = FreeSpace(block.size)
        for offset in range(0, block.size):
            disk_map[free_space_idx + offset] = block
            disk_map[first_block_idx + offset] = new_freespace
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
