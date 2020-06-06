import subprocess
class Execute(object):
    def __init__(self):
        pass

    @classmethod
    def call(self, cmd, verbose=False):
        if not isinstance(cmd, list):
            raise ValueError("cmd must be a list, current type is {} ".format(
                type(cmd)))


        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        while process.poll() is None:
            cur = process.stdout.readline()
            if verbose:
                cur = str(cur)
                print(cur.strip())

        process.stdout.close()
        print("Training process succeed!!!")

    @classmethod
    def system_call(self, cmd):
        import os
        os.system(cmd)
