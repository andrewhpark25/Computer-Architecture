"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000 
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101 
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.running = True
        self.branch = {}
        self.branch[HLT] = self.hlt
        self.branch[LDI] = self.ldi
        self.branch[PRN] = self.prn
        self.branch[MUL] = self.mul
        self.branch[PUSH] = self.push
        self.branch[POP] = self.pop
        self.branch[CALL] = self.call
        self.branch[RET] = self.ret
        self.branch[ADD] = self.add
        self.branch[CMP] = self.cmp_func
        self.branch[JMP] = self.jmp
        self.branch[JEQ] = self.jeq
        self.branch[JNE] = self.jne
        self.E = 0
        self.L = 0
        self.G = 0

       

      

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
            
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR
             

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3


    def hlt(self, operand_a, operand_b):
        self.running = False
        

    def prn(self, operand_a, operand_b):
        
        print(self.reg[operand_a])
        self.pc += 2
      

    def mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def add(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)
        self.pc += 3
    
    def push_value(self, value):
        self.reg[self.sp] -= 1
        self.ram_write(value, self.reg[self.sp])
        
    def push(self, operand_a, operand_b):
        # decrement sp
        self.push_value(self.reg[operand_a])
        self.pc += 2

    def pop_value(self):
        value = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        return value
    
    def pop(self, operand_a, operand_b):

        self.reg[operand_a] = self.pop_value()
        self.pc += 2

    def call(self, operand_a, operand_b):
        self.push_value(self.pc + 2)
        self.pc = self.reg[operand_a]


    def ret(self, operand_a, operand_b):
        self.pc = self.pop_value()
        
    
    def cmp_func(self, operand_a, operand_b):
        self.alu('CMP', operand_a, operand_b)
        self.pc += 3
        
    def jmp(self, operand_a, operand_b):
        self.pc = self.reg[operand_a]
       
    def jeq(self, operand_a, operand_b):
        if self.E == 1:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def jne(self, operand_a, operand_b):
        if self.E == 0:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2
        
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
                self.L = 0
                self.G = 0
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.L = 1
                self.E = 0
                self.G = 0
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.G = 1
                self.E = 0
                self.L = 0
               
   
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
        
        while self.running:
            # read memory address
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            # read bytes from Ram
            if int(bin(ir), 2) in self.branch:
                self.branch[ir](operand_a, operand_b)

