# Course: CS261 - Data Structures
# Student Name: Joseph Minefee
# Assignment: Assignment 3 - Circular Doubly Linked List
# Description:


class CDLLException(Exception):
    """
    Custom exception class to be used by Circular Doubly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DLNode:
    """
    Doubly Linked List Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        self.next = None
        self.prev = None
        self.value = value


class CircularList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with sentinel
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.sentinel = DLNode(None)
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel

        # populate CDLL with initial values (if provided)
        # before using this feature, implement add_back() method
        if start_list is not None:
            for value in start_list:
                self.add_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'CDLL ['
        if self.sentinel.next != self.sentinel:
            cur = self.sentinel.next.next
            out = out + str(self.sentinel.next.value)
            while cur != self.sentinel:
                out = out + ' <-> ' + str(cur.value)
                cur = cur.next
        out = out + ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list

        This can also be used as troubleshooting method. This method works
        by independently measuring length during forward and backward
        traverse of the list and return the length if results agree or error
        code of -1 or -2 if thr measurements are different.

        Return values:
        >= 0 - length of the list
        -1 - list likely has an infinite loop (forward or backward)
        -2 - list has some other kind of problem

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """

        # length of the list measured traversing forward
        count_forward = 0
        cur = self.sentinel.next
        while cur != self.sentinel and count_forward < 101_000:
            count_forward += 1
            cur = cur.next

        # length of the list measured traversing backwards
        count_backward = 0
        cur = self.sentinel.prev
        while cur != self.sentinel and count_backward < 101_000:
            count_backward += 1
            cur = cur.prev

        # if any of the result is > 100,000 -> list has a loop
        if count_forward > 100_000 or count_backward > 100_000:
            return -1

        # if counters have different values -> there is some other problem
        return count_forward if count_forward == count_backward else -2

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.sentinel.next == self.sentinel

    # ------------------------------------------------------------------ #

    def __iter__(self):
        return LinkedListIterator(self.sentinel.next)

    def add_front(self, value: object) -> None:
        """
        Adds a new node at the beginning of the list (right after the front sentinel).
        """
        # Sets current to the sentinel, creates a new link, points new_link's next to current's next node, and inserts
        # the new link.
        cur = self.sentinel
        new_link = DLNode(value)
        new_link.next = cur.next
        new_link.prev = cur
        cur.next.prev = new_link
        cur.next = new_link

    def add_back(self, value: object) -> None:
        """
        Adds a new node at the end of the list (right before the back sentinel).
        """
        new_link = DLNode(value)
        cur = self.sentinel
        # Checks if the list is empty and, if so, appends the new value between the sentinel.
        if self.is_empty() is True:
            cur = self.sentinel
            new_link = DLNode(value)
            new_link.next = cur.next
            new_link.prev = cur
            cur.next.prev = new_link
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
        # Base case is if the sentinel is the next node in the linked list. If so, it inserts the new value before the
        # sentinel.
        if cur.next == self.sentinel:
            new_link.next = cur.next
            new_link.prev = cur
            cur.next.prev = new_link
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
        new_link = DLNode(value)
        cur = self.sentinel
        count = 0
        # Checks if the index is greater than length or negative and raises an exception if so.
        if ind > length or ind < 0:
            raise CDLLException
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
            new_link.prev = cur
            cur.next.prev = new_link
            cur.next = new_link
            # Else, the count in incremented and the function calls itself.
        else:
            count += 1
            self.insert_at_index_rec(ind, count, cur.next, new_link)

    def remove_front(self) -> None:
        """
        Removes the first node from the list. If the list is empty, an exception is raised.
        """
        head = self.sentinel
        cur = head.next
        nxt = cur.next
        # Checking for empty list. If list is empty an exception is raised.
        if self.is_empty() is True:
            raise CDLLException
        # Else, removing the node directly after the head.
        else:
            nxt.prev = head
            head.next = cur.next

    def remove_back(self) -> None:
        """
        Removes the last node from the list. If the list is empty, an exception is raised.
        """
        cur = self.sentinel
        # Checks if list is empty and raises an exception if it is.
        if self.is_empty() is True:
            raise CDLLException
        # Else, it calls the recursive helper function.
        else:
            self.remove_back_rec(cur.next)

    def remove_back_rec(self, cur):
        """
        Recursive helper function for the remove_back function.
        """
        # Checks for the last node. If the node is just before the sentinel, it is removed.
        if cur.next == self.sentinel:
            last = cur
            before_last = last.prev
            self.sentinel.prev = before_last
            before_last.next = self.sentinel
        # Else, the function calls itself.
        else:
            self.remove_back_rec(cur.next)

    def remove_at_index(self, index: int) -> None:
        """
        Removes a node from the list given its index. If the index is invalid an exception is raised.
        """
        length = self.length()
        ind = index
        cur = self.sentinel
        count = 0
        # Checking if index is out of range, index is negative, or the list is empty. If so an exception is raised.
        if ind > length - 1 or ind < 0 or length == 0:
            raise CDLLException
        # If the index is zero, then the remove_front method is called.
        elif ind == 0:
            self.remove_front()
        # If the index is the last node, then the remove_back method is called.
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
            nxt = cur.next
            nxt.prev = prev
            prev.next = nxt
        # Else, the function calls itself.
        else:
            count += 1
            self.remove_at_index_rec(ind, count, cur, cur.next)

    def get_front(self) -> object:
        """
        Returns the value from the first node in the list without removing it. If the list is empty an exception is
        raised.
        """
        cur = self.sentinel.next
        # Checking if list is empty. If so, an exception is raised.
        if self.is_empty() is True:
            raise CDLLException
        # Else, the value of the node just after the sentinel is returned.
        else:
            return cur.value

    def get_back(self) -> object:
        """
        Returns the value from the last node in the list without removing it. If the list is empty an exception is
        raised.
        """
        # Checking if list is empty. If so, an exception is raised.
        if self.is_empty() is True:
            raise CDLLException
            # Else, the recursive helper method is returned.
        else:
            return self.get_back_rec(self.sentinel.next)

    def get_back_rec(self, cur):
        """
        Recursive helper method for the get_back function. Returns the value of the last node.
        """
        # Checks for base case which is the node just before the back sentinel and returns that node's value.
        if cur.next == self.sentinel:
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
        cur = self.sentinel
        val = value
        # Checks for an empty list. If so, returns False.
        if self.is_empty() is True:
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
            nxt = cur.next
            nxt.prev = prev
            prev.next = nxt
            return True
        # If the next node is the sentinel, False is returned as the value isn't present in the list.
        elif cur.next == self.sentinel:
            return False
        # Else, the recursive function is returned.
        else:
            return self.remove_rec(cur, cur.next, val)

    def count(self, value: object) -> int:
        """
        Counts the number of elements in the list that match the passed value.
        """
        cur = self.sentinel
        val = value
        count = 0
        # Checks for an empty list. If list is empty the count is returned as 0.
        if self.is_empty() is True:
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
            if cur.next == self.sentinel:
                return count
            # Else, the recursive function is returned.
            else:
                return self.count_rec(count, cur.next, val)
        else:
            # If current is the last node, the count is returned.
            if cur.next == self.sentinel:
                return count
            # Else, the recursive function is returned.
            else:
                return self.count_rec(count, cur.next, val)

    def swap_pairs(self, index1: int, index2: int) -> None:
        """
        Swaps two nodes given their indices.
        """
        length = self.length()
        # Set highest index to high and lowest to low.
        if index1 > index2:
            high = index1
            low = index2
        else:
            high = index2
            low = index1
        # Check for invalid indices.
        if self.is_empty() is True or index1 < 0 or index2 < 0 or index1 > length - 1 or index2 > length - 1:
            raise CDLLException
        # Else, iterate through the indices to find the two indices that were called.
        else:
            # Check to make sure the indices are not equal.
            if index1 != index2:
                # Check to ensure the two indices aren't right next to each other.
                if high != low +1:
                    low_node = None
                    low_prev = None
                    low_next = None
                    high_node = None
                    high_prev = None
                    high_next = None
                    cur = self.sentinel.next
                    # Loop through the list and grab the right values.
                    for i in range(high + 1):
                        if i == low:
                            low_node = cur
                            low_prev = cur.prev
                            low_next = cur.next
                            cur = cur.next
                        elif i == high:
                            high_node = cur
                            high_prev = cur.prev
                            high_next = cur.next
                        else:
                            cur = cur.next
                    # Make the swap.
                    low_prev.next = high_node
                    low_node.next = high_next
                    low_node.prev = high_prev
                    low_next.prev = high_node
                    high_prev.next = low_node
                    high_node.prev = low_prev
                    high_node.next = low_next
                    high_next.prev = low_node
                # Else, if the two values are right next to one another, we have to change the values that we grab.
                else:
                    low_node = None
                    low_prev = None
                    high_node = None
                    high_next = None
                    cur = self.sentinel.next
                    # Loop through the list to grab the values.
                    for i in range(high + 1):
                        if i == low:
                            low_node = cur
                            low_prev = cur.prev
                            cur = cur.next
                        elif i == high:
                            high_node = cur
                            high_next = cur.next
                        else:
                            cur = cur.next
                    # Make the swap.
                    low_prev.next = high_node
                    low_node.next = high_next
                    low_node.prev = high_node
                    high_node.prev = low_prev
                    high_node.next = low_node
                    high_next.prev = low_node
            else:
                pass

    def reverse(self) -> None:
        """
        TODO: Write this implementation
        """
        if self.is_empty() is True:
            pass
        pass


    def sort(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def rotate(self, steps: int) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def remove_duplicates(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def odd_even(self) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def add_integer(self, num: int) -> None:
        """
        TODO: Write this implementation
        """
        pass



if __name__ == '__main__':
    pass

    # print('\n# add_front example 1')
    # lst = CircularList()
    # print(lst)
    # lst.add_front('A')
    # lst.add_front('B')
    # lst.add_front('C')
    # print(lst)
    #
    # print('\n# add_back example 1')
    # lst = CircularList()
    # print(lst)
    # lst.add_back('C')
    # lst.add_back('B')
    # lst.add_back('A')
    # print(lst)
    #
    # print('\n# insert_at_index example 1')
    # lst = CircularList()
    # test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (3, 'D'), (-1, 'E'), (5, 'F')]
    # for index, value in test_cases:
    #     print('Insert of', value, 'at', index, ': ', end='')
    #     try:
    #         lst.insert_at_index(index, value)
    #         print(lst)
    #     except Exception as e:
    #         print(type(e))
    #
    # print('\n# remove_front example 1')
    # lst = CircularList([1, 2])
    # print(lst)
    # for i in range(3):
    #     try:
    #         lst.remove_front()
    #         print('Successful removal', lst)
    #     except Exception as e:
    #         print(type(e))
    #
    # print('\n# remove_back example 1')
    # lst = CircularList()
    # try:
    #     lst.remove_back()
    # except Exception as e:
    #     print(type(e))
    # lst.add_front('Z')
    # lst.remove_back()
    # print(lst)
    # lst.add_front('Y')
    # lst.add_back('Z')
    # lst.add_front('X')
    # print(lst)
    # lst.remove_back()
    # print(lst)
    #
    # print('\n# remove_at_index example 1')
    # lst = CircularList([1, 2, 3, 4, 5, 6])
    # print(lst)
    # for index in [0, 0, 0, 2, 2, -2]:
    #     print('Removed at index:', index, ': ', end='')
    #     try:
    #         lst.remove_at_index(index)
    #         print(lst)
    #     except Exception as e:
    #         print(type(e))
    # print(lst)
    #
    # print('\n# get_front example 1')
    # lst = CircularList(['A', 'B'])
    # print(lst.get_front())
    # print(lst.get_front())
    # lst.remove_front()
    # print(lst.get_front())
    # lst.remove_back()
    # try:
    #     print(lst.get_front())
    # except Exception as e:
    #     print(type(e))
    #
    # print('\n# get_back example 1')
    # lst = CircularList([1, 2, 3])
    # lst.add_back(4)
    # print(lst.get_back())
    # lst.remove_back()
    # print(lst)
    # print(lst.get_back())
    #
    # print('\n# remove example 1')
    # lst = CircularList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    # print(lst)
    # for value in [7, 3, 3, 3, 3]:
    #     print(lst.remove(value), lst.length(), lst)
    #
    # print('\n# count example 1')
    # lst = CircularList([1, 2, 3, 1, 2, 2])
    # print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))
    #
    print('\n# swap_pairs example 1')
    lst = CircularList([0, 1, 2, 3, 4, 5, 6])
    test_cases = ((0, 6), (0, 7), (-1, 6), (1, 5),
                  (4, 2), (3, 3), (1, 2), (2, 1))

    for i, j in test_cases:
        print('Swap nodes ', i, j, ' ', end='')
        try:
            lst.swap_pairs(i, j)
            print(lst)
        except Exception as e:
            print(type(e))
    #
    # print('\n# swap_pairs example 1')
    # lst = CircularList([0, 1, 2, 3, 4, 5, 6])
    #
    # print('Swap nodes ', 0, 6, ' ', end='')
    # try:
    #     lst.swap_pairs(0, 6)
    #     print(lst)
    # except Exception as e:
    #     print(type(e))
    #
    # print('\n# reverse example 1')
    # test_cases = (
    #     [1, 2, 3, 3, 4, 5],
    #     [1, 2, 3, 4, 5],
    #     ['A', 'B', 'C', 'D']
    # )
    # for case in test_cases:
    #     lst = CircularList(case)
    #     lst.reverse()
    #     print(lst)
    #
    # print('\n# reverse example 2')
    # lst = CircularList()
    # print(lst)
    # lst.reverse()
    # print(lst)
    # lst.add_back(2)
    # lst.add_back(3)
    # lst.add_front(1)
    # lst.reverse()
    # print(lst)
    #
    # print('\n# reverse example 3')
    #
    #
    # class Student:
    #     def __init__(self, name, age):
    #         self.name, self.age = name, age
    #
    #     def __eq__(self, other):
    #         return self.age == other.age
    #
    #     def __str__(self):
    #         return str(self.name) + ' ' + str(self.age)
    #
    #
    # s1, s2 = Student('John', 20), Student('Andy', 20)
    # lst = CircularList([s1, s2])
    # print(lst)
    # lst.reverse()
    # print(lst)
    # print(s1 == s2)
    #
    # print('\n# reverse example 4')
    # lst = CircularList([1, 'A'])
    # lst.reverse()
    # print(lst)
    #
    # print('\n# sort example 1')
    # test_cases = (
    #     [1, 10, 2, 20, 3, 30, 4, 40, 5],
    #     ['zebra2', 'apple', 'tomato', 'apple', 'zebra1'],
    #     [(1, 1), (20, 1), (1, 20), (2, 20)]
    # )
    # for case in test_cases:
    #     lst = CircularList(case)
    #     print(lst)
    #     lst.sort()
    #     print(lst)
    #
    # print('\n# rotate example 1')
    # source = [_ for _ in range(-20, 20, 7)]
    # for steps in [1, 2, 0, -1, -2, 28, -100]:
    #     lst = CircularList(source)
    #     lst.rotate(steps)
    #     print(lst, steps)
    #
    # print('\n# rotate example 2')
    # lst = CircularList([10, 20, 30, 40])
    # for j in range(-1, 2, 2):
    #     for _ in range(3):
    #         lst.rotate(j)
    #         print(lst)
    #
    # print('\n# rotate example 3')
    # lst = CircularList()
    # lst.rotate(10)
    # print(lst)
    #
    # print('\n# remove_duplicates example 1')
    # test_cases = (
    #     [1, 2, 3, 4, 5], [1, 1, 1, 1, 1],
    #     [], [1], [1, 1], [1, 1, 1, 2, 2, 2],
    #     [0, 1, 1, 2, 3, 3, 4, 5, 5, 6],
    #     list("abccd"),
    #     list("005BCDDEEFI")
    # )
    #
    # for case in test_cases:
    #     lst = CircularList(case)
    #     print('INPUT :', lst)
    #     lst.remove_duplicates()
    #     print('OUTPUT:', lst)
    #
    # print('\n# odd_even example 1')
    # test_cases = (
    #     [1, 2, 3, 4, 5], list('ABCDE'),
    #     [], [100], [100, 200], [100, 200, 300],
    #     [100, 200, 300, 400],
    #     [10, 'A', 20, 'B', 30, 'C', 40, 'D', 50, 'E']
    # )
    #
    # for case in test_cases:
    #     lst = CircularList(case)
    #     print('INPUT :', lst)
    #     lst.odd_even()
    #     print('OUTPUT:', lst)
    #
    # print('\n# add_integer example 1')
    # test_cases = (
    #   ([1, 2, 3], 10456),
    #   ([], 25),
    #   ([2, 0, 9, 0, 7], 108),
    #    ([9, 9, 9], 9_999_999),
    # )
    # for list_content, integer in test_cases:
    #    lst = CircularList(list_content)
    # print('INPUT :', lst, 'INTEGER', integer)
    # lst.add_integer(integer)
    # print('OUTPUT:', lst)
