class BuddyAllocator:
    def __init__(self, size):
        if not self.is_power_of_two(size):
            raise ValueError("Size must be power of two")
        self.size = size
        self.free_list = {self.get_power_of_two(size): [0]}  # 使用2的幂作为键
        
    def is_power_of_two(self, n):
        if n <= 0:
            return False
        return (n & (n - 1)) == 0

    def get_power_of_two(self, size):
        # 找到不小于size的最小2的幂
        power = 1
        while power < size:
            power *= 2
        return power

    def allocate(self, size):
        # 分配内存函数
        size = self.get_power_of_two(size)  # 调整size为2的幂
        for block_size in sorted(self.free_list):
            if block_size >= size:
                address = self.free_list[block_size].pop(0)
                if len(self.free_list[block_size]) == 0:
                    del self.free_list[block_size]  # 移除空列表
                self.split(block_size, address, size)
                return address
        raise ValueError("Can't allocate")

    def split(self, block_size, address, size):
        while block_size > size:
            block_size //= 2
            buddy_address = address + block_size
            self.free_list.setdefault(block_size, []).append(buddy_address)

    def free(self, address, size):
        size = self.get_power_of_two(size)  # 调整size为2的幂
        buddy_address = self.find_buddy(address, size)
        if size in self.free_list and buddy_address in self.free_list[size]:
            self.free_list[size].remove(buddy_address)
            if len(self.free_list[size]) == 0:
                del self.free_list[size]  # 移除空列表
            merged_address = min(address, buddy_address)
            self.free(merged_address, size * 2)
        else:
            self.free_list.setdefault(size, []).append(address)

    def find_buddy(self, address, size):
        return address ^ size


if __name__ == "__main__":
    # 创建分配器
    buddy = BuddyAllocator(64)

    proc_a = buddy.allocate(8)
    print(f"Allocated at {proc_a}")

    proc_b = buddy.allocate(16)
    print(f"Allocated at {proc_b}")

    proc_c = buddy.allocate(32)
    print(f"Allocated at {proc_c}")

    buddy.free(proc_a, 100)
