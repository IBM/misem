class Cluster:
    def __init__(self, name):
        self.members = []
        self.name = name
        self.has_members = False

    def add_member(self, embedding, labels):
        self.members.append(embedding)
        self.has_members = True

    def get_center(self):
        if len(self.members) == 0:
            return None
        else:
            return torch.mean(torch.stack(self.members), dim=0)