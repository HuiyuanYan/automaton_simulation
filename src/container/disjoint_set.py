import copy

class DisjointSet:
    def __init__(self,data_list):
        self.__parent = {}
        self.__rank = {}
        self.sets_count = len(data_list)
        
        for d in data_list:
            self.__parent[d]=d
            self.__rank[d] = 1
    
    def find(self,d):
        """Find the root of data d \n
        Method : CollapsingFind

        Args:
            d : data,must be in the data set of the DS
        Return:
            root of d
        """
        assert d in self.__parent

        root = d
        while self.__parent[root] != root:
            root = self.__parent[root]
        while d != root:
            temp = self.__parent[d]
            self.__parent[d] = root
            d = temp
        return root

    def union(self,a,b):
        """Merge the set of data a and the set of data b.

        Args:
            a ,b : data,must be in the data set of the DS
        """
        assert a in self.__parent
        assert b in self.__parent
        
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a != root_b:
            rank_a = self.__rank[root_a]
            rank_b = self.__rank[root_b]
            if rank_a >= rank_b:
                self.__parent[root_b] = root_a
                if rank_a == rank_b:
                    self.__rank[root_a] += 1
            else:
                self.__parent[root_a] = root_b
        self.sets_count -= 1

    def get_set_list(self)->list:
        """Get sets of DS

        Returns:
            list: sets of DS
        """
        set_list = []
        for (key,val) in self.__parent.items():
            if key == val:
                #root
                set_list.append([copy.deepcopy(key)])
        
        for data in self.__parent.keys():
            pa = self.find(data)
            if pa != data:
                for l in set_list:
                    if pa in l:
                        l.append(data)

        return set_list

    
    def parent(self):
        return copy.deepcopy(self.__parent)
    
    def rank(self):
        return copy.deepcopy(self.__rank)
    
if __name__ == '__main__':
    ds = DisjointSet(['a','b','c','d'])
    ds.union('a','b')
    ds.union('b','d')
    print(ds.parent())
    print(ds.rank())
    print(ds.get_set_list())