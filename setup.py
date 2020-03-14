from setuptools import setup, find_packages
 
setup(name='vgl',
	
	version='0.1',
	
	url='https://github.com/uhwang/vgl',
	
	license='None',
	
	author='Uisang Hwang',
	
	author_email='uhwangtx@gmail.com',
	
	description='Vector Graphic Library',
	
	packages=find_packages(),
	
	install_requires = ['pygame', 'aggdraw', 'numpy', 'pillow', 'pycairo', 'moviepy'],
	
	classifiers      = ['Programming Language :: Python :: 3.7',
                        'Intended Audience :: Everybody'#,
                        #'License :: OSI Approved :: Closed Sorce Software'
						]
    )
	#packages=find_packages(exclude=['tests']),
	
	#long_description=open('README.md').read(),
	
	#zip_safe=False,
	
	#setup_requires=['nose>=1.0'],
	
	#test_suite='nose.collector')