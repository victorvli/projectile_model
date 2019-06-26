# SAFE INPUT FOR FLOATING POINT NUMBERS
import math
import matplotlib.pyplot as plt
import numpy as np
from graphics import *


# -------------------------------------------------------------------------------------------- #
def show_title():
    # show title
    print("\n===========================================================")
    print("=================  Projectile  Simulator  =================")
    print("===========================================================\n")


# -------------------------------------------------------------------------------------------- #
def show_menu():
    print("\n* * * * * * * * * * * *  MENU LIST  * * * * * * * * * * * *")
    print("  1.enter system parameters and simulation properties")
    print("  2.calculate simulation data")
    print("  3.display simulation data")
    print("  4.save simulation data to file")
    print("  5.plot the movements")
    print("  6.animate the movements")
    print("  q.quit")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")


# -------------------------------------------------------------------------------------------- #
def my_get_float(prompt, default):
    # this is a safe way to get a float from user
    try:
        value = float(input(prompt))
        return value
    except ValueError:
        print("invalid input, using default value ", default)
        return default


# -------------------------------------------------------------------------------------------- #
# get value of parameters
# -------------------------------------------------------------------------------------------- #
def get_parameters():
    # this gets the system parameters from the user
    m = my_get_float("mass(default is 1.0 kg):", 1.0)
    g = my_get_float("gravity_acceleration(default is 9.8 m/s^2):", 9.8)
    h = my_get_float("height(default is 200.0 m):", 200.0)
    v = my_get_float("velocity(default is 100.0 m/s):", 100.0)
    ag = math.radians(my_get_float("angle(default is 60 degrees):", 60))
    k = my_get_float("drag_coefficient(default is 0.005):", 0.005)
    dt = my_get_float("time_step(default is 0.2 s):", 0.2)
    tt = my_get_float("total_time(default is 15 s):", 15)

    return m, g, h, v, ag, k, dt, tt


# -------------------------------------------------------------------------------------------- #
# get value of parameters
# -------------------------------------------------------------------------------------------- #
def get_default_parameters():
    # this gets the system parameters from the user
    print("no input detected, using default value")
    m = 1.0
    g = 9.8
    h = 200.0
    v = 100.0
    ag = math.radians(60)
    k = 0.005
    dt = 0.2
    tt = 15

    return m, g, h, v, ag, k, dt, tt


# -------------------------------------------------------------------------------------------- #
# show current system parameters
# -------------------------------------------------------------------------------------------- #
def show_parameters(m, g, h, v, ag, k, dt, tt):
    print("\n----------------- Show Parameters Value -------------------")
    print("      *    mass ....................... %6.5f (kg)" % m)
    print("      *    gravity_acceleration ....... %6.5f (m/s^2)" % g)
    print("      *    height ..................... %6.5f (m)" % h)
    print("      *    velocity ................... %6.5f (m/s)" % v)
    print("      *    angle ...................... %6.5f (degrees)" % math.degrees(ag))
    print("      *    drag_coefficient ........... %6.5f" % k)
    print("      *    time_step .................. %6.5f (s)" % dt)
    print("      *    total_time ................. %6.5f (s)" % tt)
    print("-----------------------------------------------------------\n")


# -------------------------------------------------------------------------------------------- #
def calculations(m, g, h, v, ag, k, dt, tt):
    # Set up the lists to store variables
    # Initialize the arr_velocity and position at t=0
    t = [0]    # list to keep track of time
    x = [0]    # list for x and y position
    y = [0]
    vv = [v]   # list for velocity
    aa = []    # list for acceleration
    gg = [ag]

    max_height = 0.0
    max_length = 0.0
    vel = 0.0
    tim = 0.0

    # list for velocity x and y components
    vx = [v * np.cos(ag)]
    vy = [v * np.sin(ag)]

    # drag force
    drag = k * v ** 2

    # Acceleration components
    ax = [-(drag * np.cos(ag)) / m]
    ay = [-g - (drag * np.sin(ag) / m)]
    aa.append(np.sqrt(ax[0] ** 2 + ay[0] ** 2))

    print("calculating data ...")

    # init index and do loop
    i = 0
    while t[i] <= tt and y[i] >= -h:
        # increase index
        i = i + 1

        # increase time
        t.append(t[i - 1] + dt)  # increment by dt and add to the list of time
        tim = t[i]

        # update arr_velocity
        vx.append(vx[i - 1] + dt * ax[i - 1])  # Update the arr_velocity
        vy.append(vy[i - 1] + dt * ay[i - 1])

        # update position
        x.append(x[i - 1] + vx[i - 1] * dt + 0.5 * ax[i - 1] * dt ** 2)
        y.append(y[i - 1] + vy[i - 1] * dt + 0.5 * ay[i - 1] * dt ** 2)

        max_length = x[i]
        if y[i] > max_height:
            max_height = y[i]

        # update angle
        ang = math.atan2(vy[i - 1], vx[i - 1])
        gg.append(ang)

        # with the new arr_velocity calculate the drag force and update acceleration
        vel = np.sqrt(vx[i] ** 2 + vy[i] ** 2)  # magnitude of arr_velocity
        vv.append(vel)
        drag = k * vel ** 2  # drag force
        ax.append(-(drag * np.cos(ang)) / m)
        ay.append(-g - (drag * np.sin(ang) / m))
        aa.append(np.sqrt(ax[i] ** 2 + ay[i] ** 2))

    print("calculations complete")
    print("-*- max height = ", max_height)
    print("-*- max length = ", max_length)
    print("-*- total time = ", tim)
    print("-*- final velocity = ", vel)
    input("enter to continue")

    return t, x, y, vv, aa, gg


# -------------------------------------------------------------------------------------------- #
def show_data(t, x, y, vv, aa, gg):
    for i in range(0, len(t)):
        print("i = %d  time = %4.2f  x = %4.2f  y = %4.2f  velocity = %4.2f  acceleration = %4.2f  angle = %4.2f" %
              (i, t[i], x[i], y[i], vv[i], aa[i], gg[i]))

    input("enter to continue")


# -------------------------------------------------------------------------------------------- #
def save_data(t, x, y, vv, aa, gg):

    filename = "projectile_sim.csv"
    f = open(filename, "w")
    header_string = "i,time,x,y,velocity,acceleration,angle\n"
    f.write(header_string)

    for i in range(0, len(t)):
        data_string = "%d,%6.5e,%6.5e,%6.5e,%6.5e,%6.5e,%6.5e\n" % (i, t[i], x[i], y[i], vv[i], aa[i], gg[i])
        f.write(data_string)

    f.close()

    print("file saved to %s" % filename)
    input("enter to continue")


# -------------------------------------------------------------------------------------------- #
def plot(x, y):
    # Let's plot the trajectory
    # plt.plot(x, y)
    plt.ylabel("y (m)")
    plt.xlabel("x (m)")
    plt.title("Projectile Simulation Data")
    plt.ion()

    print("plot show")
    plt.plot(x, y)
    plt.show()
    plt.pause(10)
    # input("enter to continue")
    plt.close('all')
    print("plot close")


# -------------------------------------------------------------------------------------------- #
# SHOW ANIMATION
# -------------------------------------------------------------------------------------------- #
def animate(t, x, y, dt):
    # create window
    win = GraphWin("Projectile Animation", 800, 500)
    win.setBackground("white")

    # create text arr_time
    message = Text(Point(400, 50), "press any key to continue")
    message.draw(win)

    # wait for key press
    win.getKey()

    # do animation
    i = 0
    check_key = ""
    while (i < len(t)) and (check_key is""):
        check_key = win.checkKey()

        # show current arr_time and angle
        message.setText("i=%d,  x=%f,  y=%f" % (i, x[i], y[i]))

        start_time = time.time()

        # create ball
        ball = Circle(Point(250 + x[i], 250 - y[i]), 5)
        ball.draw(win)

        # create line
        if i > 0:
            line = Line(Point(250 + x[i - 1], 250 - y[i - 1]), Point(250 + x[i], 250 - y[i]))
            line.draw(win)

        # delay
        elapsed_t = time.time() - start_time
        if elapsed_t < dt:
            time.sleep(dt - elapsed_t)

        # undraw ball
        ball.undraw()

        i = i + 1

    message.setText("press any key to exit")

    # wait for key press
    win.getKey()

    # close window
    win.close()


# -------------------------------------------------------------------------------------------- #
# MAIN PROGRAM
# -------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    menu_option = ""

    arr_t = []
    arr_x = []
    arr_y = []
    arr_vel = []
    arr_acc = []
    arr_ang = []

    mass = 0.0
    gravity_acc = 0.0
    height = 0.0
    velocity = 0.0
    angle = 0.0
    drag_cff = 0.0
    time_step = 0.0
    total_time = 0.0

    # show title
    show_title()

    while menu_option is not "q":
        # clear screen
        os.system("clear")

        # show menu
        show_menu()

        # get option
        menu_option = input("Enter option > ")

        if menu_option is "1":
            mass, gravity_acc, height, velocity, angle, drag_cff, time_step, total_time = get_parameters()
            show_parameters(mass, gravity_acc, height, velocity, angle, drag_cff, time_step, total_time)
        elif menu_option is "2":
            if mass == 0:
                mass, gravity_acc, height, velocity, angle, drag_cff, time_step, total_time = get_default_parameters()
                show_parameters(mass, gravity_acc, height, velocity, angle, drag_cff, time_step, total_time)
            arr_t, arr_x, arr_y, arr_vel, arr_acc, arr_ang = calculations(mass, gravity_acc, height, velocity, angle,
                                                                          drag_cff, time_step, total_time)
        elif menu_option is "3":
            show_data(arr_t, arr_x, arr_y, arr_vel, arr_acc, arr_ang)
        elif menu_option is "4":
            save_data(arr_t, arr_x, arr_y, arr_vel, arr_acc, arr_ang)
        elif menu_option is "5":
            plot(arr_x, arr_y)
        elif menu_option is '6':
            animate(arr_t, arr_x, arr_y, time_step)
        elif menu_option is "q":
            print("\n===========================================================")
            print("========== Thanks for using Projectile Simulator ==========")
            print("===========================================================\n")
        else:
            print("Invalid option, try again!")

    print("Goodbye...")
