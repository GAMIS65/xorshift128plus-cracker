import z3
import sys
import itertools

"""
Only works on math.random() in Firefox doesn't work on Chrome 
"""

# XorShift128+ algorithm in python
class XorShift128Plus(object):
    def __init__(self, s0, s1):
        self.s0 = s0
        self.s1 = s1
        self.state = [s0, s1]
    
    def current_double(self):
        val = (self.s0 + self.s1) & 0x1fffffffffffff
        return float(val) / 2**53
    
    # This function generates another 64-bit integer
    def __next__(self):
        s1 = self.state[0]
        s0 = self.state[1]
        
        self.state[0] = s0
        s1 ^= (s1 << 23)
        s1 &= 0xffffffffffffffff
        self.state[1] = s1 ^ s0 ^ (s1>>17) ^ (s0>>26)
                
        random_val = (self.state[1] + s0) & 0xffffffffffffffff 
        
        return random_val
    
    # This function generates another floating point-type number in the range [0,1)
    def next_double(self):
        return float(next(self) & 0x1fffffffffffff) / 2**53
    
class Cracker(object):
    def __init__(self, known_values):
        self.s0 = z3.BitVec('s0', 64)
        self.s1 = z3.BitVec('s1', 64)
        self.state = [self.s0, self.s1]

        self.solver = z3.Solver()

        # The known variable will contain the values that we generated in Firefox
        self.known = known_values
    
    def __next__(self):
        s1 = self.state[0]
        s0 = self.state[1]
        
        self.state[0] = s0
        s1 ^= (s1 << 23)
        self.state[1] = s1 ^ s0 ^ z3.LShR(s1,17) ^ z3.LShR(s0,26)
                
        return self.state[1] + s0
    
    def crack(self):
        for val in self.known:
            nextval = z3.fpToFP(z3.get_default_rounding_mode(), next(self) & 0x1fffffffffffff, z3.Float64())/(2**53)
            self.solver.add(nextval == val)

        if self.solver.check() != z3.sat:
            raise Exception("Not solved!")
        
        model = self.solver.model()
        s0 = model[self.s0].as_long()
        s1 = model[self.s1].as_long()
        
        return (s0, s1)
 
def main():
    known_values = [float(v) for v in sys.argv[1].split(",")]
    
    # We crack the state of the random number generator.
    cracker = Cracker(known_values)
    (s0, s1) = cracker.crack()
    
    prng = XorShift128Plus(s0, s1)
    for _ in itertools.repeat(None, 15):
        print(prng.next_double())
    
 
if __name__ == '__main__':
    main()