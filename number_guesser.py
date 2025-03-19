import random

def guess_the_number():
    number_to_guess = random.randint(1, 100)
    attempts = 0
    last_difference = None

    print("Welcome to the Number Guessing Game!")
    print("I have selected a number between 1 and 100. Can you guess it?")

    while True:
        try:
            guess = int(input("Enter your guess: "))
            print()
            attempts += 1
            current_difference = abs(number_to_guess - guess)

            if last_difference is not None:
                if current_difference == 0:
                    print("Correct!")
                elif current_difference < last_difference:
                    if current_difference <= 10:
                        print("Warmer!")
                    else:
                        print("Warm!")
                elif current_difference > last_difference:
                    if current_difference <= 10:
                        print("Colder!")
                    else:
                        print("Cold!")
                else:
                    print("Same distance as before!")

            if guess < number_to_guess:
                print("Too low! Try again.")
            elif guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You've guessed the number in {attempts} attempts.")
                break

            last_difference = current_difference

        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    guess_the_number()
