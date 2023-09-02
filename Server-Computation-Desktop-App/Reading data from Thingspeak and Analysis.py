import requests
import numpy as np
from scipy.optimize import minimize
from tkinter import *
import time

root=Tk()
root.geometry("650x300")
root.title("Driver Assistance Panel")
root.iconbitmap("download.ico")
myLabel=Label(root,text="STATS PANEL",font=('Times', 24))
myLabel.pack()

frame=LabelFrame(root,text="Frame",padx=15,pady=15)
frame.pack(padx=10,pady=10)

#Reading Data
READ_API_KEY='HO0ILNAB5VLATXXE'
CHANNEL_ID= '2030387'

a=requests.get("https://api.thingspeak.com/channels/2030703/feeds.json?results=30")
d=a.json()
l=d['feeds']
field1_data=[]   #ACC
field2_data=[]   #Vel
field3_data=[]   #Brake
field4_data=[]   #Lat
field5_data=[]   #Lon
for i in l:
    for j in ["field1","field2","field3","field4","field5"]:
        if i[j]==None:
            pass
        else:
            if j=="field1":
                field1_data.append(i[j])
            elif j=="field2":
                field2_data.append(i[j])
            elif j=="field3":
                field3_data.append(i[j])
            elif j=="field4":
                field4_data.append(i[j])
            elif j=="field5":
                field5_data.append(i[j])

myLabel1=Label(frame,text="Current Acceleration ")
myLabel1.grid(row=0,column=0)
ml1=Label(frame,text=str(field1_data[0]))
ml1.grid(row=0,column=1)
el1=Label(frame,text="All Fine")
el1.grid(row=0,column=2)
myLabel1=Label(frame,text="Current Velocity ")
myLabel1.grid(row=1,column=0)
ml2=Label(frame,text=str(field2_data[0]))
ml2.grid(row=1,column=1)
el2=Label(frame,text="All Fine")
el2.grid(row=1,column=2)
myLabel2=Label(frame,text="Braking Levels")
myLabel2.grid(row=2,column=0)
ml3=Label(frame,text=len("You are braking too many times")*" ")
ml3.grid(row=2,column=1)
el3=Label(frame, text="All Fine")
el3.grid(row=2,column=2)
myLabel3=Label(frame,text="GPS-Latitude")
myLabel3.grid(row=3,column=0)
ml4=Label(frame,text=str(field4_data[0]))
ml4.grid(row=3,column=1)
myLabel4=Label(frame,text="GPS-Longitude")
myLabel4.grid(row=4,column=0)
ml5=Label(frame,text=str(field5_data[0]))
ml5.grid(row=4,column=1)
i1=i2=i3=i4=i5=0
ml1.after(3000,lambda: update1(i1))
ml2.after(3000,lambda: update2(i2))
ml3.after(3000,lambda: update3(i3))
ml4.after(3000,lambda: update4(i4))
ml5.after(3000,lambda: update5(i5))

def update1(i1):
    i1+=1
    try:
        ml1.config(text=field1_data[i1])
        el1.config(text="All Fine")
        if float(field1_data[i1])>1.4705:
            el1.config(text="Exceeding acceleration limit of 1.4705 m/s2")
        if i1<6:
            ml1.after(3000,lambda: update1(i1))
    except:
        pass
def update2(i2):
    i2+=1
    try:
        ml2.config(text=field2_data[i2])
        el2.config(text="All Fine")
        if float(field2_data[i2])>90:
            el2.config(text="Exceeding velocity limit of 25 m/s")
        if i2<6:
            ml2.after(3000,lambda: update2(i2))
    except:
        pass
def update3(i3):
    i3+=1
    try:
        if int(field3_data[i3])==1 and int(field3_data[i3-1])==1 and int(field3_data[i3-2])==1:
            el3.config(text="You are braking too many times")

        else:
            el3.config(text="All Fine")
    except:
        pass
    if i3<6:
        ml3.after(3000,lambda: update3(i3))
def update4(i4):
    i4+=1
    try:
        ml4.config(text=field4_data[i4])
        if i4<6:
            ml4.after(3000,lambda: update4(i4))
    except:
        pass
def update5(i5):
    i5+=1
    try:
        ml5.config(text=field5_data[i5])
        if i5<6:
            ml5.after(3000,lambda: update5(i5))
    except:
        pass


# Algorithm to suggest optimal acceleration such that least amount of fuel is consumed, this agorithm kicks into motion every 18 seconds
def objective(x, *params):
    current_velocity, current_acceleration, current_position, target_velocity, surrounding_vehicles = params
    desired_acceleration = np.array([x[0], x[1]])
    desired_velocity = current_velocity + desired_acceleration
    future_position = current_position + desired_velocity
    cost = np.linalg.norm(target_velocity - desired_velocity)
    for sv in surrounding_vehicles:
        relative_position = sv[0] - future_position
        relative_velocity = sv[1] - desired_velocity
        relative_acceleration = sv[2]
        if np.linalg.norm(relative_velocity) < 0 and np.linalg.norm(relative_acceleration) > 0:
            cost += np.linalg.norm(relative_velocity) * np.linalg.norm(relative_acceleration) / np.linalg.norm(relative_position)
    return cost

def optimize_acceleration(current_velocity, current_acceleration, current_position, target_velocity, surrounding_vehicles):
    params = (current_velocity, current_acceleration, current_position, target_velocity, surrounding_vehicles)
    initial_guess = [0.0, 0.0]
    result = minimize(objective, initial_guess, args=params, method='SLSQP')
    return result.x

current_velocity = np.array([0,5])
current_acceleration = np.array([0,0.2])
current_position = np.array([0, 0])
target_velocity = np.array([0,7])
surrounding_vehicles = [
    (np.array([0, -30]), np.array([0,10]), np.array([0,0.2])),
    (np.array([4, 7]), np.array([0,19]), np.array([0,-0.4])),
    (np.array([6, -5]), np.array([0,25]), np.array([0,0.3])),
    (np.array([-3, 0]), np.array([0,20]), np.array([0, 0])),
    (np.array([-4, -2]), np.array([0,5]), np.array([0, 0.2]))
]

optimal_acceleration_x, optimal_acceleration_y = optimize_acceleration(current_velocity, current_acceleration, current_position, target_velocity, surrounding_vehicles)

l23=Label(frame, text="Suggested Acceleration (For best fuel efficiency): ")
l23.grid(row=5,column=0,columnspan=2)


if optimal_acceleration_x>optimal_acceleration_y and optimal_acceleration_x>0:
    l231=Label(frame,text="SLIDE RIGHT AT "+str(round((((optimal_acceleration_x)**2+(optimal_acceleration_y)**2)**0.5),4))+" m/s2")
    l231.grid(row=5,column=2)

if optimal_acceleration_x>optimal_acceleration_y and optimal_acceleration_x<0:
    l231=Label(frame,text="SLIDE LEFT AT "+str(round((((optimal_acceleration_x)**2+(optimal_acceleration_y)**2)**0.5),4))+" m/s2")
    l231.grid(row=5,column=2)
if optimal_acceleration_y>optimal_acceleration_x and optimal_acceleration_y>0:
    l231=Label(frame,text="SPEED UP FORWARD AT  "+str(round((((optimal_acceleration_x)**2+(optimal_acceleration_y)**2)**0.5),4))+" m/s2")
    l231.grid(row=5,column=2)
if optimal_acceleration_y>optimal_acceleration_x and optimal_acceleration_y<0:
    l231=Label(frame,text="SLOW DOWN AT "+str(round((((optimal_acceleration_x)**2+(optimal_acceleration_y)**2)**0.5),4))+" m/s2")
    l231.grid(row=5,column=2)
    

from scipy.optimize import curve_fit

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

acceleration = np.linspace(-1.4705,1.4705, num=100)
fuel_consumed = quadratic(acceleration, 2, -3, 4) + np.random.normal(0, 0.5, 100)
acc=round((((optimal_acceleration_x)**2+(optimal_acceleration_y)**2)**0.5),4)
params, covariance = curve_fit(quadratic, acceleration, fuel_consumed)

a, b, c = params
print("You are consuming the least amount of fuel possible given the circumstances: ",quadratic(acc,a,b,c))
l232=Label(frame,text="You are consuming the least amount of fuel possible given the circumstances: "+str(round(quadratic(acc,a,b,c),4))+ " ml of fuel")
l232.grid(row=6,column=0,columnspan=3)




root.mainloop()