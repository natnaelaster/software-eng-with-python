# Exercise on 
# Context Manager- The Real Reasson for (with)

class Timer:
    def __init__(self, label):
        self.label = label
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        elapsed_time = self.end_time - self.start_time
        print(f"[{self.label}] elapsed time:{elapsed_time:.6f} sec")
        return False

if __name__ == "__main__":
    import time
    with Timer('loop test'):
        total = 0
        for i in range(1_000_000):
            total += 1    
            
    print('done')        


import os
import tempfile
import shutil

class TempDir:
    def __init__(self, prefix="tmp"):
        self.prefix = prefix
        self.path = None
        
    def __enter__(self):
        self.path = tempfile.mkdtemp(prefix=self.prefix)  
        return self.path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path is not None:
            shutil.rmtree(self.path)
        return False
    
if __name__ == "__main__":
    with TempDir(prefix="mytest_") as path:
        print(f"Created: {path}")
        print(f"Exists during block: {os.path.exists(path)}")

        # write a file inside it to prove cleanup works
        with open(os.path.join(path, "hello.txt"), "w") as f:
            f.write("test")

        print(f"File created inside: {os.listdir(path)}")

    print(f"Exists after block: {os.path.exists(path)}")
    print("done")

    try:
        with TempDir(prefix="crash_") as path:
            print(f"Created: {path}")
            raise ValueError("something broke")
    except ValueError as e:
        print(f"Caught: {e}")

    print(f"Exists after exception: {os.path.exists(path)}")
    
