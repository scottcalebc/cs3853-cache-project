
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



class Cache:
    def __init__(
        self,
        address_space=1024,
        size = 1024,
        associativity = 1,
        block_size = 16,
        alg = "RR",
    ):

        self.size = size
        self.associativity = associativity
        self.block_size = block_size
        self.alg = alg

        self.next_col_index = 0
        self.columns = []
        rows = self.size / (self.block_size * self.associativity)

        self.block_offset_bits = math.log(float(block_size), 2)
        self.index_bits = math.log(float(rows), 2)
        self.tag_bits = math.log(float(address_space), 2) - self.index_bits - self.block_offset_bits


        for i in range(0, associativity):
            col = Column(int(rows), self.block_size)
            self.columns.append(col)

        


        
            

        

