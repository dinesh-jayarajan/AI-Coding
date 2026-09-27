def Library(memberfee, installment, book):
    memberfee = int(memberfee)
    installment = int(installment)
    book_name = str(book).strip().lower()

    books_available = {
        "philosophers stone",
        "chamber of secrets",
        "prisoner of azkaban",
        "goblet of fire",
        "order of phoenix",
        "half blood prince",
        "deathly hallows 1",
        "deathly hallows 2",
    }

    if installment > 3:
        raise ValueError("Maximum Permitted Number of Installments is 3")

    if installment == 0:
        raise ZeroDivisionError("Number of Installments cannot be Zero.")

    amount_per_installment = memberfee / installment
    print("Amount per Installment is ", amount_per_installment)

    if book_name not in books_available:
        raise NameError("No such book exists in this section")

    print("It is available in this section")


