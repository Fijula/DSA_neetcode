# Car Fleet
# Cars drive toward a target at position `target`. Car i starts at position[i] with
# speed[i]. A faster car that catches a slower one joins it and they move as one
# "fleet" at the slower speed. Return how many fleets reach the target.
# Example: target=10, position=[4,1,0,7], speed=[2,2,1,1] -> 3
#          target=10, position=[3],       speed=[3]       -> 1


# Case 1: Optimal: sort by position descending, then a stack of arrival times
def car_fleet(target, position, speed):
    # pair each car with its speed and process the ones CLOSEST to the target first
    cars = sorted(zip(position, speed), reverse=True)
    stack = []                         # arrival times of the fleets ahead

    for pos, spd in cars:
        time = (target - pos) / spd    # time for this car to reach the target alone

        # if it arrives no later than the fleet ahead, it catches up and merges,
        # so it does NOT create a new fleet
        if stack and time <= stack[-1]:
            continue
        stack.append(time)             # it stays behind: a new fleet

    return len(stack)
# Time:  O(n log n)   dominated by the sort
# Space: O(n)         the stack
# Comparing arrival TIMES rather than positions is what makes this simple: a car
# merges exactly when it would otherwise reach the target sooner than the car ahead.


# Case 2: Same idea without a stack, tracking only the slowest time ahead
def car_fleet_no_stack(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)
    fleets = 0
    slowest = 0.0                      # arrival time of the fleet currently in front

    for pos, spd in cars:
        time = (target - pos) / spd
        if time > slowest:             # cannot catch up: a genuinely new fleet
            fleets += 1
            slowest = time
    return fleets
# Time: O(n log n), Space: O(n) for the sorted pairs


if __name__ == "__main__":
    cases = [
        (10, [4, 1, 0, 7], [2, 2, 1, 1], 3),
        (10, [3], [3], 1),
        (12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3], 3),
        (100, [0, 2, 4], [4, 2, 1], 1),          # all three merge into one fleet
        (10, [0, 4, 2], [2, 1, 3], 1),
        (10, [], [], 0),                         # no cars, no fleets
    ]
    for target, position, speed, expected in cases:
        got = car_fleet(target, position, speed)
        print(target, position, speed, "->", got, got == expected)

    print(car_fleet_no_stack(10, [4, 1, 0, 7], [2, 2, 1, 1]))   # 3
