class Ingredient:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class IngredientQuantity:
    def __init__(self, ingredient, quantity):
        self.ingredient = ingredient
        self.quantity = quantity

    def get_quantity(self):
        return self.quantity

    def get_ingredient(self):
        return self.ingredient

    def update_quantity(self, new_quantity):
        self.quantity -= new_quantity

    def __str__(self):
        return "<" + str(self.ingredient) + " : " + str(self.quantity) + ">"

    def __repr__(self):
        return "<" + str(self.ingredient) + " : " + str(self.quantity) + ">"
