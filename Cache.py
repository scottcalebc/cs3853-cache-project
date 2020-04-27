
import math
import random


class Row:
    def __init__(self,
        block_size=16,
        cache=None
    ):
        self.block_size = block_size
        self.valid = 0
        self.tag = 0
        self.cache = cache

    def set_access(self, tag):
        self.cache.on_miss(self.valid)

        #print(f"Setting Row to {tag}")
        self.valid = 1
        self.tag = tag

    def data_access(self, tag):
        #print(f"Checking {self.tag} against {tag}")
        if self.valid:
            if self.tag == tag:
                return True
        return False


class Column:
    def __init__(self,
        num_rows=1,
        block_size=16,
        cache=None
    ):
        self.num_rows = num_rows
        self.block_size = block_size

        self.cache = cache
        self.rows = []
        
        for i in range(0, self.num_rows):
            row = Row(self.block_size, cache)
            self.rows.append(row)

    def set_access(self, index, tag):
        if self.cache.alg == "LRU":
            self.cache.set_col_access(self)

        #print(f"Set access called on col: {index} for tag: {tag}")

        return self.rows[index].set_access(tag)

    def data_access(self, index, tag):
        row_ret = self.rows[index].data_access(tag)

        if row_ret and self.cache.alg == "LRU":
            self.cache.set_col_access(self)
        
        return row_ret

    def find_empty(self, index):
        if self.rows[index].valid:
            return False
        return True


class Cache():

    def __init__(
        self,
        size = 1,
        associativity = 1,
        block_size = 16,
        alg = "RR",
    ):

        self.size = size * 2**10
        self.associativity = associativity
        self.block_size = block_size
        self.alg = alg
        self.address_bits = 32

        self.next_col_index = 0
        self.columns = []
        rows = self.size / (self.block_size * self.associativity)

        self.block_offset_bits = int(math.log(float(block_size), 2))
        self.index_bits = int(math.log(float(rows), 2))
        self.tag_bits = self.address_bits - self.index_bits - self.block_offset_bits
        
        self.overhead_bytes = int((self.associativity * (1 + self.tag_bits) * rows)/8)
        self.total_memory_size = (self.size + self.overhead_bytes)/ 2**10

        self.cost = 0.05

        self.next_col = 0
        self.lru_col = [0] * associativity

        self.hits = 0
        self.total_access = 0
        self.compulsory_miss = 0
        self.conflict_miss = 0


        self.total_cycles = 0
        self.instr_count = 0

        self.extra = 0


        for i in range(0, associativity):
            col = Column(int(rows), self.block_size, self)
            self.columns.append(col)


    # helper functions
    def claculate_bit_offset(self, address, num_bits):
        bits = address & ((1 << num_bits) - 1)
        address = address >> num_bits
        return (bits, address)

    def get_cache_bits(self, address):
        block_offset, new_address = self.claculate_bit_offset(address, int(self.block_offset_bits))
        index, new_address = self.claculate_bit_offset(new_address, int(self.index_bits))
        tag, new_address = self.claculate_bit_offset(new_address, int(self.tag_bits))

        return (tag, index, block_offset)


    def create_address(self, tag, index, block_offset):
        address = 0
        address |= (tag << (int(self.block_offset_bits) + int(self.index_bits)))
        address |= (index << int(self.block_offset_bits))
        address |= block_offset

        return address


    # cpi functions

    def on_hit(self):
        self.total_cycles += 1
        self.hits += 1

    def on_miss(self, miss_type):
        self.total_cycles += 3 * math.ceil(self.block_size/4)

        if miss_type == 0:
            self.compulsory_miss += 1
        
        if miss_type == 1:
            self.conflict_miss += 1

    def extra_cycles(self, num):
        self.total_cycles += num
        if num == 2:
            self.instr_count += 1


    # algorithm functions
    def set_col_access(self, col_obj):
        self.lru_col[self.columns.index(col_obj)] = 0
    
    def update_col_access(self):
        self.lru_col = list(map(lambda x: x+1, self.lru_col))

    def algo_col(self):
        if self.alg == "RR":
            ret = self.next_col
            self.next_col = (self.next_col + 1) % len(self.columns)
            return ret
        if self.alg == "RND":
            return random.randint(0, len(self.columns)) % len(self.columns)
        if self.alg == "LRU":
            return self.lru_col.index(max(self.lru_col))


    def algo_add(self, index, tag):
        col = self.algo_col()
        self.columns[col].set_access(index, tag)


    # data access functions
    def add_item(self, index, tag):
        for col in self.columns:
            if col.find_empty(index):
                col.set_access(index, tag)
                break
        else:
            self.algo_add(index, tag)


    def find_item(self, index, tag, block_offset, num_bytes, second_access=False):
        for col in self.columns:
            if col.data_access(index, tag):
                self.total_access += 1

                if not second_access:
                    self.on_hit()

                break
        else:
            self.add_item(index, tag)
            self.find_item(index, tag, block_offset, num_bytes, True)            

        blk_leftover = self.block_size - block_offset
        if blk_leftover < num_bytes:
            self.find_item(index + 1, tag, 0, num_bytes - blk_leftover)
            

    def data_access(self, address, num_bytes, instr_cost):
        tag, index, block_offset = self.get_cache_bits(address)

        
        if self.alg == "LRU" :
            self.update_col_access()

        self.find_item(index, tag, block_offset, int(num_bytes))

        self.extra_cycles(instr_cost)

        #print(f"TAG: {tag}\tINDEX: {index}\tblock_offset: {block_offset}")


    # string methods
    def unused_space(self):
        total_blks = math.ceil(self.size/self.block_size)
        leftover_blks = total_blks - self.compulsory_miss
        size_of_block_w_overhead = ((self.block_size * 2**3) + 1 + self.tag_bits)/2**3
        kb = 1024

        unused = ( leftover_blks * size_of_block_w_overhead ) / kb

        return f'{"{0:.2f}".format(unused)} KB / {self.total_memory_size} KB = {"{0:.2f}%".format((unused/self.total_memory_size)*100)} Waste: {"${0:.2f}".format(unused * self.cost)}'


    def overhead_size(self):
        return f'{self.overhead_bytes} bytes'


    def impl_mem_size(self):
        return f'{self.total_memory_size} KB ({int(self.total_memory_size * 1024)} bytes)'
        
        

    def cost_str(self):
        return "${0:.2f}".format(self.total_memory_size * self.cost)
        
    def results(self):
        return (
            f'Total Cache Accesses:           {self.total_access}\n'
            f'Cache Hits:                     {self.hits}\n'
            f'Cache Misses:                   {self.compulsory_miss + self.conflict_miss}\n'
            f'--- Compulsory Misses:              {self.compulsory_miss}\n'
            f'--- Conflict Misses:                {self.conflict_miss}\n'
        )

    def cpi_rate(self):
        return (
            f'Hit Rate:                         {"{0:.3f}%".format((self.hits * 100)/self.total_access)}\n'
            f'Miss Rate:                        {"{0:.3f}%".format(100 - ((self.hits * 100)/self.total_access))}\n'
            f'CPI:                              {"{0:.3}".format(self.total_cycles / self.instr_count)} Cycles/Instruction\n'
            f'Unused Cache Space:               {self.unused_space()}\n'
            f'Unused Cache Blocks:              {math.ceil(self.size / self.block_size) - self.compulsory_miss} / {math.ceil(self.size / self.block_size)}\n'
        )

    def __str__(self):
        return (
            f'Total # Blocks:                 {math.ceil(self.size / self.block_size)}\n'
            f'Tag Size:                       {self.tag_bits} bits\n'
            f'Index Size:                     {self.index_bits} bits\n'
            f'Total # Rows:                   {self.columns[0].num_rows}\n'
            f'Overhead Size:                  {self.overhead_size()}\n'
            f'Implementation Memory Size:     {self.impl_mem_size()}\n'
            f'Cost:                           {self.cost_str()}\n'
        )