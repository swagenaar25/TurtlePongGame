"""
Author: Sam Wagenaar
Created: May 26, 2022
Modified: May 26, 2022
Purpose: review the year
Class: Intro to Programming
"""
import turtle
import throttle

timer = throttle.Throttle(60)
# Setup the game board
wn = turtle.Screen()  # Window
wn.title("Pong Game")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.delay(0)

score_a = 0
score_b = 0

# Setup turtle a (left)
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)
paddle_a.side = "left"

# Setup turtle b (right)
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("red")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)
paddle_b.side = "right"

# Setup ball
ball = turtle.Turtle()
ball.speed(0)
ball.speed(0)
ball.shape("square")
ball.color("yellow")
ball.penup()
ball.goto(0, 0)
ball.dx = ball.dy = 2

# Setup pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("orange")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))


def correct_paddles():
    paddle_a.sety(min(300, max(-300, int(paddle_a.ycor()))))
    paddle_b.sety(min(300, max(-300, int(paddle_b.ycor()))))


def paddle_a_up():
    y = paddle_a.ycor()
    paddle_a.sety(y + 20)
    correct_paddles()


def paddle_a_down():
    y = paddle_a.ycor()
    paddle_a.sety(y - 20)
    correct_paddles()


def paddle_b_up():
    y = paddle_b.ycor()
    paddle_b.sety(y + 20)
    correct_paddles()


def paddle_b_down():
    y = paddle_b.ycor()
    paddle_b.sety(y - 20)
    correct_paddles()


wn.listen()
wn.onkey(paddle_a_up, "w")
wn.onkey(paddle_a_down, "s")

wn.onkey(paddle_b_up, "Up")
wn.onkey(paddle_b_down, "Down")

kg = True


def close():
    global kg
    kg = False
    wn.bye()


wn.onkey(close, "Escape")


def formatted_shape(sprite: turtle.Turtle):
    """Finds shape of turtle
    :return (min_x, min_y), (max_x, max_y)
    """
    shape = sprite.get_shapepoly()
    max_x = -float("inf")
    min_x = float("inf")
    max_y = -float("inf")
    min_y = float("inf")
    for coord in shape:
        x, y = coord[1], coord[0]
        max_x = max(x, max_x)
        max_y = max(y, max_y)

        min_x = min(x, min_x)
        min_y = min(y, min_y)
    return (min_x, min_y), (max_x, max_y)


border_pad = 5
# Main Game Loop
while kg:
    wn.update()

    # move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    ball_min, ball_max = formatted_shape(ball)
    ball_width = abs(ball_max[0] - ball_min[0])
    ball_height = abs(ball_max[1] - ball_min[1])

    paddle_a.min, paddle_a.max = formatted_shape(paddle_a)
    paddle_a_width = abs(paddle_a.max[0] - paddle_a.min[0])
    paddle_a_height = abs(paddle_a.max[1] - paddle_a.min[1])

    paddle_b.min, paddle_b.max = formatted_shape(paddle_b)
    paddle_b_width = abs(paddle_b.max[0] - paddle_b.min[0])
    paddle_b_height = abs(paddle_b.max[1] - paddle_b.min[1])
    # Border checking
    if ball.ycor() + ball_max[1] > 300 - border_pad:
        ball.sety((300 - border_pad) - ball_max[1])
        ball.dy = -abs(ball.dy)

    if ball.ycor() + ball_min[1] < -300:
        ball.sety((-300) - ball_min[1])
        ball.dy = abs(ball.dy)

    if ball.xcor() + ball_max[0] > 400 - border_pad:
        ball.goto(0, 0)
        ball.dx = -abs(ball.dx)
        score_a += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

    if ball.xcor() + ball_min[0] < -400:
        ball.goto(0, 0)
        ball.dx = abs(ball.dx)
        score_b += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

    # Paddle and ball collisions
    # Check that ball y is between paddle y
    if (abs(ball.ycor() - paddle_a.ycor()) < max(ball_height/2, paddle_a_height/2)) and\
            ((ball.xcor()+ball_min[0]) < (paddle_a.xcor()+paddle_a.max[0])):  # Left -x
        ball.setx(paddle_a.xcor()+paddle_a.max[0]-ball_min[0])
        ball.dx = abs(ball.dx)

    if (abs(ball.ycor() - paddle_b.ycor()) < max(ball_height/2, paddle_b_height/2)) and\
            ((ball.xcor()+ball_max[0]) > (paddle_b.xcor()+paddle_b.min[0])):  # Right +x
        ball.setx(paddle_b.xcor()+paddle_b.min[0]-ball_max[0])
        ball.dx = -abs(ball.dx)
    timer.limit()
