# Course: CS261 - Data Structures
# Student Name: Joseph Minefee
# Assignment:  Assignment 3 - Max_Stack
# Description: Implement a Stack ADT class by completing the skeleton code.


from sll import *


class StackException(Exception):
    """
    Custom exception to be used by MaxStack Class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MaxStack:
    def __init__(self):
        """
        Init new MaxStack based on Singly Linked Lists
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.sll_val = LinkedList()
        self.sll_max = LinkedList()

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "MAX STACK: " + str(self.sll_val.length()) + " elements. "
        out += str(self.sll_val)
        return out

    def is_empty(self) -> bool:
        """
        Return True is Maxstack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.sll_val.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the MaxStack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.sll_val.length()

    # ------------------------------------------------------------------ #

    def push(self, value: object) -> None:
        """
        Adds a new element to the top of the stack.
        """
        # Uses the LinkedList class method add to front to add new elements to the top of the stack. If the stack is
        # empty, the value is added to both sll_val and sll_max.
        if self.is_empty() is True:
            self.sll_val.add_front(value)
            self.sll_max.add_front(value)
        # If the stack isn't empty, the value at the head of the stack is recorded. The new value is always added to
        # the sll_val linked list, but the new value is only added to sll_max if the new value is greater than the head
        # value. Else, the current head value is repeated.
        else:
            val = self.sll_max.get_front()
            self.sll_val.add_front(value)
            if value > self.sll_max.get_front():
                self.sll_max.add_front(value)
            else:
                self.sll_max.add_front(val)

    def pop(self) -> object:
        """
        This method removes the top element from a stack and returns its value.
        """
        # Checks if stack is empty. If it is, it raises the StackException.
        if self.sll_val.is_empty() is True:
            raise StackException
        # Else, it assigns val to the top value of the stack, removes the top element from both sll_val and sll_max, and
        # returns val.
        else:
            val = self.sll_val.get_front()
            self.sll_val.remove_front()
            self.sll_max.remove_front()
            return val

    def top(self) -> object:
        """
        Returns the value of the top element of the stack without removing it.
        """
        # Checks if stack is empty. If it is, it raises the StackException.
        if self.sll_val.is_empty() is True:
            raise StackException
        # Else, it assigns val to the top value of the stack, removes the top element, and returns val.
        else:
            return self.sll_val.get_front()

    def get_max(self) -> object:
        """
        Returns the maximum value currently stored in the stack. Returns an exception if the stack is empty.
        """
        # Checks if stack is empty. If it is, it raises the StackException.
        if self.sll_max.is_empty() is True:
            raise StackException
        else:
            return self.sll_max.get_front()


# BASIC TESTING
if __name__ == "__main__":
    pass

    print('\n# push example 1')
    s = MaxStack()
    print(s)
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    print(s)
    #
    #
    print('\n# pop example 1')
    s = MaxStack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))


    print('\n# top example 1')
    s = MaxStack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)

    print('\n# get_max example 1')
    s = MaxStack()
    for value in [1, -20, 15, 21, 21, 40, 50]:
        print(s, ' ', end='')
        try:
            print(s.get_max())
        except Exception as e:
            print(type(e))
        s.push(value)
    while not s.is_empty():
        print(s.size(), end='')
        print(' Pop value:', s.pop(), ' get_max after: ', end='')
        try:
            print(s.get_max())
        except Exception as e:
            print(type(e))

    print('\n# get_max example 2')
    s = MaxStack()
    for value in [12301, -54781, -63722]:
        s.push(value)
    print(s)
    print(s.get_max())

