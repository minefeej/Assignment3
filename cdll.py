# Course: CS261 - Data Structures
# Student Name: Joseph Minefee
# Assignment: Assignment 3 - Circular Doubly Linked List
# Description: Implement a Circular Linked List


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
        #length = self.length()
        # length = self.get_length()
        # Set highest index to high and lowest to low.
        if index1 > index2:
            high = index1
            low = index2
        else:
            high = index2
            low = index1
        # Check for invalid indices.
        if self.is_empty() or index1 < 0 or index2 < 0:
            raise CDLLException
        # Else, iterate through the indices to find the two indices that were called.
            # Check to make sure the indices are not equal.
        if index1 != index2:
            # Check to ensure the two indices aren't right next to each other.
            if high != low + 1:
                low_node = None
                low_prev = None
                low_next = None
                high_node = None
                high_prev = None
                high_next = None
                cur = self.sentinel.next
                count = 0
                # Loop through the list and grab the right values.
                while cur != self.sentinel:
                    if count == low:
                        low_node = cur
                        low_prev = cur.prev
                        low_next = cur.next
                        cur = cur.next
                        count += 1
                    elif count == high:
                        high_node = cur
                        high_prev = cur.prev
                        high_next = high_node.next
                        cur = cur.next
                        count += 1
                    else:
                        cur = cur.next
                        count += 1
                # Exception is raised if the loops has made it through all values without assigning high_node.
                if high_node is None or high_node == self.sentinel:
                    raise CDLLException
                else:
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
                count = 0
                # Loop through the list to grab the values.
                while cur != self.sentinel:
                    if count == low:
                        low_node = cur
                        low_prev = cur.prev
                        high_node = cur.next
                        high_next = high_node.next
                        count += 1
                    else:
                        cur = cur.next
                        count += 1
                if high_node is None or high_node == self.sentinel:
                    raise CDLLException
                else:
                    # Make the swap.
                    low_prev.next = high_node
                    low_node.next = high_next
                    low_node.prev = high_node
                    high_node.prev = low_prev
                    high_node.next = low_node
                    high_next.prev = low_node
        else:
            cur = self.sentinel.next
            count = 0
            while cur != self.sentinel:
                cur = cur.next
                count += 1
            if count <= high:
                raise CDLLException
            else:
                return
        # length = self.length()
        # if index1 == index2:
        #     pass
        # elif self.is_empty() is True or index1 < 0 or index2 < 0 or index1 > length - 1 or index2 > length - 1:
        #     raise CDLLException
        # else:
        #     if index1 + 1 == index2 or index1 - 1 == index2:
        #         one_node = None
        #         one_prev = None
        #         two_node = None
        #         two_next = None
        #         cur = self.sentinel.next
        #         # Loop through the list to grab the values.
        #         for i in range(length):
        #             if i == index1:
        #                 one_node = cur
        #                 one_prev = cur.prev
        #                 cur = cur.next
        #             elif i == index2:
        #                 two_node = cur
        #                 two_next = cur.next
        #             else:
        #                 cur = cur.next
        #         # Make the swap.
        #         one_prev.next = two_node
        #         one_node.next = two_next
        #         one_node.prev = two_node
        #         two_node.prev = one_prev
        #         two_node.next = one_node
        #         two_next.prev = one_node
        #
        #     else:
        #         one_node = None
        #         one_prev = None
        #         one_next = None
        #         two_node = None
        #         two_prev = None
        #         two_next = None
        #         cur = self.sentinel.next
        #         # Loop through the list and grab the right values.
        #         for i in range(length):
        #             if i == index1:
        #                 one_node = cur
        #                 one_prev = cur.prev
        #                 one_next = cur.next
        #                 cur = cur.next
        #             elif i == index2:
        #                 two_node = cur
        #                 two_prev = cur.prev
        #                 two_next = cur.next
        #             else:
        #                 cur = cur.next
        #         # Make the swap.
        #         one_prev.next = two_node
        #         one_node.next = two_next
        #         one_node.prev = two_prev
        #         one_next.prev = two_node
        #         two_prev.next = one_node
        #         two_node.prev = one_prev
        #         two_node.next = one_next
        #         two_next.prev = one_node

    def reverse(self) -> None:
        """
        Reverses the order of the nodes in the list.
        """
        # Checking for an empty list. If so, it passes out of the function.
        if self.is_empty() is True:
            pass
        # Else, we swap the pointers for each node starting with the sentinel and iterating through the list.
        hold = self.sentinel.next
        cur = self.sentinel
        nxt = cur.next
        cur.next = None
        cur.prev = nxt
        # Looping until we reach the sentinel again.
        while nxt is not None:
            nxt.prev = nxt.next
            nxt.next = cur
            cur = nxt
            nxt = nxt.prev
        self.sentinel.prev = hold

    def sort(self) -> None:
        """
        Sorts the content of a doubly linked list in non-descending order using a bubble sort.
        """
        # Checking for an empty list. If so, it passes out of the function.
        if self.is_empty() is True:
            pass
        # Uses the length of the list to initialize two loops. The first passes through each element while for each pass
        # the second loop loops through the adjacent elements and makes swaps.
        else:
            length = self.length()
            cur = self.sentinel
            for pass_num in range(length):
                for ind in range(length):
                    if cur.next.value is not None and cur.value is not None:
                        if cur.value > cur.next.value:
                            # temp = cur.prev
                            cur = cur
                            nxt = cur.next
                            cur.next = nxt.next
                            nxt.next = cur
                            cur.prev.next = nxt
                            nxt.prev = cur.prev
                            cur.prev = nxt
                            cur.next.prev = cur
                    cur = cur.next

    def rotate(self, steps: int) -> None:
        """
        Rotates the linked list by shifting positions of its elements right or left steps number of times. If steps
        is positive, elements are rotated right. If steps are negative, elements are rotated left.
        """
        length = self.length()
        dist = None
        # Check for empty list.
        if self.is_empty():
            pass
        # Check if steps are negative and calculate the proper index to move.
        else:
            if steps < 0 and -steps < length:
                dist = length + steps
            elif steps < 0 and -steps > length:
                if -(steps) % length == 0:
                    dist = 0
                else:
                    dist = length - (-steps % length)
            else:
                dist = steps % length
            # If distance greater than and not equal to zero, the elements will be rotated.
            if dist > 0 and dist != 0:
                cur = self.sentinel.prev
                # Loops through the elements of the list to find the right index to insert the sentinel.
                for el in range(dist):
                    cur = cur.prev
                sent = self.sentinel
                nxt = cur.next
                cur.next = sent
                sent.next.prev = sent.prev
                sent.prev.next = sent.next
                sent.next = nxt
                nxt.prev = sent
                sent.prev = cur
            # If distance is zero, the list is left unchanged.
            else:
                pass

    def remove_duplicates(self) -> None:
        """
        Deletes all nodes that have duplicate values from a sorted linked list, leaving only nodes with distinct values.
        """
        # If the list is empty, it does nothing.
        if self.is_empty():
            pass
        # Else, cur is set to the first node of the list with a value. The while loop loops through the list removing
        # duplicate values.
        cur = self.sentinel.next
        while cur.next.value is not None:
            if cur.value == cur.next.value:
                self.remove(cur.value)
                self.remove(cur.next.value)
                cur = cur.next
            else:
                cur = cur.next

    def odd_even(self) -> None:
        """
        Regroups a list of nodes by first regrouping all of the odd nodes in the front and the even nodes in the back.
        """
        # If the list is empty, it does nothing.
        if self.is_empty():
            pass
        # Initialize cur as the first node with value, count as two, and index as zero.
        cur = self.sentinel.next
        new_cur = None
        length = self.length()
        count = 2
        ind = 0
        # The while counter loops until the count exceed the length of the linked list.
        while count < length:
            # This for loop grabs the index where we want to insert the node and the index where the node is currently.
            for i in range(count):
                if i == ind:
                    new_cur = cur
                    cur = cur.next
                else:
                    cur = cur.next
            # Then the node is swapped to its new location and the gaps are filled in.
            cur.prev.next = cur.next
            cur.next.prev = cur.prev
            cur.next = new_cur.next
            new_cur.next = cur
            cur.next.prev = cur
            cur.prev = new_cur
            ind += 1
            count += 2
            cur = self.sentinel.next

    def add_integer(self, num: int) -> None:
        """
        Receives an integer and adds it to the number already stored in the linked list.
        """
        # Initializes the num to a new variable as a string so that it can be indexed into. Then the length of the
        # num string and the linked list are assigned.
        new_num = str(num)
        num_len = len(new_num)
        length = self.length()
        # If the list is empty, the values are simply added to the end of the empty list.
        if self.is_empty():
            num_i = -1
            for i in range(num_len):
                self.add_front(int(new_num[num_i]))
                num_i -= 1
        # If the length of the num is less than or equal to the length of the linked list then we don't have to add any
        # new nodes to the list unless the first node needs to carry over which is done in the while loop.
        elif num_len <= length:
            cur = self.sentinel.prev
            # We index into the new_num from the back.
            num_i = -1
            # Zeros are added to new_num so that it is the same length as the linked list.
            new_num = "0" * (length - num_len + 1) + new_num
            # While current isn't the sentinel, we iterate through the list to add the values from the back to the
            # front. If the last (or first node) needs to carryover a one, it is added to the front.
            while cur.value is not None:
                cur.value = cur.value + int(new_num[num_i])
                if cur.value >= 10:
                    if cur.prev.value is not None:
                        cur.prev.value = cur.prev.value + 1
                        cur.value = cur.value - 10
                    else:
                        self.add_front(1)
                        cur.value = cur.value - 10
                # num_i and cur are incremented to the next values.
                num_i -= 1
                cur = cur.prev
        # If the length of the number is greater than the linked list, we have to add nodes to the front of the linked
        # list.
        else:
            cur = self.sentinel.prev
            num_i = -1
            diff = num_len - length
            new_num = "0" + new_num
            # We use the difference between the two values to add nodes to the front of the linked list.
            for i in range(diff):
                self.add_front(0)
            # While the node isn't the sentinel, values are added the same as above.
            while cur.value is not None:
                cur.value = cur.value + int(new_num[num_i])
                if cur.value >= 10:
                    if cur.prev.value is not None:
                        cur.prev.value = cur.prev.value + 1
                        cur.value = cur.value - 10
                    else:
                        self.add_front(1)
                        cur.value = cur.value - 10
                num_i -= 1
                cur = cur.prev


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
    # # print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))
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
            print(lst.length())
        except Exception as e:
            print(type(e))

    # print('\n# swap_pairs example 1')
    # lst = CircularList([6196, 27474, 89329, -53623, 98065, -13683])
    #
    # print('Swap nodes ', 6, 5, ' ', end='')
    # try:
    #     lst.swap_pairs(6, 5)
    #     print(lst)
    # except Exception as e:
    #     print(type(e))

    # print('\n# reverse example 1')
    # test_cases = (
    #     [1, 2, 3, 3, 4, 5],
    #     [1, 2, 3, 4, 5],
    #     ['A', 'B', 'C', 'D']
    # )
    # for case in test_cases:
    #     lst = CircularList(case)
    #     lst.reverse()
    #     cur = lst.sentinel
    #     for i in range(lst.length()):
    #         print(cur)
    #         cur = cur.next
    #     print(lst)

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
    # print('\n# sort example 2')
    # test_case = [99340, 11544,  -77793, -47108]
    # lst = CircularList(test_case)
    # print(lst)
    # lst.sort()
    # print(lst)
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
    # print('\n# rotate example 4')
    # source = [1, 2, 3, 4, 5]
    # steps = -4444
    # lst = CircularList(source)
    # lst.rotate(steps)
    # print(lst, steps)
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
    # #
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
    #     # cur = lst.sentinel
    #     # for i in range(6):
    #     #     print(cur)
    #     #     cur = cur.next
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
    #     lst = CircularList(list_content)
    #     print('INPUT :', lst, 'INTEGER', integer)
    #     lst.add_integer(integer)
    #     print('OUTPUT:', lst, lst.length())
    #
    # print('\n# add_integer example 2')
    # test_cases = (
    #   ([], 10456),
    #   ([], 25),
    #   ([2, 0, 9, 0, 7], 108),
    #    ([9, 9, 9], 111),
    # )
    # for list_content, integer in test_cases:
    #     lst = CircularList(list_content)
    #     print('INPUT :', lst, 'INTEGER', integer)
    #     lst.add_integer(integer)
    #     print('OUTPUT:', lst)
