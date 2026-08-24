import sys

class HanoiGame:
    def __init__(self, num_disks: int = 3):
        self.num_disks = num_disks
        self.towers = {
            '1': list(range(num_disks, 0, -1)),
            '2': [],
            '3': []
        }
        self.moves_count = 0

    def display(self):
        print("\n--- Tower of Hanoi ---")
        for lvl in range(self.num_disks - 1, -1, -1):
            row_str = []
            for col in ['1', '2', '3']:
                if lvl < len(self.towers[col]):
                    val = str(self.towers[col][lvl])
                else:
                    val = "|"
                row_str.append(val.center(5))
            print(" ".join(row_str))
        print("  col-1 col-2 col-3".center(17))
        print(f"Moves: {self.moves_count}\n")

    def move_disk(self, src: str, dst: str) -> bool:
        if src not in self.towers or dst not in self.towers:
            print("Error: Invalid tower selection! Use 1, 2, or 3.")
            return False

        if src == dst:
            print("Error: Source and destination towers must be different.")
            return False

        if not self.towers[src]:
            print(f"Error: Tower {src} is empty!")
            return False

        disk = self.towers[src][-1]

        if self.towers[dst] and self.towers[dst][-1] < disk:
            print(f"Invalid move! Cannot place larger disk {disk} on smaller disk {self.towers[dst][-1]}.")
            return False

        self.towers[src].pop()
        self.towers[dst].append(disk)
        self.moves_count += 1
        return True

    def is_won(self) -> bool:
        return len(self.towers['2']) == self.num_disks or len(self.towers['3']) == self.num_disks

def play_hanoi():
    print("Welcome to Tower of Hanoi!")
    print("Goal: Move all disks from column 1 to column 2 or 3.")
    print("Rule: A larger disk may never be placed on top of a smaller disk.")
    print("Type 'q' or 'quit' at any prompt to exit.\n")

    game = HanoiGame(num_disks=3)

    while True:
        game.display()
        if game.is_won():
            print(f"🎉 CONGRATULATIONS! You solved Tower of Hanoi in {game.moves_count} moves!")
            break

        src_input = input("Choose column to pull top disk from (1, 2, 3): ").strip().lower()
        if src_input in ('q', 'quit', 'exit'):
            print("Game exited.")
            break

        dst_input = input("Choose column to move disk to (1, 2, 3): ").strip().lower()
        if dst_input in ('q', 'quit', 'exit'):
            print("Game exited.")
            break

        game.move_disk(src_input, dst_input)

def main():
    play_hanoi()

if __name__ == '__main__':
    main()