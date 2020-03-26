from vgl import color

def create_color_table(H1, H2, S, V, order):
	cbtl = [(0,0,0)]*order
	dH, tempH=0,0
	
	if H1 > H2:
		H1, H2 = H2, H1

	dH = (H2 - H1)/order
	tempH = H1

	for i in range(order):
		cbtl[i] = color.hsv(tempH, S, V)
		tempH += dH;

	return cbtl
	
#print(create_color_table(0,240, 0.8,1,53))