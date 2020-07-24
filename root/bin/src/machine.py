import datetime
import heapq

from bin.constants import Constants
from bin.src.beverage import Beverage
from bin.src.ingredient import Ingredient
from bin.src.ingredient import IngredientQuantity


class Machine:
    def __init__(self, inventory_items, beverages_items, slots=1, time_per_order=2):
        """
        :param inventory_items: list of ingredients
        :param beverages_items: list of beverages
        :param slots: total slot in machine
        :param time_per_order: time per order in minutes
        :return:
        """
        self.slots = []
        self.slot_len = slots
        self.time_per_order = time_per_order
        self.inventory = {}
        self.beverages = {}

        for item in inventory_items:
            self.inventory.update({item.get_ingredient().get_name(): item})
        for beverage in beverages_items:
            self.beverages.update({beverage.get_name(): beverage})

    def prepare_beverage(self, beverage_name):
        """
        :param beverage_name: {type: string}beverage name to be prepared
        :return beverage: {type: beverages} beverage that has prepared
        """
        # get beverage item from beverage dict list
        beverage = self.beverages.get(beverage_name, None)
        try:
            # Check if requested beverage is available
            if beverage is None:
                raise(Exception(Constants.ItemNotPresent))
            else:
                now = datetime.datetime.now()
                # cur_time = datetime.timestamp(now)
                # Check Available Slots
                if self.check_get_slot(now):
                    # Check if ingredients are present and if quantity is sufficient
                    check_ingredient = self.all_ingredients_present(beverage)
                    if check_ingredient[0]:
                        # reduce the inventory items quantity
                        self.use_ingredients(beverage)
                        self.update_slot(now)
                    else:
                        raise(Exception(check_ingredient[1]))
                else:
                    raise(Exception(Constants.NoSlots))

        except Exception as exception_info:
            beverage = exception_info.args[0]
        return beverage

    def update_slot(self, cur_time):
        """
        :param cur_time: current time
        """
        if len(self.slots) == self.slot_len:
            heapq.heappop(self.slots)
        heapq.heappush(self.slots, cur_time)

    def check_get_slot(self, cur_time):
        """
        :param cur_time: current time
        :return: boolean value if slot available or not
        """
        if 0 <= len(self.slots) < self.slot_len:
            return True
        else:
            old_time = self.slots[0]
            if (cur_time - old_time).total_seconds()/60 > self.time_per_order:
                return True
        return False

    def all_ingredients_present(self, beverage):
        """
        :param beverage: {type: beverages} beverage that has prepared
        :return (type: list):
                [
                    Flag if beverage content is present and sufficeint in quantity
                    ,,
                    "Comment if content not available or insufficient"
                ]
        """
        # Get the content_list of beverage
        contents = beverage.get_contents()
        for content in contents:
            content_name = content.get_ingredient().get_name()
            # get item from inventory list if available
            inventory_item = self.inventory.get(content_name, None)
            if inventory_item is None:
                return [False, Constants.IngredientNotPresent]
            # Get quantity of this content of beverage to be prepared
            content_quantity = content.get_quantity()
            # Get quantity of this content available in inventory
            inventory_quantity = inventory_item.get_quantity()
            # Check if we quantity is sufficient
            if inventory_quantity < content_quantity:
                return [False, Constants.IngredientQuantityInsufficient]
        return [True, ""]

    def use_ingredients(self, beverage):
        """
        :param beverage:
        """
        contents = beverage.get_contents()
        for content in contents:
            content_name = content.get_ingredient().get_name()
            inventory_item = self.inventory.get(content_name, None)
            content_quantity = content.get_quantity()
            inventory_item.update_quantity(content_quantity)


if __name__ == "__main__":
    # Basic Ingredients
    hotWater = Ingredient("hot_water")
    hotMilk = Ingredient("hot_milk")
    blackTeaLeaves = Ingredient("black_tea_leaves_syrup")
    GreenTeaLeaves = Ingredient("green_tea_leaves_syrup")

    # Beverage Items with its basic ingredients
    hot_tea = Beverage(
        "hot_tea",
        [
            IngredientQuantity(hotWater, 100),
            IngredientQuantity(hotMilk, 50),
            IngredientQuantity(blackTeaLeaves, 10)
        ]
    )

    greenTea = Beverage(
        "green_tea",
        [
            IngredientQuantity(hotWater, 200),
            IngredientQuantity(hotMilk, 50),
            IngredientQuantity(GreenTeaLeaves, 10)
        ]
    )

    # Create a machine instance to run program (Ingredients, beverages, slot, timePerOrder)
    machine = Machine(
        [
            IngredientQuantity(hotWater, 500),
            IngredientQuantity(hotMilk, 500),
            IngredientQuantity(blackTeaLeaves, 500),
            IngredientQuantity(GreenTeaLeaves, 500)
        ],
        [
            hot_tea, greenTea
        ],
        4,
        2
    )

    print("\n--- machine object ---")
    print(machine)

    # Prepare beverage
    tea1 = machine.prepare_beverage("hot_tea")
    print("\n Result: ", tea1, machine.inventory)
    for i in range(1000000):
        pass
    tea2 = machine.prepare_beverage("hot_tea")
    print("\n Result: ", tea2, machine.inventory)
    for i in range(100000):
        pass

    tea = machine.prepare_beverage("hot_tea")
    print("\n Result: ", tea)
    for i in range(1000000):
        pass
    tea = machine.prepare_beverage("hot_tea")
    print("\n Result: ", tea)
    for i in range(1000000):
        pass
    tea = machine.prepare_beverage("hot_tea")
    print("\n Result: ", tea)
    tea = machine.prepare_beverage("hot_tea")
    print("\n Result: ", tea)
