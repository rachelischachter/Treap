# BSD
# I hereby certify that this program is solely the result of my own work and is in compliance with the Academic Integrity policy of the course syllabus and the academic integrity policy of the CS department.

import pytest
import random

#random.seed(1)     # seed is very helpful for testing because you can see where things go wrong

class Treap(object): 
    
    # The Node object for each node in the Treap. Each node has a key and stored data. 
    # Each node also has a randomly assigned priority and can point to a left and right child
    
    class Node(object):
        def __init__(self, key, data, left=None, right=None):
            self.key = key
            self.data =  data
            self.priority = random.random()
            self.leftChild = left
            self.rightChild = right 
        
        # String method for each node: prints out the node: { (key, data) | priority }
        def __str__(self):
            return "{ (" + str(self.key) + ", " + str(self.data) + ") | " + str(self.priority) + "}"
        

    # Creates an empty treap with just one attribute- self.__root that points to the root node
    def __init__(self):
        self.__root = None
    
        
    # A method that checks if the Treap is empty. Returns True if Treap is empty and False if not. Used for testing
    def isEmpty(self):
        return self.__root is None
    
    # Returns the key of the root. Used for testing
    def getRootKey(self):
        return self.__root.key
    
    # Used to generate the node being inserted. Can be used in testing
    def __generateNode(self, key, data):
        return self.Node(key, data)    

    # Insert method to insert a Node into the Treap. It takes two parameters- a key and data. 
    # The method returns True upon successfully inserting a new Node into the Treap.
    # Re-inserting a key will result in updating the data associated with that key and will return False
    
    # Wrapper method for the insertion
    def insert(self, key, data):
        
        # self.__root is the new treap, flag is if the insertion was successful or not
        node = self.__generateNode(key, data)
        self.__root, flag = self.__insert(self.__root, node) 
        # return True if a new Node was inserted, otherwise False if an existing Node was updated
        return flag 
    
    # Recursively insert a Node into the treap. The node is first inserted based on the 
    # Binary Search Tree condition with smaller keys to the left and larger keys to the right
    # Next, the Heap condition is tested and the notes rotate until the condition is met
    # This method accepts two parameters: root is the parent and curNode is the node we are inserting
    # This method returns a tuple- the root node and True/False based on if the insertion was successful
    
    def __insert(self, root, curNode): 
        
        # if the tree is empty, create the node and return new root and success. 
        if root is None: 
            return curNode, True
        
        # if the key already exists, update the data but maintain the current priority and return False 
        if curNode.key == root.key:
            root.data = curNode.data
            curNode.priority = root.priority
            return root, False 
        

        # if the key belongs to the left of the current parent 
        elif curNode.key < root.key:
            # recursively insert
            root.leftChild, flag = self.__insert(root.leftChild, curNode)
            
            
            # Check heap condition
            if curNode.priority > root.priority:
                # print("rotating RIGHT because cn =", curNode.priority, "and root is", root.priority)                
                root = self.__rotateRight(root)
                
        
        # if key is bigger, insert to the right of the parent 
        else:
            root.rightChild, flag = self.__insert(root.rightChild, curNode)
            
            # Check heap condition
            if curNode.priority > root.priority:
                # print("rotating LEFT because cn =", curNode.priority, "and root is", root.priority)                
                root = self.__rotateLeft(root)
        
        # return the node and if it was successful or not
        return root, flag 
    
    
    # Rotation methods to keep the Treap balanced:
    # Method to move the node that is rooted at the top to the left (counter clockwise)
    def __rotateLeft(self, top):
        toRaise = top.rightChild              # store the right child that is going to be raised
        top.rightChild = toRaise.leftChild    # reset the top's right children
        toRaise.leftChild = top               # reset the right child's left child 
        
        # returns the raised node to update parent
        return toRaise  
    
    def __rotateRight(self, top):
        toRaise = top.leftChild               # store the left child that is going to be raised
        top.leftChild = toRaise.rightChild    # reset the top's left children
        toRaise.rightChild = top              # reset the left child's right child
        
        # returns the raised node to update parent
        return toRaise
    
    # This method finds the data associated with a particlar key. 
    # If they key exists, returns the data. If the key does not exist, returns None
    def find(self, key):
        parent, node, status = self.__find(key, self.__root)
            
        # regular find, returns data associated with particular key
        if node: return node.data      
    
    # Iteratively traverse tree until you reach desired Node
    def __find(self, key, node):
        parent = None
        status = "root"
        while node is not None: 
            # if you hit the exact node
            # return the parent, the actual node, and where the node is located if found (right/left)
            if node.key == key: return parent, node, status        
            
            # look to the left if key is smaller than current node
            elif key < node.key:                                   
                parent = node
                status = "left"
                node = node.leftChild  
                
            # look to the right if key is bigger    
            else:                                                   
                parent = node
                status = "right"
                node = node.rightChild                 

        # fall out of loop if you reach the end and key still has not been found
        return None, None, None                   
    

    # A special wrapper method that is used by the delete function.
    # Returns parent node, target node, and which child the target node is.
    # If the node does not exist, return None, None, None 
    
    def __delFind(self, key):
        parent, node, status = self.__find(key, self.__root)
        if node: return parent, node, status
        else: return None, None, None        

    # This function deletes a specificed key. Returns True upon successfully deleting the key
    # Returns False if the key is not in the Tree
        
    def delete(self, key, root = "start"):
        # find the key using the special version of the find function
        parent, toDelete, status = self.__delFind(key)
        
       # print("STATS: Parent:", parent, " Deleting:", toDelete.key, " Right/Left?", status)
        
        # if node doesn't exist, return False 
        if not toDelete: 
            # print("Key does not exist")
            return False
        
        # if the tree only contains root 
        if status == "root" and not (toDelete.leftChild or toDelete.rightChild):
            self.__root = None
            return True        
        
        # Otherwise, change the Priority to be -1 to start the trickle down
        # Because priority is determined by random.random() the lowest possible priority is always greater than -1 
        toDelete.priority = -1

        # Trickle down by having the node switch spots with the child with higher priority. The node  
        # Loop until the node reaches the bottom (fall out of loop when node has no children i.e. is a leaf)
        while toDelete.leftChild or toDelete.rightChild: 
            
            # Determine which direction to rotate in to trickle down:
            # The node will swap places with whichever child has the highest priority
            
            # if there is only a left child or if the left child has a higher priority than right child, rotate right (left child becomes new root)
            if not toDelete.rightChild or (toDelete.leftChild and toDelete.leftChild.priority > toDelete.rightChild.priority): 
                # keep track of which child it is to reconnect parent
                if status == "root":
                    self.__root = self.__rotateRight(toDelete)
                    parent = self.__root
                    
                elif status == "right":
                    parent.rightChild = self.__rotateRight(toDelete)
                    parent = parent.rightChild 
                    
                else:
                    parent.leftChild = self.__rotateRight(toDelete)
                    parent = parent.leftChild 
                
                # toDelete is now the right child   
                status = "right"
            
            # if there is only a right child or the right child is greater, rightChild becomes new root 
            else: 
                if status == "root":
                    self.__root = self.__rotateLeft(toDelete)
                    parent = self.__root
                    
                elif status == "right":
                    parent.rightChild = self.__rotateLeft(toDelete)
                    parent = parent.rightChild
                    
                else: 
                    parent.leftChild = self.__rotateLeft(toDelete)
                    parent = parent.leftChild
                
                # toDelete is now the left child   
                status = "left"                    
            
            #self.printTreap()   
        # fall out of the loop when it is finally a node
        # trim off the approrpiate child of the last parent
        # print("Deleting:", toDelete.key, "Parent: ", parent, "Right/left?", status)
        
        if status == "left":
            parent.leftChild = None
            return True
        
        else:
            parent.rightChild = None
            return True
        
        # self.printTreap()
     
        
    # Recursively print out the tree
    
    # wrapper method- start at the root
    def printTreap(self):
        self.__pTreap(self.__root, "ROOT:  ", "")
        print()
        
    def __pTreap(self, node, kind, indent):
        # print the proper indentation, and what child it is 
        print("\n" + indent + kind, end="")
        if node:   
            print(node, end="")
            if node.leftChild:
                self.__pTreap(node.leftChild,  "LEFT:   ",  indent + "    ")
            if node.rightChild:
                self.__pTreap(node.rightChild, "RIGHT:  ", indent + "    ") 
        
    # Asserts that the Heap condition is satisfied- each parent is of a higher priority than all children
    # Returns True if the heap condition is satisfied 
    
    def isHeap(self, node = "start"):
        # start from the root
        if node == "start": node = self.__root
        # if heap is empty 
        if not node: return True
        # check left child
        if node.leftChild: return node.leftChild.priority < node.priority
        # check right child
        if node.rightChild: return node.rightChild.priority < node.priority
        # recurse
        return self.isHeap(node.leftChild) and self.isHeap(node.rightChild)
   
    # Asserts that the Binary Search Tree condition is satisfied
    # all nodes to the left of a parent are smaller
    # all nodes to the right of a parent are larger
    # Returns True if the condition is satsfied 
    
    def isBST(self, node = "start"):
        # start from the root
        if node == "start": node = self.__root
        # if heap is empty
        if not node: return True
        # check left child
        if node.leftChild: return node.leftChild.key < node.key
        # check right child
        if node.rightChild: return node.rightChild.key > node.key
        # recurse
        return self.isBST(node.leftChild) and self.isBST(node.rightChild) 
    
    # Asserts that both BST and Heap conditions are satisfied
    def isTreap(self):
        return self.isBST() and self.isHeap()
    
################################# TESTING ######################################
        
# Function to generate array of random "words". 
# Returns an array of size-many words
def randomWords(size):
    words = []
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for i in range(size):
        word = ""
        for j in range(random.randint(1,10)):
            # make a random j-letter word
            word += letters[random.randint(0,25)]
        words += [word]
        
    return words 

# Function to make trees with a randomized keys. 
# This function returns a Treap and a dictionary with all of the key-data pairs in the treap
def makeTreap(size):
    keys = randomWords(size)
    dict = {}
    trp = Treap()
    for i in range(size):
        data = random.randint(1,50)
        trp.insert(keys[i], data)
        dict[keys[i]] = data

    return trp, dict   


# Test insert and find- make sure all words are properly inserted into the treap by finding them after 
def test_find_small():
    # make a treap
    t, dict = makeTreap(10)
    # make sure the treap is a treap
    assert t.isTreap()
    # make sure all inserted keys are in the treap with the correct data
    for key in dict:
        assert dict[key] == t.find(key) 
        
# Test insert and find on a much larger scale- repeat 100 times with Treaps with ~1000 elements        
def test_find_torture():
    for i in range(100):
        t, dict = makeTreap(1000) 
        assert t.isTreap()
        for key in dict:
            assert dict[key] == t.find(key)  
            
# Test the find method on an empty Treap. Should return None
def test_find_empty():
    t = Treap()
    assert t.find("Not there") is None

# Test the find method using keys that are not in the Treap. Should return None   
def test_find_notThere():
    t, dict = makeTreap(1000)
    for key in dict:
        searchKey = key + str(1)            # create a key that is for sure not in the dictionary/treap
        assert t.find(searchKey) is None    # make sure that it doesn't exist
        
# Torture test to make sure the insert method is working correctly
def test_insert_torture():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Repeat this 100 times
    for i in range(100):
        t = Treap()                                   # make a Treap
        keys = []                                     # Dictionary for all of the words
        for j in range(100):                          # make 100 random words
            data = random.randint(1,500)
            word = ""
            for len in range(4):                      # each word is 4 letters
                word += letters[random.randint(0,25)]
            if word not in keys:                      # if it's a new word
                assert t.insert(word, data)           # insert it into the Treap
                keys += [word]                        # add it to the seen words
            else:                                     # if it's an old word, 
                assert t.insert(word, data) == False  # insert must return False
            
            assert t.isTreap()                        # make sure Treap conditions are satisfied
            
# Test to make sure that duplicate insertions update the data and maintain treap condition but return False
def test_insertDups():
    t = Treap()
    # make sure the inserts are successful
    assert t.insert("BSD", 18)
    assert t.insert("TYH", 26)
    assert t.insert("Treap", 100)
    # these inserts should return False because they are duplicates
    assert t.insert("BSD", 123) == False 
    assert t.insert("TYH", 2626) == False
    assert t.insert("Treap", 200) == False
    # assert that the data is updated
    assert t.find("BSD") == 123
    assert t.find("TYH") == 2626
    assert t.find("Treap") == 200
    # assert that Treap condition is satisfied
    assert t.isTreap()
    
def test_insertDups_torture():
    for i in range(10):
        t, dict = makeTreap(100)                         # Make Treaps
        assert t.isTreap()                               
        for key in dict:                                 # Attempt to re-insert existing keys
            assert t.insert(key, dict[key]+1) == False   # Assert that insert returns False
            assert t.find(key) == dict[key]+1            # Assert that data is updated
            assert t.isTreap()                           # Assert that Heap condition is satisfied

# Test to delete the root of a Treap
def test_deleteRoot_torture():
    for i in range(100):  
        # make a treap
        t, dict = makeTreap(10)
        # get the root
        root = t.getRootKey()
        assert t.delete(root) 
        
# Torture test to delete all elements from a Treap. Must result in an empty Treap
def test_delete_torture():
    for i in range(100):
        # make treap of size 100 
        t, dict = makeTreap(100)
        assert t.isTreap()
        # if the key exists, make sure it deletes
        for key in dict:
            if t.find(key):
                assert t.delete(key) 
        assert t.isEmpty()
        
# Test to delete from an empty Treap. Deletion will fail and return False. Treap should remain empty 
def test_deleteEmpty():
    t = Treap()
    assert t.isEmpty()
    assert t.delete("hello") == False
    assert t.delete("world") == False
    assert t.isEmpty()
    assert t.isTreap()

# Test to delete from a Treap with just a single element
def test_deleteSingle():
    for i in range(10):
        t = Treap()
        key = str(random.randint(1,1000))
        t.insert(key, 1)
        t.delete(key)
        assert t.isEmpty()

# Test to delete keys that are not in the Treap
def test_delete_notThere_torture():
    t, dict = makeTreap(100)
    for key in dict:
        fakeKey = key + str(1)             # Create a key that is for sure not in the dictionary/treap
        assert t.delete(fakeKey) == False  # Make sure that the delete fails    

pytest.main(["-v", "-s", "Treap.py"])