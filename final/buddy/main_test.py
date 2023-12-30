import unittest
from main import *

class TestBuddyAllocator(unittest.TestCase):
    def test_initialization(self):
        size = 1024
        buddy = BuddyAllocator(size)
        self.assertEqual(buddy.size, size)

    def test_allocate_and_free(self):
        buddy = BuddyAllocator(1024)
        addr = buddy.allocate(100)
        self.assertIsNotNone(addr)
        buddy.free(addr, 100)
        self.assertNotIn(addr, buddy.free_list[1024])

    def test_invalid_initialization(self):
        with self.assertRaises(ValueError):
            BuddyAllocator(1000)  # 非2的幂次方

    def test_allocation_failure(self):
        buddy = BuddyAllocator(1024)
        with self.assertRaises(ValueError):
            buddy.allocate(2048)  # 请求更多内存

    def test_double_free(self):
        buddy = BuddyAllocator(1024)
        addr = buddy.allocate(100)
        buddy.free(addr, 100)
        with self.assertRaises(ValueError):
            buddy.free(addr, 100)  # 二次释放同一个地址


if __name__ == "__main__":
    unittest.main()
