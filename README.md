# ChessAI
Most of these games which are zero sum in nature work on the minimax algorithm. In this project I have implemented a minimax algorithm and some interesting computer vision to track pieces.
# Capturing the Board
Taking a screenshot of the screen and finding the square with the largest area helps us find our chess board.
# Tracking the pieces
An initial state of a standard chess board is saved in the memory. The first screenshot which is taken saves the picture of each piece with its corresponding position on the board.
Each piece is converted to a black and white mask and saved in a dictionary with their name
# Bitwise AND and OR in images
![Bitwise AND](https://github.com/user-attachments/assets/a867f9bf-14e1-43db-8c1f-2e4feb6dc86a)
![Bitwise OR](https://github.com/user-attachments/assets/63b041e1-14d4-4cfb-980d-fd58669e1bf5)\
Credits for the images: https://pyimagesearch.com/
# Recognising pieces
Each piece is put against the stored pieces in the dictionary where we perform some basic math. (Formula used: (SAVED_PIECE OR PIECE)-(SAVED_PIECE AND PIECE). If these 2 images are equal then the bitwise OR and the bitwise AND would be the same output. Hence subtracting them would lead to near 0 white pixels hence confirming which piece it is.
# Moving the cursor
Moving the cursor and clicks are handled by a python library called pyautogui
# Working project
![Working Video](https://github.com/user-attachments/assets/4dbb50a5-05c4-42aa-9cf7-c1680189fde0)\
On the left side is the original chess board and on the right is the cv2 output with the pieces marked.
