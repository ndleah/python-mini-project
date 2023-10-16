<h1 align="center">⚫ Othello/Reversi ⚪ </h1>

A two-player, GUI-equipped, [Othello/Reversi](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english) game made in **Python3** using the `pygame` library.

## 📜 Description
Othello is a board-game played on a 8x8 board, with 64 discs that are black on one side and white on the other. Each player gets 32 such discs, out of which 2 from each player are kept on the board in the following manner:

![image](https://github.com/TERNION-1121/Othello-Reversi-Game/assets/97667653/ea03fdd8-9abc-4b14-bdc9-7d983fb38041)

<br>

A move consists of "outflanking" your opponent's disc(s), then flipping the "outflanked" disc(s) to your color.
To outflank means, if your disc is kept on square X, and you have another disc on square Y, such that:
- X and Y lie on the same row, or
- X and Y lie on the same column, or
- X and Y lie on the same diagonal,

If any one (or more) of the above is the case while playing, then the Opponent's discs between X and Y get flipped to your color.

<br>

Example:

> Here White disc A was already present on the board, after placing White disc B, the row of Black discs between White disc A and B got outflanked,

![06a8330dc692b7631a2e50660e4a7346](https://github.com/TERNION-1121/Othello-Reversi-Game/assets/97667653/84feed70-ee16-4f4f-baad-39a3ecc148ed)

> And thus the outflanked Black discs flipped to White.

![cd51ed676fb49538035a8bf006ffbe96](https://github.com/TERNION-1121/Othello-Reversi-Game/assets/97667653/bafe9059-7a32-4d93-aaa2-bfc97a311fce)

For a more comprehensive explanation of the game rules, check out this [link](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english).


### How to Play the Game 🎮
1. Download the source code
2. Make sure to install Python3 on your Computer along with `pip`
3. Install the `numpy` and `pygame` libraries. To do this, open the terminal and type `pip install numpy` and `pip install pygame`. 
4. Run the `main.py` file and play the game!

## Author
This Project was Contributed by [Vikrant Singh Bhadouriya](https://www.github.com/TERNION-1121). 

Thanks for your kind attention!