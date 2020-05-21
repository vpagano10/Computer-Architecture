# CPU functionality.

import sys
program_file = sys.argv[1]
# this program list replaces the one hardcoded below in load function
program = []


class CPU:
    # Main CPU class.
    def __init__(self):
        # Construct a new CPU.
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7
        self.instructions = {
            "HLT": 0b00000001,
            "LDI": 0b10000010,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "PUSH": 0b01000101,
            "POP": 0b01000110
        }

    def load(self, program):
        # Load a program into memory.
        address = 0
        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        with open(program_file) as f:
            for line in f:
                line = line.strip().split("#")[0]
                # if line == "":
                #     continue
                if line != "":
                    self.ram_write(address, int(line, 2))
                    address += 1
        #     line = int(line, 2)
        #     program.append(line)

        # for instruction in program:
        #     # self.ram[address] = instruction
        #     self.ram_write(address, line)
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        # ALU operations.
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        # Handy function to print out the CPU state. You might want to call this
        # from run() if you need help debugging.
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        # should accept the address to read and return the value stored there
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # should accept a value to write, and the address to write it to
        self.ram[MAR] = MDR

    def run(self):
        # Run the CPU.
        # read memory address stored in register PC, and store result in IR where IR is just a local variable inside this function
        # make two more variables:
        #   operand_a = PC + 1 (&&) operand_b = PC + 2 (PC nums coming from ram)
        self.trace()
        running = True
        while running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            if ir == self.instructions["HLT"]:
                self.pc += 1
                running = False
            elif ir == self.instructions["LDI"]:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == self.instructions["PRN"]:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == self.instructions["MUL"]:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == self.instructions["PUSH"]:
                self.reg[self.SP] -= 1
                reg_num = self.ram[self.pc+1]
                val = self.reg[reg_num]
                address = self.reg[self.SP]
                self.ram[address] = val
                self.pc += 2
            elif ir == self.instructions["POP"]:
                val = self.ram_read(self.reg[self.SP])
                self.reg[operand_a] = val
                self.reg[self.SP] += 1
                self.pc += 2
            else:
                print("unknown instruction")
                sys.exit(1)
