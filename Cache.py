
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


    def read(self, tag, index, block_offset, num_bytes):
        read_bytes = num_bytes
        while read_bytes != 0 and tag < self.num_rows:
            bytes_read_from_row, block_offset  = self.rows[index].read(tag, block_offset, num_bytes)
            if bytes_read_from_row > 0:
                read_bytes = read_bytes - bytes_read_from_row
            else:
                return (read_bytes, index, block_offset)
            index += 1
        return (read_bytes, index, block_offset)

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

        

    def get_column(self):
        if self.arg == "RR":
            col = self.columns[self.next_col_index]
            self.next_col_index = (self.next_col_index + 1) % len(self.columns)
            return col
        else :
            return self.columns[0]

    def claculate_bit_offset(self, address, num_bits):
        bits = address & ((1 << num_bits) - 1)
        address = address >> num_bits
        return (bits, address)

    def get_address(self, address):
        block_offset, address = self.claculate_bit_offset(address, int(self.block_offset_bits))
        index, address = self.claculate_bit_offset(address, int(self.index_bits))
        tag, address = self.claculate_bit_offset(address, int(self.tag_bits))

        return (tag, index, block_offset)

    def create_address(self, tag, index, block_offset):
        address = 0
        address |= (tag << int(self.block_offset_bits) + int(self.index_bits))
        address |= (index << int(self.block_offset_bits))
        address |= block_offset

        return address


    def read(self, address, num_bytes):
        tag, index, block_offset = self.get_address(address)

        for col in iter(self.columns):
            read_bytes, index, block_offset = col.read(tag, index, block_offset, num_bytes)

        if read_bytes != 0:
            self.write()
            

        

