import math
from scipy import optimize
from matplotlib import pyplot as plt
import numpy as np

def parseResults(filename):
	f=open(filename, "r")
	fl =f.readlines()
	delta_i_global = []
	probability = []
	for x in fl:
		l = x.split('\t')
		delta_i_global.append(float(l[1]))
		try:
			probability.append(float(l[2]))
		except ValueError:
			probability.append(0)

	return delta_i_global, probability

delta_i_global, probability = parseResults("Farhad 22-06-2019 21-51-22.txt")	

x = np.linspace(-4,4,1000) 
x_to_zero = np.linspace(-4,0,1000)

def U(x, delta_i, alpha):
	b = -delta_i / alpha
	return np.power(x,4)/4 - np.power(x,2)/2+b*x

def ro(x, delta_i, alpha, D):
	  #return U(x, delta_i, alpha)
		return np.exp(-2 * U(x, delta_i, alpha) / D)

def p_estimated(delta_i, alpha, D):
	global x, x_to_zero

	y = ro(x,delta_i, alpha, D)

	integral1 = np.trapz(y,x)
	A = 1 / integral1

	y_to_zero = ro(x_to_zero, delta_i, alpha, D)

	#plt.plot(x_to_zero,y_to_zero)
	#plt.show()

	my_ro = A * np.trapz(y_to_zero, x_to_zero)	

	#print(my_ro)

	return my_ro	

def my_error(vars):
	error = 0

	alpha = vars[0]
	D = vars[1]

	if alpha < 0 or alpha > 2.5 or D > 1.5 or D < 0:
		return 1000

	for index, delta_i in enumerate(delta_i_global):

		p_estimated_val = p_estimated(delta_i, alpha, D) 

		error += np.square(probability[index] - p_estimated_val)

	return error

x0 = np.array([1.25, 0.75]) # in the middle. First is aplha and second is D

res = optimize.minimize(my_error, x0, method='powell',
    options={'xtol': 1e-8, 'disp': True})
print(res.x)

true_alpha = res.x[0]
true_D = res.x[1]
D_p = true_alpha * true_D

print('alpha ' + str(true_alpha))
print('D ' + str(true_D))

print('noise intensity ' + str(D_p))

plt.scatter(delta_i_global, probability)

delta_i_continuos = np.linspace(-0.5,0.5,1000) 
p_min = []
for delta_i in delta_i_continuos:
	#print(p_estimated(delta_i, true_alpha, true_D))
	p_min.append(p_estimated(delta_i, true_alpha, true_D))

plt.plot(delta_i_continuos, p_min)
plt.show()
#plt.plot(x,y)
#plt.show()




