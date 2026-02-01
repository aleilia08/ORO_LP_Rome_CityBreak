from pulp import *

# Parameters
c_flight = 58
c_uber = 50
c_train = 12
c_hotel_3n = 300
c_airbnb_3n = 120
c_hostel_3n = 75
min_breakfast = 8
min_lunch = 15
min_dinner = 18.5
c_attraction_avg = 9
max_paid_attractions = 5
min_paid_attractions = 3


def solve_rome_citybreak(max_budget=300):
    problem = LpProblem("Rome_3Day_CityBreak_Optimization", LpMinimize)

    # Decision variables
    x_uber = LpVariable("Uber_Transport", cat=LpBinary)
    x_train = LpVariable("Train_Transport", cat=LpBinary)

    h_hotel = LpVariable("Hotel", cat=LpBinary)
    h_airbnb = LpVariable("Airbnb", cat=LpBinary)
    h_hostel = LpVariable("Hostel", cat=LpBinary)

    y_breakfast = LpVariable("Breakfast_per_day", lowBound=0, cat=LpContinuous)
    y_lunch = LpVariable("Lunch_per_day", lowBound=0, cat=LpContinuous)
    y_dinner = LpVariable("Dinner_per_day", lowBound=0, cat=LpContinuous)

    z_attractions = LpVariable(
        "Paid_Attractions",
        lowBound=0,
        upBound=max_paid_attractions,
        cat=LpInteger
    )

    # Objective function
    total_cost = (
        c_flight
        + c_uber * x_uber + c_train * x_train
        + c_hotel_3n * h_hotel + c_airbnb_3n * h_airbnb + c_hostel_3n * h_hostel
        + 3 * (y_breakfast + y_lunch + y_dinner)
        + c_attraction_avg * z_attractions
    )

    problem += total_cost, "Total_Cost"

    # Constraints
    problem += x_uber + x_train == 1, "One_Airport_Transport"
    problem += h_hotel + h_airbnb + h_hostel == 1, "One_Accommodation_Type"
    problem += y_breakfast >= min_breakfast, "Min_Breakfast_Cost"
    problem += y_lunch >= min_lunch, "Min_Lunch_Cost"
    problem += y_dinner >= min_dinner, "Min_Dinner_Cost"
    problem += z_attractions >= min_paid_attractions, "Min_Attractions"
    problem += total_cost <= max_budget, "Budget_Constraint"

    return problem, {
        "x_uber": x_uber,
        "x_train": x_train,
        "h_hotel": h_hotel,
        "h_airbnb": h_airbnb,
        "h_hostel": h_hostel,
        "y_breakfast": y_breakfast,
        "y_lunch": y_lunch,
        "y_dinner": y_dinner,
        "z_attractions": z_attractions,
        "total_cost": total_cost,
    }


if __name__ == "__main__":
    MAX_BUDGET = 300

    problem, v = solve_rome_citybreak(max_budget=MAX_BUDGET)

    problem.solve(PULP_CBC_CMD(msg=False))

    print("Status:", LpStatus[problem.status])

    if LpStatus[problem.status] != "Optimal":
        print(f"Model is not optimal under budget {MAX_BUDGET} €.")
        exit(0)

    # Read solution
    uber = int(round(v["x_uber"].varValue))
    train = int(round(v["x_train"].varValue))

    hotel = int(round(v["h_hotel"].varValue))
    airbnb = int(round(v["h_airbnb"].varValue))
    hostel = int(round(v["h_hostel"].varValue))

    breakfast = float(v["y_breakfast"].varValue)
    lunch = float(v["y_lunch"].varValue)
    dinner = float(v["y_dinner"].varValue)

    attractions = int(round(v["z_attractions"].varValue))

    total = float(value(v["total_cost"]))

    print("\nOptimal decisions:")
    print("Airport transport:")
    print("  Uber:", uber)
    print("  Train:", train)

    print("\nAccommodation choice:")
    print("  Hotel:", hotel)
    print("  Airbnb:", airbnb)
    print("  Hostel:", hostel)

    print("\nDaily food costs (€ per day):")
    print("  Breakfast:", round(breakfast, 2))
    print("  Lunch:", round(lunch, 2))
    print("  Dinner:", round(dinner, 2))

    print("\nPaid attractions visited:", attractions)

    cost_transport = c_uber * uber + c_train * train
    cost_accommodation = c_hotel_3n * hotel + c_airbnb_3n * airbnb + c_hostel_3n * hostel
    cost_food = 3 * (breakfast + lunch + dinner)
    cost_attractions = c_attraction_avg * attractions

    print("\nCost breakdown (€):")
    print("  Flight:", c_flight)
    print("  Transport:", round(cost_transport, 2))
    print("  Accommodation (3 nights):", round(cost_accommodation, 2))
    print("  Food (3 days):", round(cost_food, 2))
    print("  Attractions:", round(cost_attractions, 2))

    print("\nMinimum total cost (€):", round(total, 2))
    print("Budget limit (€):", MAX_BUDGET)
    print("Budget remaining (€):", round(MAX_BUDGET - total, 2))
