from luna_city_rules import RULES
from question_generator import run_forward_chaining, run_backward_chaining


def list_rules():
    for r in RULES:
        print(f"{r['name']}: {r['then']} — {r['desc']}")


def main():
    print("HELLO, welcome to the Luna-City Expert Tourist Check System.")
    while True:
        print("\nMenu:")
        print("  1 - List all rules")
        print("  2 - Run forward chaining (dynamic questions)")
        print("  3 - Run backward chaining (dynamic questions)")
        print("  0 - Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            list_rules()
        elif choice == "2":
            run_forward_chaining()
        elif choice == "3":
            run_backward_chaining()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
