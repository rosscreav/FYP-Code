input =[19,19,19,19,19,19,19,19,19,19,19,19,19,20,20,20,20,20,20,20,20,20,20,20,21,21,21,21,21,21,22,22,22,22,22,22,23,23,23,23,24,24,24,24,24,25,25,25,26,26,27,27,27,28,28,28,29,29,30,30,31,32,32,32,33,34,34,35,35,35,34,34,33,33,32,32,31,31,30,30,29,29,28,28,28,27,27,27,26,26,26,26,25,25,25,24,24,24,24,24,24,24,24,23,23,23,23,23,23,23,23,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,23,23,23,23,23,23,23,24,24,24,24,24,24,25,25,25,25,26,26,26,26,27,27,27,28,28,28,29,29,30,30,31,31,32,32,33,33,34,35,35,36,37,38,38,40,40,41,42,44,45,46,47,48,50,52,53,54,54,54,53,52,52,51,50,50,49,49,49,48,48,47,47,46,46,46,46,45,45,45,44,44,44,44,44,44,44,43,43,43,43,43,-3,-3,41,42,43,43,43,43,43,43,44,44,44,44,44,44,45,45,45,46,46,46,46,47,46,44,42,40,38,36,34,33,31,30,29,27,26,25,24,24,23,22,21,20,20,19,18,18,17,17,16,16,15,15,14,14,13,13,13,12,12,12,13,13,13,14,15,15,16,16,17,18,19,20,21,22,23,24,25,26,27,29,30,32,34,36,38,39,40,39,39,39,39,38,38,38,38,38,38,38,38,37,37,37,37,37,37,37,37,37,36,36,37,37,37,37,37,37,38,38,38,38,38,38,38,39,39,39,39,39,40,40,40,40,41,41,41,42,42,42,43,43,44,44,44,45,45,46,46,46,47,47,46,45,44,43,42,41,40,39,38,37,36,36,35,34,34,33,32,32,31,31,30,30,29,29,28,28,27,27,27,26,26,26,25,25,25,24,24,24,24,23,23,23,23,22,22,22,22,21,21,21,21,21,21,20,20,20,20,20,20,20,20,19,19,19,19]

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def plot(input):
	angle = 360/len(input)
	curangle = 0
	x=[]
	y=[]
	for dist in input:
		if dist != -3:
			x.append((dist+18) * math.cos(math.radians(curangle)))
			y.append((dist+18) * math.sin(math.radians(curangle)))
		curangle+= angle
	#yhat = np.convolve(y, box, mode='same')
	plt.scatter(x, smooth(y,3))
	plt.scatter([0],[0],color='red')
	plt.text(0, 0+2, 'Robot Postion')
	plt.savefig('/Flask/static/images/map.png')


if __name__ == '__main__':
	input= list(filter((-3).__ne__, input))
	plot(input)
	#draw()