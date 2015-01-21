import libdeps

mydp = libdeps.DepMgr()
mydp.add_dependency('net','netdev')
mydp.add_dependency('server','net')
mydp.add_dependency('client','net')
mydp.add_dependency('script','server')
