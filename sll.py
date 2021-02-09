# Course: CS261 - Data Structures
# Student Name: Joseph Minefee
# Assignment:   Assignment 2: Singly Linked List
# Description:  Implement deque and bag ADT interfaces with a singly linked list data structure.


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class SLNode:
    """
    Singly Linked List Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        self.next = None
        self.value = value


class LinkedList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with front and back sentinels
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.head = SLNode(None)
        self.tail = SLNode(None)
        self.head.next = self.tail

        # populate SLL with initial values (if provided)
        # before using this feature, implement add_back() method
        if start_list is not None:
            for value in start_list:
                self.add_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        if self.head.next != self.tail:
            cur = self.head.next.next
            out = out + str(self.head.next.value)
            while cur != self.tail:
                out = out + ' -> ' + str(cur.value)
                cur = cur.next
        out = out + ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
            length += 1
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.head.next == self.tail

    # ------------------------------------------------------------------ #

    def add_front(self, value: object) -> None:
        """
        Adds a new node at the beginning of the list (right after the front sentinel).
        """
        # Sets current to the head, creates a new link, points new_link's next to current's next node, and inserts
        # the new link.
        cur = self.head
        new_link = SLNode(value)
        new_link.next = cur.next
        cur.next = new_link

    def add_back(self, value: object) -> None:
        """
        Adds a new node at the end of the list (right before the back sentinel).
        """
        # traverse the list to find last node
        new_link = SLNode(value)
        cur = self.head
        # Checks if the list is empty and, if so, appends the new value between the sentinels.
        if cur.next == self.tail:
            cur = self.head
            new_link = SLNode(value)
            new_link.next = cur.next
            cur.next = new_link
        # Else, it calls the recursive helper function.
        else:
            self.add_back_rec(cur.next, new_link)

    def add_back_rec(self, cur, new_link):
        """
        Recursive helper function for the add_back function.
        """
        cur = cur
        new_link = new_link
        # Base case is if the tail is the next node in the linked list. If so, it inserts the new value before the
        # back sentinel.
        if cur.next == self.tail:
            new_link.next = cur.next
            cur.next = new_link
        # Else, the function calls itself.
        else:
            self.add_back_rec(cur.next, new_link)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Adds a new value at the specified index position in the linked list.
        """
        length = self.length()
        ind = index
        new_link = SLNode(value)
        cur = self.head
        count = 0
        # Checks if the index is greater than length or negative and raises an exception if so.
        if ind > length or ind < 0:
            raise SLLException
        # Else if the index is zero, the add_front function is called.
        else:
            if ind == 0:
                self.add_front(value)
            # Else, it calls the recursive helper function.
            else:
                count += 1
                self.insert_at_index_rec(ind, count, cur.next, new_link)

    def insert_at_index_rec(self, ind, count, cur, new_node):
        """
        Recursive helper function for insert_at_index with a base case that index is equal to count.
        """
        cur = cur
        new_link = new_node
        ind = ind
        count = count
        # Checks if the count and index is equal. If so, it inserts the new node.
        if ind == count:
            new_link.next = cur.next
            cur.next = new_link
            # Else, the count in incremented and the function calls itself.
        else:
            count += 1
            self.insert_at_index_rec(ind, count, cur.next, new_link)

    def remove_front(self) -> None:
        """
        Removes the first node from the list. If the list is empty, an exception is raised.
        """
        length = self.length()
        head = self.head
        cur = self.head.next
        # Checking for empty list. If list is empty an exception is raised.
        if length < 1:
            raise SLLException
        # Else, removing the node directly after the head.
        else:
            head.next = cur.next

    def remove_back(self) -> None:
        """
        Removes the last node from the list. If the list is empty, an exception is raised.
        """
        length = self.length()
        cur = self.head
        # Checks if list is empty and raises an exception if it is.
        if length < 1:
            raise SLLException
        # Else, it calls the recursive helper function.
        else:
            self.remove_back_rec(cur, cur.next)

    def remove_back_rec(self, prev, cur):
        """
        Recursive helper function for the remove_back function.
        """
        # Checks for the last node. If the node is just before the tail, it is removed.
        if cur.next == self.tail:
            prev.next = cur.next
        # Else, the function calls itself.
        else:
            self.remove_back_rec(cur, cur.next)

    def remove_at_index(self, index: int) -> None:
        """
        Removes a node from the list given its index. If the index is invalid an exception is raised.
        """
        length = self.length()
        ind = index
        cur = self.head
        count = 0
        # Checking if index is out of range, index is negative, or the list is empty. If so an exception is raised.
        if ind > length - 1 or ind < 0 or length == 0:
            raise SLLException
        # If the index is zero, then the remove_front method is called.
        elif ind == 0:
            self.remove_front()
        # If the index is before the back sentinel, the the remove_back method is called.
        elif ind == length - 1:
            self.remove_back()
        # Else, the recursive helper function is called.
        else:
            self.remove_at_index_rec(ind, count, cur, cur.next)

    def remove_at_index_rec(self, ind, count, prev, cur):
        """
        Recursive helper method for the remove at index function.
        """
        # If the index is equal to the count, then the current node is removed.
        if ind == count:
            prev.next = cur.next
        # Else, the function calls itself.
        else:
            count += 1
            self.remove_at_index_rec(ind, count, cur, cur.next)

    def get_front(self) -> object:
        """
        Returns the value from the first node in the list without removing it. If the list is empty an exception is
        raised.
        """
        length = self.length()
        cur = self.head.next
        # Checking if list is empty. If so, an exception is raised.
        if length == 0:
            raise SLLException
        # Else, the value of the node just after the front sentinel is returned.
        else:
            return cur.value

    def get_back(self) -> object:
        """
        Returns the value from the last node in the list without removing it. If the list is empty, the method raises an
        exception.
        """
        length = self.length()
        # Checks if the list is empty. If so, it raises and exception.
        if length == 0:
            raise SLLException
        # Else, the recursive helper method is returned.
        else:
            return self.get_back_rec(self.head.next)

    def get_back_rec(self, cur):
        """
        Recursive helper method for the get_back function. Returns the value of the last node.
        """
        # Checks for base case which is the node just before the back sentinel and returns that node's value.
        if cur.next == self.tail:
            return cur.value
        # Returns the recursive call.
        else:
            return self.get_back_rec(cur.next)

    def remove(self, value: object) -> bool:
        """
        Traverses the list from the beginning to the end and removes the first node in the list that matches the
        provided value object. It returns True if some node was actually removed from the list. Otherwise, it returns
        False.
        """
        length = self.length()
        cur = self.head
        val = value
        # Checks for an empty list. If so, returns False.
        if length == 0:
            return False
        # Else, returns the recursive helper method.
        else:
            return self.remove_rec(cur, cur.next, val)

    def remove_rec(self, prev, cur, val):
        """
        Recursive helper method for the remove function. Returns true if a node is removed. Else, returns false.
        """
        # Checks for the base case. If the current node's value is equal to the passed value, the node is removed and
        # True is returned.
        if cur.value == val:
            prev.next = cur.next
            return True
        # If the next node is the tail, False is returned as the value isn't present in the list.
        elif cur.next == self.tail:
            return False
        # Else, the recursive function is returned.
        else:
            return self.remove_rec(cur, cur.next, val)

    def count(self, value: object) -> int:
        """
        Counts the number of elements in the list that match the passed value.
        """
        length = self.length()
        cur = self.head
        val = value
        count = 0
        # Checks for an empty list. If list is empty the count is returned as 0.
        if length == 0:
            return count
        # Else, the recursive helper function is returned.
        else:
            return self.count_rec(count, cur.next, val)

    def count_rec(self, count, cur, val):
        """
        Recursive helper method for the count function. Returns the count of elements in the list that match the
        provided value.
        """
        # Checks if the current node value is equal to the passed value. If so, it increments the count.
        if cur.value == val:
            count += 1
            # If current is the last node, the count is returned.
            if cur.next == self.tail:
                return count
            # Else, the recursive function is returned.
            else:
                return self.count_rec(count, cur.next, val)
        else:
            # If current is the last node, the count is returned.
            if cur.next == self.tail:
                return count
            # Else, the recursive function is returned.
            else:
                return self.count_rec(count, cur.next, val)

    def slice(self, start_index: int, size: int) -> object:
        """
        Returns a new LinkedList object that contains the requested number of nodes from the original list starting
        with the node located at the requested start index.
        """
        new_list = LinkedList()
        length = self.length()
        cur = self.head
        count = 0
        # Checks for an index out of range and a size out of range.
        if start_index > length - 1 or start_index < 0 or size < 0 or length - start_index < size:
            raise SLLException
        # Checks if the size is zero and returns an empty linked list object.
        elif size == 0:
            return new_list
        # Else, it returns the recursive helper method.
        else:
            return self.slice_rec(cur.next, count, start_index, size, new_list)

    def slice_rec(self, cur, count, start_index, size, linked_list):
        """
        Recursive helper method for the slice function. Returns a linked list object.
        """
        # Checks if count is greater than or equal to the start index to find the value at the start index.
        if count >= start_index:
            # Checks if count is equal to the start index and add the value of the current node.
            if count == start_index:
                linked_list.add_back(cur.value)
                # If count is larger than or equals the start index, we then check if we are at the final node to add.
                # The node is added to the new linked list and that list is returned.
                if count == start_index + size - 1:
                    return linked_list
                # Else, the count in incremented and the recursive helper is returned again.
                else:
                    count += 1
                    return self.slice_rec(cur.next, count, start_index, size, linked_list)
            # Else, if count was equal to the start index, we check if the start index is also the last node to be added
            # tot the new list. If so, the value is added and the list is returned.
            else:
                if count == start_index + size - 1:
                    linked_list.add_back(cur.value)
                    return linked_list
                # Else, the count is incremented, the value is added, and the recursive helper is returned again.
                else:
                    count += 1
                    linked_list.add_back(cur.value)
                    return self.slice_rec(cur.next, count, start_index, size, linked_list)
        # If we haven't reached the starting index, the count is incremented and the recursive helper is returned.
        else:
            count += 1
            return self.slice_rec(cur.next, count, start_index, size, linked_list)


if __name__ == '__main__':
    pass

    print('\n# add_front example 1')
    list = LinkedList()
    print(list)
    list.add_front('A')
    list.add_front('B')
    list.add_front('C')
    print(list)


    print('\n# add_back example 1')
    list = LinkedList()
    print(list)
    list.add_back('C')
    list.add_back('B')
    list.add_back('A')
    print(list)


    print('\n# insert_at_index example 1')
    list = LinkedList()
    test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (3, 'D'), (-1, 'E'), (5, 'F')]
    for index, value in test_cases:
        print('Insert of', value, 'at', index, ': ', end='')
        try:
            list.insert_at_index(index, value)
            print(list)
        except Exception as e:
            print(type(e))


    print('\n# insert_at_index example 2')
    list = LinkedList()
    test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (2, 'D'), (2, 'E'), (4, 'F')]
    for index, value in test_cases:
        print('Insert of', value, 'at', index, ': ', end='')
        try:
            list.insert_at_index(index, value)
            print(list)
        except Exception as e:
            print(type(e))


    print('\n# remove_front example 1')
    list = LinkedList([1, 2])
    print(list)
    for i in range(3):
        try:
            list.remove_front()
            print('Successful removal', list)
        except Exception as e:
            print(type(e))


    print('\n# remove_back example 1')
    list = LinkedList()
    try:
        list.remove_back()
    except Exception as e:
        print(type(e))
    list.add_front('Z')
    list.remove_back()
    print(list)
    list.add_front('Y')
    list.add_back('Z')
    list.add_front('X')
    print(list)
    list.remove_back()
    print(list)


    print('\n# remove_at_index example 1')
    list = LinkedList([1, 2, 3, 4, 5, 6])
    print(list)
    for index in [0, 0, 0, 2, 2, -2]:
        print('Removed at index:', index, ': ', end='')
        try:
            list.remove_at_index(index)
            print(list)
        except Exception as e:
            print(type(e))
    print(list)


    print('\n# remove_at_index example 2')
    list = LinkedList([1, 2, 3, 4, 5, 6])
    print(list)
    for index in [2, 3, 1, 0, 1, -2]:
        print('Removed at index:', index, ': ', end='')
        try:
            list.remove_at_index(index)
            print(list)
        except Exception as e:
            print(type(e))
    print(list)


    print('\n# get_front example 1')
    list = LinkedList(['A', 'B'])
    print(list.get_front())
    print(list.get_front())
    list.remove_front()
    print(list.get_front())
    list.remove_back()
    try:
        print(list.get_front())
    except Exception as e:
        print(type(e))


    print('\n# get_back example 1')
    list = LinkedList([1, 2, 3])
    list.add_back(4)
    print(list.get_back())
    list.remove_back()
    print(list)
    print(list.get_back())


    print('\n# remove example 1')
    list = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(list)
    for value in [7, 3, 3, 3, 3]:
        print(list.remove(value), list.length(), list)


    print('\n# count example 1')
    list = LinkedList([1, 2, 3, 1, 2, 2])
    print(list, list.count(1), list.count(2), list.count(3), list.count(4))


    print('\n# slice example 1')
    list = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = list.slice(1, 3)
    print(list, ll_slice, sep="\n")
    ll_slice.remove_at_index(0)
    print(list, ll_slice, sep="\n")
    #
    #
    print('\n# slice example 2')
    list = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", list)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Slice", index, "/", size, end="")
        try:
            print(" --- OK: ", list.slice(index, size))
        except:
            print(" --- exception occurred.")
