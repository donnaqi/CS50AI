from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # definication for A
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # information given by A
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Or(Not(AKnight), Not(AKnave)))
)

# print(model_check(knowledge0, AKnave))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # definition of A
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # definition of B
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # information given by A
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Or(Not(AKnave), Not(BKnave)))
)
# print(model_check(knowledge1, AKnave))
# print(model_check(knowledge1, BKnight))

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # definition of A
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # definition of B
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # information given by A
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # information given by B
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),
)
# print(model_check(knowledge2, AKnave))
# print(model_check(knowledge2, BKnight))

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # definition of A
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # definition of B
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # definition of C
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    # information given by B says "A said 'I am a knave'."
    Implication(BKnight, Implication(AKnight, AKnave)),
    Implication(BKnight, Implication(AKnave, AKnight)),
    # information given by B says "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    # information given by C says "A is a knight."
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)

# print(model_check(knowledge3, AKnight))
# print(model_check(knowledge3, BKnight))
# print(model_check(knowledge3, CKnight))


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
