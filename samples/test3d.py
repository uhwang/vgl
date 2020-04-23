import view3d 
import pygame 
from pygame.locals import *
import numpy as np
from operator import itemgetter
import pyquaternion as pyq
from vgl import Data, Frame

def convertToComputerFrame(self, point):
	computerFrameChangeMatrix = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]])
	return np.matmul(computerFrameChangeMatrix, point)
		
# Node stores each point of the block
class Node:
    def __init__(self, coordinates, color):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.color = color

# Face stores 4 nodes that make up a face of the block
class Face:
    def __init__(self, nodes, color):
        self.nodeIndexes = nodes
        self.color = color

# Wireframe stores the details of the block
class Wireframe:
	def __init__(self):
		self.nodes = []
		self.edges = []
		self.faces = []

	def addNodes(self, nodeList, colorList):
		for node, color in zip(nodeList, colorList):
			self.nodes.append(Node(node, color))

	def addFaces(self, faceList, colorList):
		for indexes, color in zip(faceList, colorList):
			self.faces.append(Face(indexes, color))

	#def quatRotate(self, w, dt):
	#    self.quaternion.rotate(w, dt)

	#def rotatePoint(self, point):
	#    rotationMat = quat.getRotMat(self.quaternion.q)
	#    return np.matmul(rotationMat, point)
	#
	def convertToComputerFrame(self, point):
		computerFrameChangeMatrix = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]])
		return np.matmul(computerFrameChangeMatrix, point)

	def getAttitude(self):
		return quat.getEulerAngles(self.quaternion.q)

	def outputNodes(self):
		print("\n --- Nodes --- ")
		for i, node in enumerate(self.nodes):
			print(" %d: (%.2f, %.2f, %.2f) \t Color: (%d, %d, %d)" %
				(i, node.x, node.y, node.z, node.color[0], node.color[1], node.color[2]))

	def outputFaces(self):
		print("\n --- Faces --- ")
		for i, face in enumerate(self.faces):
			print("Face %d:" % i)
			print("Color: (%d, %d, %d)" % (face.color[0], face.color[1], face.color[2]))
			for nodeIndex in face.nodeIndexes:
				print("\tNode %d" % nodeIndex)
				
class test3d():
	def __init__(self, width, height, wireframe):
		self.frm = Frame(0,0,0,3,3,Data(-1,1,-1,1,-1,1))
		self.width = width
		self.height = height
		self.wireframe = wireframe
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('Attitude Determination using Quaternions')
		self.background = (10,10,50)
		self.clock = pygame.time.Clock()
		pygame.font.init()
		self.m_xRotate = 1.5;
		self.m_yRotate = 0;
		self.old_pos = (0,0)
		self.move = False
		self.v3d = view3d.View3d(self.frm)
		self.lbutton = False
		
	def display(self):
		if not self.lbutton and not self.move:return
		
		self.screen.fill(self.background)
		
		# Transform nodes to perspective view
		dist = 5
		pvNodes = []
		pvDepth = []
		for node in self.wireframe.nodes:
			point = [node.x, node.y, node.z]
			newCoord = self.v3d.rotate_point(point)
			comFrameCoord = self.wireframe.convertToComputerFrame(newCoord)
			#pvNode.append(self.projectOthorgraphic(comFrameCoord[0], comFrameCoord[1], comFrameCoord[2],
			#										self.screen.get_width(), self.screen.get_height(),
			#										70, pvDepth))
			#print(type(dot), dot)
			#pygame.draw.circle(self.screen, (255,10,10), (int(dot[0]), int(dot[1])), 3, 0)
			
			pvNodes.append(self.projectOnePointPerspective(comFrameCoord[0], comFrameCoord[1], comFrameCoord[2],self.screen.get_width(), self.screen.get_height(),	5, 10, 20, pvDepth))
			
		
		# Calculate the average Z values of each face.
		avg_z = []
		for face in self.wireframe.faces:
			n = pvDepth
			z = (n[face.nodeIndexes[0]] + n[face.nodeIndexes[1]] +
				n[face.nodeIndexes[2]] + n[face.nodeIndexes[3]]) / 4.0
			avg_z.append(z)

		# Draw the faces using the Painter's algorithm:
		for idx, val in sorted(enumerate(avg_z), key=itemgetter(1)):
			face = self.wireframe.faces[idx]
			pointList = [pvNodes[face.nodeIndexes[0]],
						pvNodes[face.nodeIndexes[1]],
						pvNodes[face.nodeIndexes[2]],
						pvNodes[face.nodeIndexes[3]]]
			pygame.draw.polygon(self.screen, face.color, pointList)
			
	def projectOnePointPerspective(self, x,y,z,win_width, win_height, P, S, scaling_constant, pvDepth):
		# In Pygame, the y axis is downward pointing.
		# In order to make y point upwards, a rotation around x axis by 180 degrees is needed.
		# This will result in y' = -y and z' = -z
		xPrime = x
		yPrime = -y
		zPrime = -z
		xProjected = xPrime * (S/(zPrime+P)) * scaling_constant + win_width / 2
		yProjected = yPrime * (S/(zPrime+P)) * scaling_constant + win_height / 2
		pvDepth.append(1/(zPrime+P))
		return (round(xProjected), round(yProjected))
		
	def projectOthorgraphic(self, x, y, z, win_width, win_height, scaling_constant, pvDepth):
		# In Pygame, the y axis is downward pointing.
		# In order to make y point upwards, a rotation around x axis by 180 degrees is needed.
		# This will result in y' = -y and z' = -z
		xPrime = x
		yPrime = -y
		xProjected = xPrime * scaling_constant + win_width / 2
		yProjected = yPrime * scaling_constant + win_height / 2
		# Note that there is no negative sign here because our rotation to computer frame
		# assumes that the computer frame is x-right, y-up, z-out
		# so this z-coordinate below is already in the outward direction
		pvDepth.append(z)
		
		#return (round(xProjected), round(yProjected))
		return (xProjected, yProjected)
		
	def run(self):
		""" Create a pygame screen until it is closed. """
		running = True
		loopRate = 50
		angularVeloctiy = [0.25, 0.25, 0.25]
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.old_pos = event.pos
					self.lbutton = True
				elif event.type == pygame.MOUSEMOTION:
					if self.lbutton:
						self.move = True
						self.cur_mouse_pos = event.pos
						self.m_yRotate -= self.old_pos[0]-self.cur_mouse_pos[0]
						self.m_xRotate += self.old_pos[1]-self.cur_mouse_pos[1]
						self.v3d.xrotation(self.m_xRotate)
						self.v3d.yrotation(self.m_yRotate)
						self.old_pos = event.pos
				elif event.type == pygame.MOUSEBUTTONUP:
					self.lbutton = False
					self.move = False
	
			self.clock.tick(loopRate)
			self.display()
			pygame.display.flip()
			
def initializeCube():
    block = Wireframe()

    block_nodes = [(x, y, z) for x in (-1.5, 1.5) for y in (-1.5, 1.5) for z in (-1.5, 1.5)]
    node_colors = [(255, 255, 255)] * len(block_nodes)
    block.addNodes(block_nodes, node_colors)
    block.outputNodes()

    faces = [(0, 2, 6, 4), (0, 1, 3, 2), (1, 3, 7, 5), (4, 5, 7, 6), (2, 3, 7, 6), (0, 1, 5, 4)]
    colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0)]
    block.addFaces(faces, colors)
    block.outputFaces()

    return block
	
				
if __name__ == '__main__':
    block = initializeCube()
    pv = test3d(640, 480, block)
    pv.run()