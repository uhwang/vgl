import numpy as np

def create_cylinder(r, jpan, ipan, zmin, zmax):
	jpnt = jpan+1
	ipnt = ipan+1
	twopi= 2*np.pi
	dthe = twopi/(ipan)
	geom = np.zeros((jpnt,ipnt,3),dtype=np.float32)
	dz = (zmax-zmin)/jpan

	for j in range(jpnt):
		z = zmin + j*dz
		for i in range(ipnt):
			the = i * dthe
			x = r*np.cos(the)
			y = r*np.sin(the)
			geom[j][i][0] = x
			geom[j][i][1] = y
			geom[j][i][2] = z
				
	return geom
