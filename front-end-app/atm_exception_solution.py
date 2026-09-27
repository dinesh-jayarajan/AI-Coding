class MinimumDepositError(Exception):
    pass


class MinimumBalanceError(Exception):
    pass


def Bank_ATM(balance, choice, amount):
    balance = int(balance)
    choice = int(choice)
    amount = int(amount)

    try:
        if balance < 500:
            raise ValueError("As per the Minimum Balance Policy, Balance must be at least 500")

        if choice == 1:
            if amount < 2000:
                raise MinimumDepositError("The Minimum amount of Deposit should be 2000.")
            balance += amount

        elif choice == 2:
            if balance - amount < 500:
                raise MinimumBalanceError("You cannot withdraw this amount due to Minimum Balance Policy")
            balance -= amount

        print(f"Updated Balance Amount:  {balance}")

        return balance

    except (ValueError, MinimumDepositError, MinimumBalanceError) as err:
        print(err)
