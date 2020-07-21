"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branch = {
        }
        
        self.branch[HLT] = self.hlt
        self.branch[LDI] = self.ldi
        self.branch[PRN] = self.prn
        self.branch[MUL] = self.mul
         
        
      

    def load(self):
        """Load a program into memory."""

       # address = 0

        # For now, we've just hardcoded a program:
           
        """program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1"""

        try:
            filename = sys.argv[1]
            address = 0
            with open(filename) as f:
                # Read contents line by line
                for line in f:
                    # Remove comments
                    line = line.split("#")[0]
                    # Remove whitespace
                    line = line.strip()
                    # Skip empty lines
                    if line == "":
                        continue

                    instruction = int(line, 2)

                    # Set the instruction to memory
                    self.ram[address] = instruction
                    address += 1
                    
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)
            
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
             

    def ldi(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)  
        self.reg[operand_a] = operand_b
        self.pc += 3

    def hlt(self):
        
        sys.exit(1)

    def prn(self):
        
        data = self.ram[self.pc + 1]
        print(self.reg[data])
        self.pc += 2

    def mul(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)  
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3
        
        
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
   
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.load()
        
        while True:
            # read memory address
            ir = self.ram_read(self.pc)
            # read bytes from Ram
            self.branch[ir]()

            
                
            
