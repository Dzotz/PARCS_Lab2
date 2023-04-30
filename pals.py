from Pyro4 import expose
    
class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        str = self.read_input()
       
        step = len(str) / len(self.workers)
        
        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            print("map %d" % i)
            chunk = str[i*step:i*step+step]
            mapped.append(self.workers[i].mymap(chunk))

        # reduce
        primes = self.myreduce(mapped)

        # output
        self.write_output(primes)

        print("Job Finished")
    
    @staticmethod
    @expose
    def mymap(s):
        count = 0
        for i in range(len(s)):
            for j in range(i+1, len(s)+1):
                if j-i>1:
                    if s[i:j] == s[i:j][::-1]:
                        count += 1
        return count

    @staticmethod
    @expose
    def myreduce(mapped):
        print("reduce")
        output = 0
        for m in mapped:
            output+=m.value
        
        
        print("reduce done")
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        n = str(f.readline())
        f.close()
        return n

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
        print("output done")
