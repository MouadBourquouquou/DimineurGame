class Mine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = False   # Si la mine est révélée
        self.marquee = False   # Si le joueur a mis un drapeau

    def reveler(self):
        self.visible = True

    def marquer(self):
        self.marquee = not self.marquee  # Alterne entre marqué / pas marqué

    def est_visible(self):
        return self.visible

    def est_marquee(self):
        return self.marquee

    def position(self):
        return (self.x, self.y)
