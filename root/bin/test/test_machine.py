from bin.constants import ItemNotPresent, IngredientNotPresent, IngredientQuantityInsufficient, NoSlots
from bin.src.machine import Machine
from bin.src.beverage import Beverage
from bin.src.ingredient import Ingredient
from bin.src.ingredient import IngredientQuantity
from unittest import TestCase


class MachineTest(TestCase):
    def get_machine(self):
        """
        :return: Machine object
        """
        pepsi = Ingredient("pepsi")
        hot_water = Ingredient("hot_water")
        hot_milk = Ingredient("hot_milk")
        ginger_syrup = Ingredient("ginger_syrup")
        lemon_juice = Ingredient("lemon_juice")
        sugar_syrup = Ingredient("sugar_syrup")
        tea_leaves_syrup = Ingredient("tea_leaves_syrup")
        green_mixture = Ingredient("green_mixture")

        # Beverage Items with its basic ingredients
        item_hot_tea = Beverage(
            "hot_tea",
            [
                IngredientQuantity(hot_water, 200),
                IngredientQuantity(hot_milk, 100),
                IngredientQuantity(ginger_syrup, 10),
                IngredientQuantity(sugar_syrup, 10),
                IngredientQuantity(tea_leaves_syrup, 10)
            ]
        )

        item_black_tea = Beverage(
            "black_tea",
            [
                IngredientQuantity(hot_water, 100),
                IngredientQuantity(ginger_syrup, 30),
                IngredientQuantity(sugar_syrup, 50),
                IngredientQuantity(tea_leaves_syrup, 30)
            ]
        )

        item_green_tea = Beverage(
            "green_tea",
            [
                IngredientQuantity(hot_water, 100),
                IngredientQuantity(ginger_syrup, 30),
                IngredientQuantity(green_mixture, 30)
            ]
        )

        item_lemon_water = Beverage(
            "lemon_water",
            [
                IngredientQuantity(hot_water, 300),
                IngredientQuantity(lemon_juice, 10)
            ]
        )

        item_cold_pepsi = Beverage(
            "cold_pepsi",
            [
                IngredientQuantity(pepsi, 1),
            ]
        )

        # Create a machine instance to run program (Ingredients, beverages, slot, timePerOrder)
        machine = Machine(
            [
                IngredientQuantity(pepsi, 500),
                IngredientQuantity(hot_water, 500),
                IngredientQuantity(hot_milk, 500),
                IngredientQuantity(ginger_syrup, 500),
                IngredientQuantity(ginger_syrup, 500),
                IngredientQuantity(lemon_juice, 500),
                IngredientQuantity(sugar_syrup, 500),
                IngredientQuantity(tea_leaves_syrup, 500)
            ],
            [
                item_black_tea, item_green_tea, item_hot_tea, item_lemon_water, item_cold_pepsi
            ],
            4,
            2
        )
        return machine

    def test1(self):
        machine = self.get_machine()
        # Success case -- Beverage is prepared
        hot_tea = machine.prepare_beverage("hot_tea")
        self.assertEqual("hot_tea", hot_tea.get_name())

        black_tea = machine.prepare_beverage("black_tea")
        self.assertEqual("black_tea", black_tea.get_name())

        # Beverage requested is not available (not in beverages list of machine)
        coffee = machine.prepare_beverage("coffee")
        self.assertEqual(ItemNotPresent, coffee)

        # One of ingredient in requested Beverage is not present
        green_tea = machine.prepare_beverage("green_tea")
        self.assertEqual(IngredientNotPresent, green_tea)

        # One of ingredient quantity in requested Beverage is not sufficient
        lemon_water = machine.prepare_beverage("lemon_water")
        self.assertEqual(IngredientQuantityInsufficient, lemon_water)

    def test2(self):
        # machine with 4 slots
        machine = self.get_machine()

        # Slot1
        machine.prepare_beverage("cold_pepsi")

        # Slot2
        machine.prepare_beverage("cold_pepsi")

        # Slot3
        machine.prepare_beverage("cold_pepsi")

        # Slot4
        machine.prepare_beverage("cold_pepsi")

        # All slots are full
        pepsi = machine.prepare_beverage("cold_pepsi")
        self.assertEqual(NoSlots, pepsi)
