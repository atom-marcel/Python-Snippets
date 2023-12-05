from typing import Dict, List, Any, TypedDict, Callable
from Data_Manipulation.cfg import Cfg

class Node:
    key: str | int
    value: Dict = {}
    left: 'Node' = None
    right: 'Node' = None

    def __init__(self, key: str | int):
        self.key = key
        self.value = {}

    def setValue(self, value: Dict):
        self.value = value

    def getValue(self):
        return self.value
    
    def compare(self, node: 'Node'):
        if(node.key < self.key):
            return -1
        if(node.key > self.key):
            return 1

        return 0

    def __eq__(self, __value: 'Node') -> bool:
        if self.key == __value.key:
            return True
        
        return False
    
    def compareKey(self, key: str | int):
        if(key < self.key):
            return -1
        if(key > self.key):
            return 1

        return 0


class Tree:
    root: Node

    def __init__(self, root: Node):
        self.root = root

    def insertOrdered(self, node: Node, top: Node = None):
        if not top:
            top = self.root

        cmp: int = top.compare(node)
        if(cmp < 0):
            if(top.left):
                self.insertOrdered(node, top.left)
            else:
                top.left = node
        else:
            if(top.right):
                self.insertOrdered(node, top.right)
            else:
                top.right = node

    def getValue(self, key: str | int, top: Node = None):
        if not top:
            top = self.root

        if(top.key == key):
            return top.value
        
        cmp: int = top.compareKey(key)
        if(cmp < 0):
            if(top.left):
                return self.getValue(key, top.left)
            else:
                print(f"Key '{key}' not found in tree.")
        else:
            if(top.right):
                return self.getValue(key, top.right)
            else:
                print(f"Key '{key}' not found in tree.")

    def getNodes(self, top: Node = None, nodes: int = 1):        
        if not top:
            top = self.root

        if(top.left):
            nodes = self.getDepth(top.left, nodes + 1)
        if(top.right):
            nodes = self.getDepth(top.right, nodes + 1)

        return nodes
    
    def getDepth(self, top: Node = None, depth: int = 1, maxDepth: int = 1):
        if not top:
            top = self.root

        if(top.left):
            maxDepth = self.getDepth(top.left, depth + 1, maxDepth)
        if(top.right):
            maxDepth = self.getDepth(top.right, depth + 1, maxDepth)

        if(depth > maxDepth):
            maxDepth = depth

        return maxDepth
    
    def print(self, node: Node = None):
        if not node:
            node = self.root

        print("(", end="")
        if(node.left):
            self.print(node.left)
        else:
            print("_", end="")
        
        print(f", {node.key}, ", end="")

        if(node.right):
            self.print(node.right)
        else:
            print("_", end="")
        print(")", end="")

    def toCfg(key: str | int, value: Dict, args: List):
        key = str(key)
        v = {}
        for x in value.keys():
            v[str(x)] = str(value[x])

        dc = { key: v}
        
        for x in dc.keys():
            args[0].information[x] = dc[x]

        return dc
    
    def CfgToTree(self, cfg: Cfg):
        for key in cfg.information.keys():
            node = Node(key)
            node.value = cfg.information[key]
            if self.root:
                self.insertOrdered(node)
            else:
                self.root = node

    def iterate(self, operation: Callable, args: List = [], node: Node = None):
        if not node:
            node = self.root

        if(node.left):
            self.iterate(operation, args, node.left)
        if(node.right):
            self.iterate(operation, args, node.right)

        return operation(node.key, node.value, args)