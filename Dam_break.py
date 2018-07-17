from numpy import *
import matplotlib.pyplot as plotting

print("1D DAM BREAK PROBLEM")

f = open("INPUT.txt", "r")
data = f.readlines()
f.close()
f_out = open("OUTPUT.txt", "w")

# input data from file
# d0 = initial water depth before dam break
# d1 = water depth downstream of channel
# v1 = velocity of water downstream of channel
# t = time of analysis after dam break
d0 = float(data[3])
d1 = float(data[5])
v1 = float(data[7])
time = data[9].split(',')
total_time = len(time)
length_ds = float(data[11])


t = [0.0 for i in range(total_time)]
for i in range(0,total_time,1):
    t[i] = float(time[i])

# calculating depth of water with positive surge, d2 meter using empirical formula of Hubert Chanson
d2 = d0 * 0.9319671 * (d1 / d0) ** 0.371396

print("Depth of water with positive surge, d2 in meter")
print(d2)

# calculating velocity of water with positive surge, v2 in m/s using MOC
v2 = 2 * (sqrt(9.81 * d0) - sqrt(9.81 * d2))

print("Flow velocity of water with positive surge, V2 m/s")
print(v2)

# calculating absolute wave velocity with positive surge, U m/s
# using continuity equation on either side of positive surge
U = (d2 * v2 - d1 * v1) / (d2 - d1)

print("Absolute wave velocity of positive surge, U m/s")
print(U)

# calculating time for a given distance d/s at which the positive surge front will reach
time_of_p_surge_front = (length_ds * 1000 / (U-v1))/60
print("Time for positive surge front to reach is")
print(time_of_p_surge_front)

# calculating positive surge front height
positive_surge_height = d2 - d1

# writing positive surge height to file
f_out.write("Positive surge front height = ")
f_out.write(str(round(positive_surge_height,2)))
f_out.write(" meter")
f_out.write("\n")

# writing time of positive surge front to reach given d/s distance to file
f_out.write("Time for positive surge front to reach ")
f_out.write(str(length_ds))
f_out.write(" km d/s = ")
f_out.write(str(round(time_of_p_surge_front,2)))
f_out.write(" minutes")
f_out.write("\n")
f_out.write("--------------------------")
f_out.write("\n")

# writing heading to file
f_out.write("X_km")
f_out.write("\t")
f_out.write("Depth_m")
f_out.write("\n")

for j in range(0, total_time, 1):

    # calculating distance of leading edge of negative wave, xE1 in km
    xE1 = - sqrt(9.81 * d0) * (t[j] * 60) / 1000
    print("Distance of leading edge of negative wave from original dam position, xE1 in km")
    print(xE1)

    # calculating distance of trailing edge of negative wave, xE2 in km
    xE2 = (v2 - sqrt(9.81 * d2)) * (t[j] * 60) / 1000
    print("Distance of trailing edge of negative wave from original dam position, xE2 in km")
    print(xE2)

    # calculating distance of leading edge of positive wave, xE2 in km
    xE3 = (U - v1) * (t[j] * 60) / 1000
    print("Distance of leading edge of positive wave from original dam position, xE3 in km")
    print(xE3)

    # Parabolic profile of negative wave, within E1 and E2
    # l = length of negative wave = xE2-xE1 in km
    l = int((xE2 - xE1))
    print("l")
    print(l)

    x = [0.0 for i in range(l + 2)]
    x[0] = xE1
    last_index = 0
    for i in range(1,l + 1,1):
        x[i] = x[i-1] + 1
        last_index = i

    x[last_index+1] = xE2
    print("last index")
    print(last_index)
    print("x")
    print(x)

    # finding depth of negative wave, parabolic
    d = [0.0 for i in range(l + 2)]
    for i in range(0,l + 2, 1):
        d[i] = (1 / (3 * sqrt(9.81)) * (2 * sqrt(9.81 * d0) - x[i] * 1000 / (t[j] * 60))) ** 2

    print("d")
    print(d)

    # plotting profile
    # original profile before dam break
    x0 = [0.0 for i in range(2)]
    d_initial = [0.0 for i in range(2)]
    x0[1] = xE1
    x0[0] = x0[1] - 6

    d_initial[1] = d[0]
    d_initial[0] = d0

    # original depth plot
    plotting.plot(x0, d_initial)

    # negative wave profile
    plotting.plot(x, d)

    # for positive surge
    xps = [0.0 for i in range(3)]
    dps = [0.0 for i in range(3)]

    xps[0] = xE2
    xps[1] = xE3
    xps[2] = xE3

    dps[0] = d[l+1]
    dps[1] = d[l+1]
    dps[2] = d1

    # positive surge plot
    plotting.plot(xps, dps)

    xs = [0.0 for i in range(2)]
    ds = [0.0 for i in range(2)]

    xs[0] = xE3
    xs[1] = xs[0] + 6

    ds[0] = d1
    ds[1] = d1

    # downstream water plot
    plotting.plot(xs, ds)

    # writing original profile to file
    f_out.write("Profile at ")
    f_out.write(str(t[j]))
    f_out.write(" minutes")
    f_out.write("\n")
    f_out.write("---------------------------")
    f_out.write("\n")
    f_out.write("original profile")
    f_out.write("\n")
    for p in range(0, 2, 1):
        f_out.write(str(round(x0[p],2)))
        f_out.write("\t")
        f_out.write(str(round(d_initial[p], 2)))
        f_out.write("\n")

    # writing negative wave to file
    f_out.write("Negative wave")
    f_out.write("\n")
    for p in range(0, l + 2, 1):
        f_out.write(str(round(x[p],2)))
        f_out.write("\t")
        f_out.write(str(round(d[p], 2)))
        f_out.write("\n")

    # writing positive wave to file
    f_out.write("Positive surge")
    f_out.write("\n")
    for p in range(0, 2, 1):
        f_out.write(str(round(xps[p],2)))
        f_out.write("\t")
        f_out.write(str(round(dps[p], 2)))
        f_out.write("\n")

    # writing Downstream water profile to file
    f_out.write("Downstream water profile")
    f_out.write("\n")
    for p in range(0, 2, 1):
        f_out.write(str(round(xs[p], 2)))
        f_out.write("\t")
        f_out.write(str(round(ds[p], 2)))
        f_out.write("\n")

    f_out.write("--------------------------")
    f_out.write("\n")

    plotting.title("Profile after " + str(t[j]) + " minutes of Dam break")
    plotting.xlabel("Distance, km")
    plotting.legend(['Initial water depth','Negative wave','Positive Surge','Downstream water'])
    plotting.ylabel("Depth, meter")
    plotting.grid(True)
    plotting.savefig("Profile_dam_break" + str(t[j]) + ".png", bbox_inches="tight")
    plotting.show()
