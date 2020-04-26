
import math

class Row:
    def __init__(self,
        block_size=16
    ):
        self.block_size = block_size
        self.valid = 0
        self.tag = 0


class Column:
    def __init__(self,
        num_rows=1,
        block_size=16
    ):
        self.num_rows = num_rows
        self.block_size = block_size

        
        self.rows = []
        
        for i in range(0, self.num_rows):
            row = Row(self.block_size)
            self.rows.append(row)



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
        
        self.overhead_bytes = int(self.associativity * (1 + self.tag_bits) * rows/8)
        self.total_memory_size = (self.size + self.overhead_bytes)/ 2**10

        self.cost = 0.05


        for i in range(0, associativity):
            col = Column(int(rows), self.block_size)
            self.columns.append(col)

    def test_str(self):
        return (
            f'Size: {self.size}\n'
            f'block size: {self.block_size}\n'
            f'Associativity: {self.associativity}\n'
            f'Replacement Policy: {self.alg}\n'
            f'Address bits: {self.address_bits}'
        )

    def overhead_size(self):
        return f'{self.overhead_bytes} bytes'


    def impl_mem_size(self):
        return f'{self.total_memory_size} KB ({self.overhead_bytes} bytes)'
        
        

    def cost_str(self):
        return "${0:.2f}".format(self.total_memory_size * self.cost)
        

    def __str__(self):
        return (
            f'Total # Blocks:                 {math.ceil(self.size / self.block_size)}\n'
            f'Tag Size:                       {self.tag_bits}\n'
            f'Index Size:                     {self.index_bits}\n'
            f'Total # Rows:                   {self.columns[0].num_rows}\n'
            f'Overhead Size:                  {self.overhead_size()}\n'
            f'Implementation Memory Size:     {self.impl_mem_size()}\n'
            f'Cost:                           {self.cost_str()}\n'
        )
        
            

        

