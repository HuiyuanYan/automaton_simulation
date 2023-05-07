import copy
from typing import List,Set,Tuple,Any
class multi_key_dict:
    def __init__(self,key_num = 1) -> None:
        """
        Initialize a multi-key dictionary.
        Args:
            key_num (int, optional):the number of keys. Defaults to 1.
        """
        assert key_num >= 1
        self.__key_num = key_num
        self.__dict = dict()
        self.__keys = set()
        pass

    def set_value(self,keys:tuple,val)->None:
        """Set the value of multi_key_dict[key_1][key_2]...[key_n].

        Args:
            keys (tuple): A tuple that contains keys in order. Its length must be equal to the number of keys.
            val (_type_): Value.
        """
        assert len(keys) == self.__key_num
        d = self.__dict
        for i in range(0,self.__key_num-1):
            key = keys[i]
            if key not in d:
                d[key] = dict()
            d = d[key]
        d[keys[self.__key_num -1]] = val
        self.__keys.add(keys)        

    def get_value(self,keys:tuple)->Any:
        """Get the value of multi_key_dict[key_1][key_2]...[key_n].

        Args:
            keys (tuple): A tuple that contains keys in order. Its length must be equal to the number of keys.
        """
        assert len(keys) == self.__key_num
        d = self.__dict
        for i in range(0,self.__key_num):
            d = d[keys[i]]
        return d

    def keys(self)->Set[tuple]:
        """Get all keys of the multi_key_dict.
        """
        return self.__keys.copy()
    
    def values(self)->List[Any]:
        """Get all values of the multi_key_dict.
        """
        values = []
        for key in self.__keys:
            values.append(self.get_value(key))
        return values

    def items(self)->List[Tuple[Tuple,Any]]:
        """Get set of all "(keys,val)" in multi_key_dict.
        """
        mutli_keys_dict_items = []
        for key in self.__keys:
            print(key)
            val = self.get_value(key)
            print(val)
            mutli_keys_dict_items.append((key,val))
        return mutli_keys_dict_items
    
    def __contains__(self,keys:tuple)->bool:
        """Check whether the given multi_key is in the dict.

        Args:
            keys (tuple): A tuple that contains keys in order. Its length must be equal to the number of keys.

        Returns:
            bool: The result.
        """
        assert len(keys) == self.__key_num
        if keys in self.__keys:
            return True
        return False
    
    def clear(self)->None:
        """Clear all the "keys-val" pairs in the dict.

        Note that the number of keys is not reset.
        """
        self.__dict.clear()
        self.__keys.clear()
    
    def keys_num(self)->int:
        """Get the number of keys.
        """ 
        return self.__key_num
    
    def __str__(self) -> str:
        items = self.items()
        s = str()
        for key,val in items:
            s += f'{key} : {val}\n'
        return s
    
    def copy(self):
        """Return a deep copy of this dict.
        """
        copy.deepcopy(self)        


def test_multi_key_dict():
    d = multi_key_dict(3)
    l = [('a','b','c'),('d','e','f'),('g','h','i'),('g','h','j')]

    # test 'set_value' and 'get_value'
    for i in range(0,len(l)):
        d.set_value(l[i],i)
        assert d.get_value(l[i]) == i
    
    # test 'keys'
    keys = d.keys()
    for elem in l:
        assert elem in keys
    
    # test 'values':
    values = d.values()
    for i in range(0,len(l)):
        assert i in values
    
    # test 'items':
    items = d.items()
    for i in range(0,len(l)):
        assert (l[i],i) in items

    # test 'in':
    for elem in l:
        assert elem in d

    # test 'clear':
    d.clear()
    assert len(d.keys()) == 0

    print('Test passed!')

def test():
    a = multi_key_dict(3)
    a.set_value(('q','a','X'),{('p','Y')})
    s = a.get_value(('q','a','X'))
    s.add(('r','Z'))
    print(a.items())

def test2():
    a = multi_key_dict(2)
    a.set_value(('1','2'),[])
    print(a)
if __name__ == '__main__':
    test_multi_key_dict()
    test2()