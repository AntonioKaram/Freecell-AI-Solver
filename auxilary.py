class Auxiliary:
    @staticmethod
    def syntax_error():
        print("Error | Invalid arguments")
        print("Run:")
        print("java -jar <method> <input-file> <output-file>")
        print("where:")
        print("<method> = breadth|depth|best|astar")
        print("<input-file> is a file containing a freecell description.")
        print("<output-file> is the file where the solution will be written.")

    @staticmethod
    def get_syntax_error():
        return ("Run:\n"
                "java -jar <method> <input-file> <output-file>\n"
                "where:\n"
                "<method> = breadth | depth | best | astar\n"
                "<input-file> is a file containing a freecell description.\n"
                "<output-file> is the file where the solution will be written.")

    @staticmethod
    def print_results(solution_found, time_elapsed, nodes_in_frontier, num_of_nodes_expanded, nodes_visited):
        print()
        if not solution_found:
            print("Solution not found")
        else:
            print("Solution found")
        print(f"Time elapsed: {time_elapsed} seconds")
        print(f"Nodes visited: {nodes_visited}")
        print(f"Nodes expanded: {num_of_nodes_expanded}")
        print(f"Nodes in frontier: {nodes_in_frontier}")

    @staticmethod
    def print_start_searching_message(method):
        print()
        print("Start Searching....")
        print(f"Using algorithm: {method}")
        print()

    @staticmethod
    def wrong_method():
        print("Algorithm provided does not exist")
        print("Trying astar instead")
        print("Or terminate the program and provide a correct algorithm")

    @staticmethod
    def move_helper_message():
        print()
        print("Move Helper message")
        print("---- Move card to freecell ----")
        print("<freecell> <card identifier ex: D5>")
        print()
        print("---- Move card to stack ----")
        print("<stack> <card identifier ex: D5 (card to move)> <card identifier ex: S4 (card on stack)>")
        print()
        print("---- Move card to empty stack ----")
        print("<newstack>  <card identifier ex: D5>")
        print()
        print("---- Move card to foundation ----")
        print("<source> <card identifier ex: D5>")

    @staticmethod
    def freecells_full_message():
        print("Freecells are full or the card is already in a freecell")
        print()

    @staticmethod
    def invalid_move_to_stack():
        print("Card should be smaller by 1 and different color to be placed in a stack")
        print()

    @staticmethod
    def invalid_move_to_foundation():
        print("Card should be A to start the foundation stack")
        print("Card should be smaller by 1 and same suit to be placed in the foundation")
        print()

    @staticmethod
    def generic_error():
        print("An Error occurred")
