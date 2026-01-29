def crafting(current_recipe, inventory):
    for item in current_recipe[1]:
        if item[0] not in inventory or inventory[item[0]] < item[1]:
            break
    else:
        for item in current_recipe[1]:
            inventory[item[0]] -= item[1]
            if inventory[item[0]] == 0:
                del inventory[item[0]]
        if current_recipe[0][0] not in inventory:
            inventory[current_recipe[0][0]] = current_recipe[0][1]
        else:
            inventory[current_recipe[0][0]] += current_recipe[0][1]
    return inventory