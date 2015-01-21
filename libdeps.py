class DependencyException(Exception):
    pass

class DepMgr(object):
    def __init__(self):
        self.dependency_map = dict()
        self.installed = set()

    def add_dependency(self, subj, dep):
        if not self.dependency_map.has_key(subj):
            self.dependency_map[subj] = set()

        self.dependency_map[subj].add(dep)

    def remove_dependency(self, subj, dep):
        if self.dependency_map.has_key(subj):
            try:
                self.dependency_map[subj].remove(dep)
            except KeyError:
                pass

    def dependsp(self, subj, dep):
        if self.dependency_map.has_key(subj):
            return (dep in self.dependency_map[subj])
        return False

    def get_direct_depends(self, subj):
        if self.dependency_map.has_key(subj):
            return set(self.dependency_map[subj])
        return set()


    def get_dependency_tree(self, subj, installed=False, rem=set(), depth=10):
        """return a set of all dependencies for subj. installed flag indicates we only want a set of ones that aren't installed."""
        if depth <= 0:
            return set()
        if not self.dependency_map.has_key(subj):
            return set()
        ret = set(self.dependency_map[subj])
        localrem = set(rem)
        localrem.add(subj)
        for dep in self.dependency_map[subj]:
            if dep in rem:
                continue
            ret.update(self.get_dependency_tree(dep, installed, localrem, depth-1))
            localrem.add(dep)
        if installed:
            ret.difference_update(self.installed)
        return ret

    def get_rev_dependency_tree(self, subj, installed=False, rem=set(), depth=10):
        """return a set of all packages which depend on this one."""
        if installed:
            startset = set(self.installed)
        else:
            startset = set(self.dependency_map.keys())

        ret = set()
        localrem = set(rem)
        for dep in startset:
            if dep in rem:
                continue
            if self.dependsp(dep, subj):
                ret.add(dep)
                ret.update(self.get_rev_dependency_tree(dep, installed, localrem, depth-1))
                localrem.add(dep)
        return ret

    def install(self, subj):
        """install a single subj if dependencies are already met."""
        depset = self.get_direct_depends(subj).difference(self.installed)
        if depset:
            raise DependencyException("missing dependencies: %s" % str(depset))

        self.installed.add(subj)

    def remove(self, subj):
        """remove a single subj if possible. Return a set of subjs which depend on this subj."""
        if not subj in self.installed:
            return set()

        depset = self.get_rev_dependency_tree(subj, True)

        if depset:
            raise DependencyException("still dependend upon: %s" % str(depset))

        self.installed.remove(subj)
