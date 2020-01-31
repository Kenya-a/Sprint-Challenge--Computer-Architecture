"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
      
        self.registers = [0b0] * 8

        # internal registers
        self.pc = 0 
        self.ram = [0b0] * 0xFF
        self.ir = None # Instruction Register
        self.eq = None 
        self.lt = None 
        self.gt = None 
        self.stack_pointer = None 

        self.stack_pointer = 7
        self.registers[self.stack_pointer] = 0xF4

        self.OPCODES = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT',
            0b10100010: 'MUL',
            0b01000110: 'POP',
            0b01000101: 'PUSH',
            0b10000100: 'ST',
            0b10100111: 'CMP',
            0b01010100: 'JMP',
            0b01010110: 'JNE',
            0b01010101: 'JEQ',
        }

    def load(self, filename: str):
        """Load a program into memory."""

        try:
            with open(filename, 'r') as f:
                lines = (line for line in f.readlines() if not (line[0]=='#' or line[0]=='\n'))
                program = [int(line.split('#')[0].strip(), 2) for line in lines]

            address = 0

            for instruction in program:
                self.ram[address] = instruction
                address += 1
        except FileNotFoundError as e:
            print(e)
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # addition
        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]

        # multiplication
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]

        elif op == 'CMP':

            a = self.registers[reg_a]
            b = self.registers[reg_b]

            if a==b:
                self.eq, self.lt, self.gt = (1, 0, 0)
            elif a<b:
                self.eq, self.lt, self.gt = (0, 1, 0)
            elif a>b:
                self.eq, self.lt, self.gt = (0, 0, 1)
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
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        isRunning = True
        while isRunning:
            self.ir = self.ram[self.pc]
            try:
                op = self.OPCODES[self.ir]
            
                if op == 'LDI':
                    register = self.ram[self.pc+1]
                    value = self.ram[self.pc+2]
                    self.registers[register] = value
                    self.pc += 3

                # Print
                elif op == 'PRN':
                    register = self.ram[self.pc+1]
                    value = self.registers[register]
                    print(f"hex val: {value:x}\tdec val: {value}\tbin val: {value:b}")
                    self.pc += 2

                # pass to alu
                elif op == 'ADD' or op == 'MUL' or op == 'CMP':
                    reg_a = self.ram[self.pc+1]
                    reg_b = self.ram[self.pc+2]
                    self.alu(op, reg_a, reg_b)
                    self.pc += 3

                
                elif op == 'PUSH':
                    register = self.ram[self.pc + 1]
                    value = self.registers[register]
                    self.registers[self.stack_pointer] -= 1
                    # Copy the value in register to the address @ stack_pointer.
                    self.ram[self.registers[self.stack_pointer]] = value
                    self.pc += 2

                elif op == 'POP':
                    register = self.ram[self.pc + 1]
                    value = self.ram[self.registers[self.stack_pointer]]
                    # Copy value from the address @stack_pointer to  register.
                    self.registers[register] = value
                    # Increment stack_pointer.
                    self.registers[self.stack_pointer] += 1
                    self.pc += 2

                elif op == 'ST':
                    # Store value in reg_b to the address stored in reg_a.
                    reg_a = self.ram[self.pc + 1]
                    reg_b = self.ram[self.pc + 2]
                    address_a = self.registers[reg_a]
                    val_b = self.registers[reg_b]
                    self.ram[addres_a] = val_b
                    self.pc += 2

                elif op == 'JMP':
                    # Jump to the address stored in register.
                    self.register = self.ram[self.pc + 1]
                    value = self.registers[self.register]
                    # Set the PC to the address stored register.
                    self.pc = value

                elif op == 'JEQ':
                    if self.eq == 1:
                        self.register = self.ram[self.pc + 1]
                        value = self.registers[self.register]
                        self.pc = value
                    else:
                        self.pc += 2

                elif op == 'JNE':
                    if self.eq == 0:
                        self.register = self.ram[self.pc + 1]
                        value = self.registers[self.register]
                        self.pc = value 
                    else:
                        self.pc += 2

                # exit
                elif op == 'HLT':
                    isRunning = False

            except KeyError as e:
                print(f"unknown command {self.ir}")
                self.pc += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
        
