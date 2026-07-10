from tracker import *
from cli_helpers import *


def main():

    while True:

        print("\n----- Fitness Tracker -----")
        print("1. Log Daily Metrics")
        print("2. Log Workout Session")
        print("3. Get Workout Recommendation")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            cli_log_daily_metrics()


        elif choice == "2":
            date = log_workout()
            

            if date is not None:

                display_workout_summary(date)
                display_recovery(date)
                calorie_trend(date)
                consistency_tracker(date)
                display_progress(date)

        elif choice == "3":
            display_recommendation()

        elif choice == "4":
            break

        else:
            print("Invalid Choice")

main()