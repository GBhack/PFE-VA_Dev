#!/usr/bin/python

spacing = 100
maxValue = 1550
f = open('workfile', 'w')
valeurs=["GND","GND","GPIO_38","GPIO_39","GPIO_34","GPIO_35","GPIO_66","GPIO_67","GPIO_69","GPIO_68","GPIO_45","GPIO_44","EHRPWM2B","GPIO_26","GPIO_47","GPIO_46","GPIO_27","GPIO_65","GPIO_22","GPIO_63","GPIO_62","GPIO_37","GPIO_36","GPIO_33","GPIO_32","GPIO_61","GPIO_86","GPIO_88","GPIO_87","GPIO_89","GPIO_10","GPIO_11","GPIO_09","GPIO_81","GPIO_08","GPIO_80","GPIO_78","GPIO_79","GPIO_76","GPIO_77","GPIO_74","GPIO_75","GPIO_72","GPIO_73","GPIO_70","GPIO_71"]
for i in range(0,46):
	position = maxValue -(spacing*(i+1))
	stringToWrite = "X " + valeurs[i] + " 8" +str(i+1)+" -750 " +str(position)+" 200 L 50 50 1 1 P\n"
	print(stringToWrite)
	f.write(stringToWrite)

f.close()
