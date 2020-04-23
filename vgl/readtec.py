# readtec.py
# 4/23/20
# Import Tecplot data file

import vgl

class ImportTecfile():
	def __init__(self, fname):
		self.fp = open(fname, "rt")
		
	def get_mesh(self):
		#mesh = vgl.mesh3d.SuareMesh()
		return

