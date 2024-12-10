from dataclasses import dataclass
from time import process_time


@dataclass
class Data:
    size: int
    id: int = None

    def is_empty(self):
        return self.id is None

    def is_file(self):
        return not self.is_empty()


def get_input():
    with open("test_input.txt", "r") as f:
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


def find_empty(disk_map: list[Data], idx=0):
    while idx < len(disk_map):
        data = disk_map[idx]
        if data.is_empty():
            # print(f"Found free space at {i}: {data_at_block}")
            return idx, data
        idx += 1
    return None, None


def defrag(disk_map: list[Data]):
    empty_idx = 0
    for i in range(len(disk_map) - 1, -1, -1):
        block = disk_map[i]
        if block.is_empty():
            continue
        empty_idx, empty_data = find_empty(disk_map, empty_idx)
        if empty_data is None or empty_idx >= i:
            break
        disk_map[empty_idx] = block
        empty_data.size = empty_data.size - 1
        disk_map[i] = Data(1)
        # print(f"Moved file {block.id} to {free_space_idx}")


start = process_time()
res = 0
disk_map = analyse_disk(get_input())
defrag(disk_map)
for i, block in enumerate(disk_map):
    if block.is_file():
        res += i * block.id
end = process_time()
print(res)
print(f"Took {end-start}s")
