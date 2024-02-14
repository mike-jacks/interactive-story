import json

class Terminal:

    def __init__(self, fname):
        self.wd = "~"
        self.filesystem = self.load_filesystem(fname)
        self.commands = {
            "pwd": self.pwd,
            "ls": self.ls
        }

    def load_filesystem(self, fname):
        with open(fname) as fobj:
            data = fobj.read()
        print(data)
        return json.loads(data)

    def execute(self, action):
        try:
            self.commands[action]()
        except:
            print("oops not a valid command")

    def pwd(self):
        print(self.wd)

    def ls(self):
        print(self.filesystem[self.wd])


def main():
    terminal = Terminal("./filesystems/home.json")
    print(terminal.filesystem)

    action = input("$ ")
    terminal.execute(action)

if __name__ == "__main__":
    main()
