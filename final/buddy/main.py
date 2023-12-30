class BuddyAllocator:
    def __init__(self, size):
        if not self.is_power_of_two(size):
            raise ValueError("Size must be power of two")
        self.size = self.get_power_of_two(size)
        self.free_list = {self.size: [0]}  # 使用2的幂作为键
        self.allocated_list = {}  # 记录分配的地址

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

        # 从小到大寻找合适的block size
        for block_size in sorted(self.free_list):
            if block_size >= size:
                # 取出第一个符合大小的block的首地址
                address = self.free_list[block_size].pop(0)
                if len(self.free_list[block_size]) == 0:
                    del self.free_list[block_size]  # 移除空列表

                # 确定了首地址和size, 对剩余内存进行拆分
                self.split(block_size, address, size)
                self.allocated_list[address] = size
                self.show_mem()
                return address
        raise ValueError("Can't allocate")

    def split(self, block_size, address, size):
        # 递归拆分
        while block_size > size:
            block_size //= 2
            # 计算出buddy的首地址
            buddy_address = address + block_size
            self.free_list.setdefault(block_size, []).append(buddy_address)

    def free(self, address, size):
        # 释放内存
        size = self.get_power_of_two(size)  # 调整size为2的幂

        # Do double free check
        if address not in self.allocated_list:
            raise ValueError("Can't double free")

        buddy_address = self.find_buddy(address, size)

        # 如果buddy空闲,则合并
        if size in self.free_list and buddy_address in self.free_list[size]:
            self.free_list[size].remove(buddy_address)
            if len(self.free_list[size]) == 0:
                del self.free_list[size]  # 移除空列表

            # 向左或向右合并buddy
            merged_address = min(address, buddy_address)

            # 尝试递归合并
            self.free(merged_address, size * 2)
        else:
            # buddy不空闲则把目前的释放
            self.free_list.setdefault(size, []).append(address)
            del self.allocated_list[address]  # 从记录中移除
            self.show_mem()

    def find_buddy(self, address, size):
        # 因为二分得到的buddy在地址上只有一位的差别,
        # 因此用异或操作可以直接计算出buddy的首地址
        return address ^ size

    def show_mem(self):
        mem_visual = ["-" for _ in range(self.size)]  # 初始化全部为可用
        # 标记已分配的内存
        for address, size in self.allocated_list.items():
            for i in range(address, address + size):
                mem_visual[i] = "X"

        # 将内存可视化为字符串
        mem_str = "".join(mem_visual)
        # 打印可视化的内存
        print("Memory Visualization:")
        print(mem_str)


if __name__ == "__main__":
    # 创建分配器
    buddy = BuddyAllocator(64)

    proc_a = buddy.allocate(8)
    print(f"Allocated at {proc_a}")
    print()

    proc_b = buddy.allocate(16)
    print(f"Allocated at {proc_b}")
    print()

    proc_c = buddy.allocate(32)
    print(f"Allocated at {proc_c}")
    print()

    buddy.free(proc_a, 8)
    print(f"freed {proc_a}")
    print()
