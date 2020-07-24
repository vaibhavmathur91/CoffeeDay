class Beverage:
    def __init__(self, name, content_list):
        self.name = name
        self.contents = content_list

    def get_name(self):
        return self.name

    def get_contents(self):
        return self.contents

    def __str__(self):
        return "(" + str(self.name) + ": " + str(self.contents) + ")"

    def __repr__(self):
        return "(" + str(self.name) + ": " + str(self.contents) + ")"
