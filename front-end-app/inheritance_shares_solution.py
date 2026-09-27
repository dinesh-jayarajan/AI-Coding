class son(parent):
    def __init__(self, total_asset, Percentage_for_son):
        super().__init__(total_asset)
        self.Percentage_for_son = Percentage_for_son

    def son_display(self):
        son_share = round((self.total_asset * self.Percentage_for_son) / 100, 2)
        print(f"Share of Son is {son_share} Million.")


class daughter(parent):
    def __init__(self, total_asset, Percentage_for_daughter):
        super().__init__(total_asset)
        self.Percentage_for_daughter = Percentage_for_daughter

    def daughter_display(self):
        daughter_share = round((self.total_asset * self.Percentage_for_daughter) / 100, 2)
        print(f"Share of Daughter is {daughter_share} Million.")
