import numpy as np

def create_sphere(r, jpan, ipan):
	jpnt = jpan+1
	ipnt = ipan+1
	twopi= 2*np.pi
	pi_2 = np.pi*0.5
	dphi = twopi/(jpan)
	dthe = twopi/(ipan)
	geom = np.zeros((jpnt,ipnt,3),dtype=np.float32)
	ang = 0
	for j in range(jpnt):
		#start = pi_2 if math.fabs(ang-twopi) < 0.001 else 0
		#phi = start+j * dphi
		#ang = phi
		phi = j*dphi
		for i in range(ipnt):
			the = i*dthe
			x = r*np.cos(phi)*np.cos(the)
			y = r*np.cos(phi)*np.sin(the)
			z = r*np.sin(phi)
			geom[j][i][0] = x
			geom[j][i][1] = y
			geom[j][i][2] = z
	return geom
	
