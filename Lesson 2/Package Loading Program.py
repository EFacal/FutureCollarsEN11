#1. First - ask about amount of packages
max_items = int(input("Provide the number of items to process"))

#1. 5 if max_items <= 0: wrong
if max_items <= 0:
    print("Number of items must be greater than 0")
    exit()

#2. initialize variables
current_package_weight = 0
packages_sent = 0
total_weight_sent = 0
max_unused_package = 1
max_unused_capacity = 0
item_count = 0

#if max_items is ok, then start main loop
while item_count < max_items:
    current_weight = int(input("Enter the weight of the item (1-10 kg), or 0 to quit"))

    #4. Check if quit the program
    if current_weight == 0:
        print("Terminating the program")
        break
    # 5. Main condition
    elif current_weight < 1 or current_weight > 10:
        print("Weight must be between 1 and 10 kg")
        continue
    else:
        # 6. If weight is ok, then start calculating
        if current_package_weight + current_weight > 20:
            # Package is full, send it
            unused = 20 - current_package_weight
            # Check if this package has more unused capacity
            if unused > max_unused_capacity:
                max_unused_capacity = unused
                max_unused_package = packages_sent + 1
            packages_sent += 1
            total_weight_sent += current_package_weight
            current_package_weight = current_weight
        else:
            # Add to current package
            current_package_weight += current_weight
        item_count += 1

        # Only print results after all items are processed
        if item_count == max_items:
            # Handle last package if not empty
            if current_package_weight > 0:
                unused = 20 - current_package_weight
                # Check if last package has most unused capacity
                if unused > max_unused_capacity:
                    max_unused_capacity = unused
                    max_unused_package = packages_sent + 1
                packages_sent += 1
                total_weight_sent += current_package_weight

            # 7. Print the results
            print("Results:")
            print(f"Number of packages sent: {packages_sent}")
            print(f"Total weight sent: {total_weight_sent} kg")
            print(f"Total unused capacity: {(packages_sent * 20) - total_weight_sent} kg")
            print(f"Package {max_unused_package} had the most unused capacity: {max_unused_capacity} kg")