"""
# Node Class Documentation

## Overview

The `Node` class represents a node in a tree-like data structure. It allows for the hierarchical organization of objects and offers methods to navigate the tree, add subnodes, and perform other tree-based operations.

---

## Class Attributes

- `counter (int)`: Keeps track of the number of Node instances created.

---

## Instance Attributes

- `_title (str, optional)`: The title of the node. Default is None.
- `_id (int)`: A unique identifier for the node.
- `_parent (Node or None)`: The parent node of the current node. Default is None.
- `_current_node (Node or None)`: The node currently pointed to. Default is None.
- `subnodes (list)`: List of child nodes.

---

## Usage Examples

### Initialize root and child nodes

```python
root = Node("Root")
child1 = Node("Child1")
grandchild1 = Node("Grandchild1")
grandchild2 = Node("Grandchild2")
```

### Add child and grandchild nodes

```python
child1.add_subnode(grandchild1)
child1.add_subnode(grandchild2)
root.add_subnode(child1)
```

### Initialize another child node

```python
child2 = Node("Child2")
root.add_subnode(child2)
```

### Tree navigation

```python
next_node = root.next()
prev_node = root.prev()
```

### Check tree boundaries

```python
if root.is_at_tree_boundary():
    print("Reached the boundary.")
```

### Iterating through the tree

```python
for node in root:
    print(node.title)
```

---

## Advanced Usage and Behavior of the Node Class

### Counter
- The class attribute `Node.counter` keeps track of the number of `Node` instances. Useful for debugging and analysis.

### Tree Traversal: `next()` and `prev()`
- Calling `next()` on a root node initially returns the root node itself.
- Subsequent calls traverse the tree depth-first, moving from parent to first child, then to the next sibling, and so on.
- The `prev()` method traverses the tree in the reverse order but does not ascend above the node it was initially called on.
- `next()` and `prev()` methods update the flags `reached_tree_start` and `reached_tree_end` to indicate if the traversal has reached the tree boundaries.

### Boundary Check: `is_at_tree_boundary()`
- Returns `True` when the current node is at the start or the end of the tree/subtree.

### Node Indexing
- Nodes can be accessed using a list of indices through methods like `get_node_by_index()` and `set_current_node_by_index()`.
- Index lists are relative to the node on which the method is called.

### Removing Nodes: `remove()`
- The `remove()` method can take in a list of indices to remove a specific node or set of nodes.
- Providing an empty list or calling `remove()` without arguments removes all subnodes.

### Iteration
- The class supports Python's iterator protocol, allowing traversal using a `for` loop.

### Method Independence
- `next()` and `prev()` methods on different nodes within the same tree operate independently.

### Method Limitations
- `prev()` does not traverse up to the root when called from a child node.
- `next()` does not traverse to siblings when called from a child node.

### Node Relationships: `get_root_and_target()`
- Returns the root and target nodes based on current traversal, with options to consider the node either as a root or as a part of a larger tree.

### Utility Methods
- `get_root_node()` returns the ultimate root node of any given node.
- `get_end_node()` returns the deepest last node in the tree or subtree.
- `get_last_node()` returns the last subnode of a node, if any.
- `pretty_print()` outputs the structure of the tree/subtree rooted at the node.

### Unit Testing
- Extensive unit tests cover all these scenarios and edge cases, providing examples of expected behavior.

"""

import re


class Node:
    """
    Represents a node in a tree-like data structure. The Node class allows for
    hierarchical organization of objects, complete with methods to navigate the tree,
    add subnodes, and perform other tree-based operations.

    Class Attributes:
        counter (int): Class-level variable that keeps track of the number of Node instances created.

    Instance Attributes:
        _title (str, optional): The title of the node. Default is None.
        _id (int): A unique identifier for the node.
        _parent (Node or None): The parent node of the current node. Default is None.
        _current_node (Node or None): The node currently pointed to. Default is None.
        subnodes (list): List of child nodes.

    Usage Examples:

        # Initialize root and child nodes
        root = Node("Root")
        child1 = Node("Child1")
        grandchild1 = Node("Grandchild1")
        grandchild2 = Node("Grandchild2")

        # Add child and grandchild nodes
        child1.add_subnode(grandchild1)
        child1.add_subnode(grandchild2)
        root.add_subnode(child1)

        # Initialize another child node
        child2 = Node("Child2")
        root.add_subnode(child2)

        # Tree navigation
        next_node = root.next()
        prev_node = root.prev()

        # Check tree boundaries
        if root.is_at_tree_boundary():
            print("Reached the boundary.")

        # Iterating through the tree
        for node in root:
            print(node.title)
    """

    counter = 0
    """
    int: Class-level counter that auto-increments to generate a unique ID for each new Node instance.
    """

    fields = {}
    """
    dict: Class-level property for storing additional attributes of a Node instance. Beyond the title, this property allows for the storage of any Node data without pre-defined structure constraints.
    """

    subnodes = []
    """
    list: Class-level property that stores or holds the list of subnodes, each of which must be a Node instance, attached to a Node instance.
    """

    reached_tree_end = False
    """
    bool: Class-level property that indicates whether the end of the tree has been reached during traversal.
    """

    reached_tree_start = True
    """
     bool: Class-level property that indicates whether the start of the tree has been reached during traversal.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a Node instance with attributes and optional subnodes.

        Args:
            *args: Zero or more arguments. The last string argument sets the node's title. 
                Other arguments should be Node instances or dictionaries for subnodes.
            **kwargs: Additional configurations.
                - subnodes (list[Node], optional): Extend existing subnodes.
                - Other keyword arguments populate the 'fields' dictionary.

        Side Effects:
            - Generates a unique ID for the node by incrementing the class-level 'counter'.
            - Initializes '_title', '_id', and '_parent' attributes.
            - Populates 'subnodes' list and sets their parent to this node.
            - Fills 'fields' dictionary with additional keyword arguments, excluding 'title' and 'subnodes'.
            - Calls 'reset' method to initialize state flags.

        Raises:
            - TypeError: If any argument in *args is not a string, Node instance, or dictionary.
        """
        Node.counter += 1
        title = kwargs.get("title", None)
        subnodes = []
        for arg in args:
            # The last string in the arguments will be the one left for the title
            if isinstance(arg, str) or isinstance(arg, int) or isinstance(arg, float):
                title = arg
            elif isinstance(arg, Node) or isinstance(arg, dict):
                subnodes.append(arg)
            else:
                raise TypeError("Node must be either type of Node or dictionary")
        self._title = title
        self._id = Node.counter
        # Parent is by default None
        # It will be replaced if this node is added to the other node by add_subnode
        self._parent = None
        self.subnodes = []
        if subnodes:
            for node in subnodes:
                self.add_subnode(node)
        # Extend subnodes if keyword arguments has subnodes
        if "subnodes" in kwargs:
            self.add_subnodes(*kwargs["subnodes"])
        # Set all other fields to the field storage except subnodes and title
        self.fields = {k: v for k, v in kwargs.items() if k not in ["title", "subnodes"]}
        self.reset()
    
    def reset(self):
        """
        Reset the current node and boundary flags to their initial states relative to the node where the method is called.

        Returns:
            Node: The current node instance relative to which the reset is performed, allowing for method chaining.

        Behavior:
            - Sets the internal '_current_node' attribute to None. Note: 'current_node' is set to None after reset, and only calling 'root.next()' will set 'current_node' to 'root'.
            - Sets the 'reached_tree_end' flag to False.
            - Sets the 'reached_tree_start' flag to True.
            - The reset is local to the node where the method is called and does not propagate to parent or child nodes.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)

            # Traverse the tree starting from root
            root.next()  # Sets 'current_node' to 'root'
            root.next()  # Sets 'current_node' to 'child1'

            # Reset the tree traversal state for 'child1'
            child1.reset()  # Returns 'child1', resets traversal flags and current node locally

            # Demonstrate that the reset on 'child1' did not affect 'root'
            root.next()  # Traverses 'current_node' to 'child2'

            # Demonstrate that the reset on 'child1' is local
            child1.next()  # Traverses 'current_node' to 'child1', the starting node
        """
        self._current_node = None
        self.reached_tree_end = False
        self.reached_tree_start = True
        return self

    def has_subnodes(self):
        """
        Determine if the current node contains any subnodes.

        Returns:
            bool: True if the current node has one or more subnodes; otherwise, False.

        Behavior:
            - Checks the length of the 'subnodes' list attribute of the current node.
            - Returns True if the length is greater than zero, indicating the presence of subnodes.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            root.add_subnodes(child1)
            # Check if root has subnodes
            has_subnodes = root.has_subnodes()  # Returns True
            # Check if child1 has subnodes
            has_subnodes = child1.has_subnodes()  # Returns False
        """
        return len(self.subnodes) > 0

    def get_subnodes(self):
        """
        Retrieve the list of subnodes for the current node.

        Returns:
            list: A list of subnodes belonging to the current node.

        Behavior:
            - Directly returns the 'subnodes' attribute of the current node, which is a list containing all its subnodes.
            - The 'subnodes' attribute can also be accessed directly using 'node.subnodes'.
            - Subnodes can be added or modified using the 'add_subnode(s)', 'insert_subnode(s)', and 'set_subnode' methods.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)
            # Get the list of subnodes
            subnodes_list = root.get_subnodes()  # Returns [child1, child2]
            # Alternatively
            subnodes_list = root.subnodes  # Returns [child1, child2]
        """
        return self.subnodes

    def peek_next(self):
        """
        Peek at the next node in the tree traversal without actually moving to it.

        Returns:
            Node or None: The next node in the depth-first traversal, or None if the end of the tree is reached.

        Behavior:
            - Checks the 'reached_tree_end' flag. If True, returns None.
            - Calls the 'next' method to get the next node.
            - Immediately calls the 'prev' method to revert the traversal, ensuring the current node remains unchanged.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)
            # Peek at the next node without moving
            next_node_peek = root.peek_next()  # Returns the root node on the first call if 'current_node' is None
        """
        if self.reached_tree_end:
            return None
        node = self.next()
        if node:
            self.prev()
        return node

    def peek_prev(self):
        """
        Peek at the previous node in the tree traversal without actually moving to it.

        Returns:
            Node or None: The previous node in the depth-first traversal, or None if the start of the tree is reached.

        Behavior:
            - Checks the 'reached_tree_start' flag. If True, returns None.
            - Calls the 'prev' method to get the previous node.
            - Immediately calls the 'next' method to revert the traversal, ensuring the current node remains unchanged.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)
            # Traverse to the end of the tree
            while root.next():
                pass
            # Peek at the previous node without moving
            prev_node_peek = root.peek_prev()  # Returns the last node in the tree on the first call
        """
        if self.reached_tree_start:
            return None
        node = self.prev()
        if node:
            self.next()
        return node

    def is_at_tree_boundary(self):
        """
        Checks whether the current node is at either boundary of the tree.

        Returns:
            bool: True if at either boundary (start or end), otherwise False.

        Logic Explained:
            - Returns True if either 'reached_tree_end' or 'reached_tree_start' is True.
        """
        return self.reached_tree_end or self.reached_tree_start

    @property
    def title(self):
        """
        Retrieve the title of the node.

        Returns:
            str: The title of the node.

        Behavior:
            - Accesses the internal '_title' attribute to return the title.

        Examples:
            # Initialize a node with a title
            node = Node("MyTitle")
            # Retrieve the title
            node_title = node.title  # Returns 'MyTitle'
        """
        return self._title

    @title.setter
    def title(self, title=None):
        """
        Set the title of the node.

        If node title is None, the __str__ representation will use autoincrement id for the part of the label.

        Args:
            title (str, optional): The new title for the node. Defaults to None.
        """
        self._title = title

    def get_title(self):
        return self._title
    
    def get_fields(self):
        return self.fields

    @property
    def parent(self):
        """
        Retrieve the parent node of the current node.

        Returns:
            Node or None: The parent node of the current node, or None if the node is the root.

        Behavior:
            - Returns the value stored in the private attribute '_parent', which is set either during initialization or when added as a subnode to another node.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child = Node("Child")
            root.add_subnodes(child)
            # Retrieve the parent of 'child'
            parent_node = child.parent  # Returns 'root'
        """
        return self._parent

    @property
    def current_node(self):
        """
        Retrieve the current node in the tree traversal.

        Returns:
            Node: The current node.

        Behavior:
            - Retrieves the value from the private attribute '_current_node'.
            - The '_current_node' attribute is set during tree traversal methods like 'next' and 'prev'.
        """
        return self._current_node

    @current_node.setter
    def current_node(self, node):
        """
        Sets the current node.

        Parameters:
            node (Node): The node to set as the current node.
        """
        self._current_node = node
    
    def _modify_subnodes(self, index_list, action, node=None, **kwargs):
        # Validate and create the node
        if not isinstance(node, Node) and not isinstance(node, dict):
            raise TypeError("Node must be of type Node object or dictionary")
        if not node and not kwargs:
            raise ValueError("Either 'node' or 'kwargs' must be provided")
        if isinstance(node, dict) or kwargs:
            # If both are given, node will be used
            node = Node(**(node or kwargs))
        node._parent = self

        # Navigate to the target location
        target = self
        for i in index_list[:-1]:
            target = target.subnodes[i]

        # Perform the action
        if action == 'set':
            target.subnodes[index_list[-1]] = node
        elif action == 'insert':
            target.subnodes.insert(index_list[-1], node)
        elif action == 'add':
            target.subnodes.append(node)
        else:
            raise ValueError("Invalid action")

        return self

    def set_subnode(self, index_list, node=None, **kwargs):
        """
        Replace a subnode at a specified index with a new node and return the modified node.

        Parameters:
            index_list (int or list[int]): The index or list of indices specifying the subnode to replace.
            node (Node, optional): An existing Node instance to set as the new subnode. If None, a new node will be created based on the **kwargs.
            **kwargs: Optional parameters in dictionary format for creating a new node. Can include 'title', 'subnodes', and any extra fields.

        Returns:
            Node: The modified node, allowing for method chaining.

        Behavior:
            - Calls the private '_modify_subnodes' method with the following arguments:
                1. A list containing the index or indices for the subnode to replace.
                2. The operation type ('set' in this case).
                3. The Node instance to set, either provided or created from **kwargs.
            - Replaces the existing subnode at the specified index with the new node.
        """
        return self._modify_subnodes([index_list] if isinstance(index_list, int) else index_list, 'set', node, **kwargs)

    def insert_subnode(self, index_list, node=None, **kwargs):
        """
        Insert a subnode at a specified index, shifting subsequent subnodes, and return the modified node.

        Parameters:
            index_list (int or list[int]): The index or list of indices specifying where to insert the new subnode.
            node (Node, optional): An existing Node instance to insert. If None, a new node will be created based on the **kwargs.
            **kwargs: Optional parameters in dictionary format for creating a new node. Can include 'title', 'subnodes', and any extra fields.

        Returns:
            Node: The modified node, allowing for method chaining.

        Behavior:
            - Calls the private '_modify_subnodes' method with the following arguments:
                1. A list containing the index or indices for the new subnode.
                2. The operation type ('insert' in this case).
                3. The Node instance to insert, either provided or created from **kwargs.
            - Existing subnodes at and after the specified index are shifted to make room for the new subnode.
        """
        return self._modify_subnodes([index_list] if isinstance(index_list, int) else index_list, 'insert', node, **kwargs)

    def add_subnode(self, node=None, **kwargs):
        """
        Add a subnode to the current node and return the modified node.

        Parameters:
            node (Node, optional): An existing Node instance to add as a subnode. If None, a new node will be created based on the **kwargs.
            **kwargs: Optional parameters in dictionary format for creating a new node. Can include 'title', 'subnodes', and any extra fields. 'Subnodes', if provided, undergo type-checking and conversion to Node instances as needed.

        Returns:
            Node: The modified node, allowing for method chaining.

        Behavior:
            - Utilizes the private '_modify_subnodes' method to handle subnode management.
            - '_modify_subnodes' is called with:
                1. A list specifying the index for the new subnode.
                2. The operation type, which is 'add' in this case.
                3. The Node instance to add, either provided or created from **kwargs.
        """
        return self._modify_subnodes([len(self.subnodes)], 'add', node, **kwargs)

    def next(self):
        """
        Navigate to the next node in a depth-first traversal of the tree and return it.

        Returns:
            Node or None: The next node in the depth-first traversal, or None if the end of the tree is reached.

        Behavior:
            - Initially, the 'current_node' is None. After the first call to 'next', it becomes the root node.
            - Resets the 'reached_tree_start' flag to False, as the traversal moves forward.
            - If 'reached_tree_end' is True, returns None.
            - If the current node has subnodes, moves to the first subnode.
            - If the current node has no subnodes, moves to the next sibling.
            - If there is no next sibling, traverses up the tree to find an ancestor with an unvisited sibling. Sets 'reached_tree_end' to True if none is found.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node('Root')
            child1 = Node('Child1')
            child2 = Node('Child2')
            root.add_subnodes(child1, child2)
            # Traverse the tree using the 'next' method
            root_node = root.next()  # Returns the root node on the first call
            child1_node = root.next()  # Returns the child1 node on the second call
        """
        # Reset the flag since we are going forwards.
        self.reached_tree_start = False

        if self.reached_tree_end:
            return None

        if self._current_node is None:
            self._current_node = self
        else:
            if self._current_node.subnodes:
                self._current_node = self._current_node.subnodes[0]
            else:
                parent = self._current_node._parent
                while parent:
                    index = parent.subnodes.index(self._current_node)
                    if index < len(parent.subnodes) - 1:
                        self._current_node = parent.subnodes[index + 1]
                        return self.current_node
                    else:
                        if parent == self:
                            self.reached_tree_end = True
                            return None
                        self._current_node = parent
                        parent = parent._parent
        return self._current_node

    def get_path(self):
        """
        Retrieve the path from the root to the current node as a list of indices.

        Returns:
            list: A list of indices representing the path from the root to the current node.

        Behavior:
            - Initializes an empty list 'path' to store the indices.
            - Iteratively traverses up the tree from the current node to the root.
            - Inserts the index of each node in its parent's subnodes list at the beginning of 'path'.
            - Returns 'path'.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            grandchild1 = Node("Grandchild1")
            child1.add_subnodes(grandchild1)
            root.add_subnodes(child1, child2)

            # Get the path for grandchild1
            path = grandchild1.get_path()  # Returns [0, 0]
        """
        this = self
        parent = this.parent
        path = []
        while parent:
            path.insert(0, parent.subnodes.index(this))
            this = parent
            parent = parent.parent
        return path

    def end(self, from_root=False):
        """
        Set the current node to the deepest last node in the subtree rooted at the current node.

        Parameters:
            from_root (bool): If True, considers the ultimate root as the starting point; otherwise, starts from the current node. Default is False.

        Returns:
            Node: The deepest last node in the subtree.

        Behavior:
            - Calls 'get_end_node' to retrieve the deepest last node in the subtree.
            - Sets '_current_node' to the obtained end node.
            - Returns '_current_node'.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            grandchild2 = Node("Grandchild2")
            child2.add_subnodes(grandchild2)
            root.add_subnodes(child1, child2)

            # Set the current node to the end node
            end_node = root.end()  # Returns 'grandchild2'
        """
        self._current_node = self.get_end_node(from_root)
        return self._current_node

    def prev(self):
        """
        Navigate to the previous node in a depth-first traversal of the tree and return it.

        Returns:
            Node or None: The previous node in the depth-first traversal, or None if the start of the tree is reached.

        Behavior:
            - Resets the 'reached_tree_end' flag to False, as the traversal moves backward.
            - If 'reached_tree_start' is True or the 'current_node' is None, returns None and sets 'reached_tree_start' to True.
            - If the current node is not the first sibling, moves to the previous sibling and navigates to its last descendant.
            - If it is the first sibling, moves to the parent node.
            - If there is no parent (i.e., the node is the root), sets 'reached_tree_start' to True.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node('Root')
            child1 = Node('Child1')
            child2 = Node('Child2')
            root.add_subnodes(child1, child2)
            # Traverse to the end of the tree
            while root.next():
                pass
            # Traverse the tree using the 'prev' method
            prev_node = root.prev()  # Returns the last node in the tree on the first call
        """
        # Reset the flag since we are going backwards.
        self.reached_tree_end = False

        if self.reached_tree_start:
            return None

        if self._current_node is None or self._current_node == self:
            self.reached_tree_start = True
            return None

        parent = self._current_node._parent
        if parent:
            index = parent.subnodes.index(self._current_node)
            if index > 0:
                self._current_node = parent.subnodes[index - 1]
                while self._current_node.subnodes:
                    self._current_node = self._current_node.subnodes[-1]
            else:
                self._current_node = parent
        return self._current_node

    def set_current_node_by_index(self, index):
        """
        Sets the current node based on a given index path.

        Parameters:
            index (list): A list of integers representing the index path from the current node to the target node.

        Raises:
            IndexError: If the index is out of bounds.

        Logic Explained:
            - Starts at the current node.
            - Iteratively navigates to the subnode at each index in the list.
            - Sets the current node to the final node reached.
        """
        self._current_node = self.get_node_by_index(index)
        return self._current_node

    def get_node_by_index(self, index):
        """
        Retrieve a node based on a given index path from the current node.

        Parameters:
            index (list or int): A list of integers or a single integer representing the index path from the current node to the target node.

        Returns:
            Node: The node at the specified index path.

        Raises:
            IndexError: If the index is out of bounds.

        Behavior:
            - Starts at the current node.
            - Iteratively navigates to the subnode at each index in the list or the single integer.
            - Returns the final node reached.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)
            # Get a node by index
            target_node = root.get_node_by_index([1])  # Returns 'child2'
            target_node = root.get_node_by_index(1)  # Also returns 'child2'
        """
        node = self
        for i in [index] if isinstance(index, int) else index:
            node = node.subnodes[i]
        return node

    def get_root_node(self):
        """
        Retrieve the ultimate root node of the tree to which the current node belongs.

        Returns:
            Node: The ultimate root node of the tree.

        Behavior:
            - Calls the 'get_root_and_target' method with 'from_root=True' to determine the ultimate root node.
            - The second element of the tuple returned by 'get_root_and_target' is ignored.
            - Returns the obtained root node.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            root.add_subnodes(child1)
            # Get the root node
            root_node = child1.get_root_node()  # Returns 'root'
        """
        root, _ = self.get_root_and_target(True)
        return root

    def get_last_node(self, from_root=False):
        """
        Retrieve the last subnode of the current node, if any.

        Parameters:
            from_root (bool): If True, considers the ultimate root as the starting point; otherwise, starts from the current node. Default is False.

        Returns:
            Node or None: The last subnode of the current node, or None if the current node has no subnodes.

        Behavior:
            - Checks the 'subnodes' list of the current node.
            - Returns the last element if the list is not empty; otherwise, returns None.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node('Root')
            child1 = Node('Child1')
            child2 = Node('Child2')
            child3 = Node('Child3')
            grandchild1 = Node('Grandchild1')
            child2.add_subnodes(grandchild1)
            root.add_subnodes(child1, child2, child3)
            # Get the last subnode
            last_node = root.get_last_node()  # Returns 'child3' as the last subnode
            # Note: This is equivalent to root.subnodes[-1]
        """
        subnodes = self.get_root_node().subnodes if from_root else self.subnodes
        return subnodes[-1] if subnodes else None

    def get_end_node(self, from_root=False):
        """
        Retrieve the deepest last node in the subtree rooted at the current node.

        Parameters:
            from_root (bool): If True, considers the ultimate root as the starting point; otherwise, starts from the current node. Default is False.

        Returns:
            Node: The deepest last node in the subtree.

        Behavior:
            - Calls 'get_root_and_target' to get the root node based on 'from_root'.
            - Iteratively traverses to the last node at each level to find the end node.
            - Returns the obtained end node.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node('Root')
            child1 = Node('Child1')
            child2 = Node('Child2')
            grandchild1 = Node('Grandchild1')
            grandchild2 = Node('Grandchild2')
            child2.add_subnodes(grandchild1, grandchild2)
            root.add_subnodes(child1, child2)
            # Get the end node
            end_node = root.get_end_node()  # Returns 'grandchild2' as the deepest last node
        """
        node, _ = self.get_root_and_target(from_root)
        end = node
        while True:
            node = node.get_last_node()
            if node:
                end = node
            else:
                break
        return end

    def get_root_and_target(self, from_root=True):
        """
        Retrieve the root and target nodes based on the current node and an optional flag.

        Parameters:
            from_root (bool): Determines the root node. If True, finds the ultimate root of the tree; otherwise, treats the current node as the root. Default is True.

        Returns:
            tuple: (root, target)
                - root: The ultimate root or the current node, depending on 'from_root'.
                - target: The node currently pointed to by the 'root'.

        Behavior:
            - If a parent node exists, the method traverses upwards to find the ultimate root of the tree.
            - The 'root' and 'target' are determined as follows:
                1. When 'from_root' is True and a parent exists:
                    - 'root' is set to the ultimate root of the tree.
                    - 'target' is set to the current node of this ultimate root.
                2. When 'from_root' is False:
                    - 'root' is set to the current node.
                    - If a parent exists, 'target' is set to the current node of the ultimate root.
                    - If no parent exists, 'target' is set to the current node of the 'root'.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            root.add_subnodes(child1)
            # Get the root and target nodes
            root, target = child1.get_root_and_target()  # Returns ('root', 'child1')
        """
        if self._parent:
            parent = self._parent
            while parent:
                if parent._parent:
                    parent = parent._parent
                else:
                    break

        if from_root and self._parent:
            root = parent
            target = root._current_node
        else:
            root = self
            if self._parent:
                target = parent._current_node
            else:
                target = root._current_node
        return root, target

    def get_current_node(self):
        """
        Retrieve the current node in the tree traversal.

        Returns:
            Node or None: The current node in the depth-first traversal, or None if no node has been traversed yet.

        Behavior:
            - Returns the value of the '_current_node' attribute.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)
            root.next().next()
            # Get the current node
            current_node = root.get_current_node()  # Returns Child2
        """
        return self._current_node

    def get_parent(self):
        """
        Retrieve the parent node of the current node.

        Returns:
            Node or None: The parent node of the current node, or None if the current node is the root.

        Behavior:
            - Accesses the '_parent' attribute of the current node.
            - Returns the value of the '_parent' attribute.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            root.add_subnodes(child1)
            # Get the parent node
            parent_node = child1.get_parent()  # Returns 'root'
        """
        return self._parent

    def get_current_node_index(self, from_root=True):
        """
        Retrieve the index path of the current node based on the 'from_root' parameter.

        Parameters:
            from_root (bool): If True, considers the ultimate root of the tree as the starting point; otherwise, starts from the current node itself. Default is True.

        Returns:
            list: A list of integers representing the index path to the current node, either from the ultimate root or the current node based on 'from_root'.

        Behavior:
            - Fetches the root and target nodes using the 'get_root_and_target' method.
            - Initializes an empty list called 'path'.
            - Traverses the tree from the root node to find the target node.
            - Updates 'path' during traversal to capture the index-based route to the target node.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)
            # Get the index path of the current node
            index_path = root.get_current_node_index()  # Returns [] if 'current_node' is None or the root
        """
        root, target = self.get_root_and_target(from_root)

        path = []

        def traverse(node, current_path):
            nonlocal path
            if node == target:
                path = current_path
                return True
            if node:
                for i, subnode in enumerate(node.subnodes):
                    if traverse(subnode, current_path + [i]):
                        return True
            return False

        traverse(root, [])

        return path

    def pretty_print(self, indent=0):
        """
        Recursively print the tree rooted at the current node in a formatted manner.

        Parameters:
            indent (int): The current indentation level for the printout. Default is 0.

        Behavior:
            - Prints the string representation of the current node, indented by the specified amount.
            - Recursively traverses and prints all subnodes, incrementing the indentation level by 1 for each level.

        Examples:
            # Initialize a tree with root and two child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)

            # Pretty print the tree
            root.pretty_print()  
            # Output:
            # Root
            #   Child1
            #   Child2
        """
        print('  ' * indent + str(self))
        for subnode in self.subnodes:
            subnode.pretty_print(indent + 1)

    def __repr__(self):
        """
        Generate a string representation of the Node instance.

        Returns:
            str: A string that represents the Node instance, including its title, number of subnodes, and fields.

        Behavior:
            - Calls `str(self)` to get the string representation of the Node's title.
            - Counts the number of subnodes using `len(self.subnodes)`.
            - Includes the fields dictionary in the representation.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root", extra_field="extra_value")
            child1 = Node("Child1")
            root.add_subnodes(child1)

            # Generate string representation
            repr_string = repr(root)  # Returns "llmmanugen.Node(Root subnodes=1 fields={'extra_field': 'extra_value'})"
        """
        return f"llmmanugen.Node({str(self)} subnodes={len(self.subnodes)} fields={self.fields})"

    def __str__(self):
        """
        Returns a string representation of the current node.

        Returns:
            str: The title of the node if set, otherwise a default string containing
            the node's internal ID and its Python object ID.

        Behavior:
            1. If a title is set for the node, returns the title.
            2. If no title is set, returns a string in the format "Node-{internal ID} (ID: {Python object ID})".
        """
        return str(self._title) if self._title else f"Node-{self._id} (ID: {id(self)})"

    def remove(self, index=None):
        """
        Remove a node based on its index path, multiple subnodes based on their indices or clear all subnodes of the current node.

        Parameters:
            index (list|int, optional): List of indices or an integer specifying the subnodes to remove. Represents the index route to the target node(s).

        Returns:
            Node: The modified node, allowing for method chaining.

        Behavior:
            - If 'index' is provided, navigates to the specified node and removes it, along with its subnodes.
            - If 'index' is omitted or an empty list is given, clears all subnodes of the current node.
            - Sorts the indices in reverse order to avoid index shifts during removal.
            - Iterates through each index in the sorted list.
            - Calls the 'remove' method for each index to remove the corresponding subnode.

        Examples:
            1. To remove the first subnode:
                node.remove(1)
            2. To remove a specific subnodes:
                node.remove([0, 1])  # Removes the first and the second subnodes.
            3. To remove subnode from path:
                node.remove([[0, 1]])  # Removes the second child of the first child of 'node'.
            4. To clear all subnodes:
                node.remove()
        """
        if index is not None:
            if isinstance(index, int):
                del self.subnodes[index]
                return self
            else:
                # Sorting index based on length and value, in reverse order
                index.sort(key=lambda x: (len(x) if isinstance(x, list) else 0, x), reverse=True)

            for idx in index:
                if isinstance(idx, list):
                    parent_node = self.get_node_by_index(idx[:-1])
                    del parent_node.subnodes[idx[-1]]
                else:
                    del self.subnodes[idx]
        else:
            # Remove all subnodes
            self.subnodes = []

        return self

    def add_subnodes(self, *nodes):
        """
        Add multiple subnodes to the current node and return the modified node.

        Parameters:
            *nodes (Node): A variable number of Node instances to add as subnodes.

        Returns:
            Node: The modified node, allowing for method chaining.

        Behavior:
            - Iterates through the variable argument list of nodes.
            - Invokes the 'add_subnode' method for each node, adding it as a subnode and setting its parent.

        Example:
            root = Node("Root")
            child1, child2, child3 = Node("Child1"), Node("Child2"), Node("Child3")
            root.add_subnodes(child1, child2, child3)
        """
        for node in nodes:
            self.add_subnode(node)

        return self

    def insert_subnodes(self, index, *nodes):
        """
        Insert multiple subnodes at a specified index, shifting subsequent subnodes, and return the modified node.

        Parameters:
            index (int): The index specifying where to insert the new subnodes.
            *nodes (Node): A variable number of Node instances to insert as subnodes.

        Returns:
            Node: The modified node, allowing for method chaining.

        Behavior:
            - Iterates through the variable argument list of nodes.
            - Invokes the 'insert_subnode' method for each node, inserting it at the specified index and shifting subsequent subnodes.
        """
        for node in nodes:
            self.insert_subnode(index, node)

    def __iter__(self):
        """
        Make the Node instance iterable.

        Returns:
            Node: The current instance, making it iterable.

        Behavior:
            - The Node class itself serves as an iterator.
            - Enables the use of the instance in 'for' loops and other iterable contexts.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)

            # Iterate through the tree using the Node instance
            for node in root:
                print(node.title)
        """
        return self

    def __next__(self):
        """
        Returns the next node in the depth-first traversal.

        Returns:
            Node: The next node in the depth-first traversal.

        Raises:
            StopIteration: If the traversal reaches the end of the tree.

        Behavior:
            - Calls the 'next' method to get the next node.
            - If the next node is None (end of the tree), raise StopIteration.
            - Otherwise, returns the next node.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node('Root')
            child1 = Node('Child1')
            child2 = Node('Child2')
            root.add_subnodes(child1, child2)

            # Create an iterator object
            node_iterator = iter(root)

            # Use __next__ to traverse the tree
            first_node = next(node_iterator)  # Returns 'Root'
            second_node = next(node_iterator)  # Returns 'Child1'
            third_node = next(node_iterator)  # Returns 'Child2'

            # Raises StopIteration when there are no more nodes to traverse
            try:
                fourth_node = next(node_iterator)
            except StopIteration:
                print('End of tree reached.')
        """
        node = self.next()
        if node is None:
            raise StopIteration
        return node

    def search(self, query, path=None):
        """
        Search for nodes whose titles match a given query.

        Parameters:
            query (str or re.Pattern): The search query, either a string or a regular expression pattern.
            path (list, optional): A list of indices representing the path to start the search from. Default is None.

        Returns:
            list: A list of tuples, each containing a matching node and its path.

        Behavior:
            - Initializes an empty list 'results' to store matching nodes and their paths.
            - Defines a nested function 'traverse' to recursively search for nodes with matching titles.
            - Calls 'traverse' starting from the current node's subnodes.
            - Appends matching nodes and their paths to 'results'.
            - Returns 'results'.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node('Root')
            child1 = Node('Child1')
            child2 = Node('Child2')
            root.add_subnodes(child1, child2)

            # Search for nodes with title containing 'Child'
            result = root.search('Child')  # Returns [(child1, [0]), (child2, [1])]
        """
        results = []

        def traverse(subnodes, new_path=[]):
            for i, node in enumerate(subnodes):
                local_path = new_path + [i]
                if ((isinstance(query, str) and query.lower() in node.title.lower()) or
                    (isinstance(query, re.Pattern) and query.search(node.title))):
                    if path is None or path == local_path[:len(path)]:
                        results.append((node, local_path))
                if node.has_subnodes():
                    traverse(node.subnodes, local_path)
        traverse(self.subnodes)
        return results

    def find_path_by_titles(self, titles):
        """
        Locate nodes by matching their titles to a list of specified field values.

        Parameters:
            titles (list or str): Field values to match against node titles. Can be a single string or a list of strings.

        Returns:
            list: A list of tuples, each containing a node and its path that matches the field values.

        Behavior:
            - Converts 'titles' to a list if it's a single string.
            - Initializes an empty list 'results' to store matching nodes and their paths.
            - Defines a recursive function 'traverse' to search for nodes with matching titles.
            - Calls 'traverse' starting from the current node's subnodes, passing the list of remaining titles to match.
            - Appends matching nodes and their paths to 'results'.
            - Returns 'results'.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            grandchild1 = Node("Grandchild1")
            child2.add_subnodes(grandchild1)
            root.add_subnodes(child1, child2)

            # Find path by titles
            result = root.find_path_by_titles(["Child2", "Grandchild1"])  # Returns [(grandchild1, [1, 0])]
        """
        if not isinstance(titles, list):
            titles = [titles]

        results = []

        def traverse(subnodes, remaining_titles, new_path=[]):
            for i, node in enumerate(subnodes):
                if remaining_titles and node.title == remaining_titles[0]:
                    local_path = new_path + [i]
                    if len(remaining_titles) == 1:
                        results.append((node, local_path))
                    if node.has_subnodes():
                        return traverse(node.subnodes, remaining_titles[1:], local_path)
        traverse(self.subnodes, titles)
        return results

    def __sub__(self, other):
        """
        Remove subnodes by index or list of indices.

        Parameters:
            other (Union[int, list]): The index or list of indices of subnodes to remove.

        Returns:
            Node: The modified Node object with the specified subnodes removed.

        Raises:
            TypeError: If the provided argument is not an integer or a list.

        Behavior:
            - Checks if `other` is an integer or a list.
            - Calls the `remove` method to remove the subnode(s) at the specified index or indices.

        Examples:
            # Initialize a Node with subnodes
            node = Node('Node1')
            node.add_subnodes(Node('Child1'), Node('Child2'))

            # Remove subnode by index
            node - 0  # Removes the first subnode
        """
        if isinstance(other, int) or isinstance(other, list):
            return self.remove(other)
        else:
            raise TypeError("Unsupported type for substraction")

    def __add__(self, other):
        """
        Add subnodes to the Node.

        Parameters:
            other (Union[list, tuple, Node]): The subnode(s) to add.

        Returns:
            Node: The modified Node object with the new subnodes added.

        Behavior:
            - Checks if `other` is a list or a tuple.
            - Calls `add_subnodes` if `other` is a list or tuple, otherwise calls `add_subnode`.

        Examples:
            # Initialize Nodes
            node1 = Node('Node1')
            node2 = Node('Node2')
            node3 = Node('Node3')

            # Add multiple subnodes
            result1 = (node1 + node2) + node3  # Equivalent to node1.add_subnode(node2).add_subnode(node3)

            # Reset node1 for the next example
            node1 = Node('Node1')

            # Different precedence
            result2 = node1 + (node2 + node3)  # Equivalent to node2.add_subnode(node3), then node1.add_subnode(node2)

            # Note: result1 and result2 will not be the same due to the different precedence in addition.
        """
        if isinstance(other, list) or isinstance(other, tuple):
            self.add_subnodes(*other)
        else:
            self.add_subnode(other)
        return self

    def __lt__(self, other):
        """
        Add a new subnode or multiple subnodes to the current node at the first subnode index using the '<' operator.

        Parameters:
            other (Node or list[Node] or tuple[Node]): The node(s) to add as subnodes.

        Returns:
            Node: The last added subnode.

        Behavior:
            - Checks the type of 'other' to determine if it's a single node or a list/tuple of nodes.
            - Calls 'insert_subnode' if 'other' is a single node.
            - Calls 'insert_subnodes' if 'other' is a list or tuple of nodes.
            - Returns the last inserted subnode.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")

            # Add a single subnode using the '<' operator
            root < child1  # Returns 'child1'. Root has one child now.

            # Add multiple subnodes using the '<' operator
            child2 = Node("Child2")
            child3 = Node("Child3")
            last_added_node = root < [child2, child3]  # Returns 'child3'
        """
        if isinstance(other, list) or isinstance(other, tuple):
            self.insert_subnodes(0, *other)
        else:
            self.insert_subnode(0, other)
        return self.subnodes[0]

    def __gt__(self, other):
        """
        Add (append) a new subnode or multiple subnodes to the current node at the last subnode index using the '>' operator.

        Parameters:
            other (Node or list[Node] or tuple[Node]): The node(s) to add as subnodes.

        Returns:
            Node: The last added subnode.

        Behavior:
            - Checks the type of 'other' to determine if it's a single node or a list/tuple of nodes.
            - Calls 'add_subnode' if 'other' is a single node.
            - Calls 'add_subnodes' if 'other' is a list or tuple of nodes.
            - Returns the last added subnode.

        Examples:
            # Initialize a tree with root and child nodes
            root = Node("Root")
            child1 = Node("Child1")

            # Add a single subnode using the '>' operator
            root > child1  # Returns 'child1'. Root has one child now.

            # Add multiple subnodes using the '>' operator
            child2 = Node("Child2")
            child3 = Node("Child3")
            last_added_node = root > [child2, child3]  # Returns 'child3'
        """
        if isinstance(other, list) or isinstance(other, tuple):
            self.add_subnodes(*other)
        else:
            self.add_subnode(other)
        return self.subnodes[-1]

    def __getattr__(self, key):
        """
        Retrieve the value of an attribute or field by key.

        Parameters:
            key (str): The name of the attribute or field to retrieve.

        Returns:
            Any: The value of the attribute or field.

        Raises:
            AttributeError: If the key is not found in either the Node's attributes or fields.

        Behavior:
            - Checks if the key exists in the Node's attributes using `key in self.__dict__`.
            - If it exists, returns the value using `self.__getitem__(key)`.
            - Checks if the key exists in the `fields` dictionary.
            - If it exists, returns the value from `fields`.
            - If the key is not found in either, raises an AttributeError.

        Examples:
            # Initialize a Node with fields
            node = Node("Node1", extra_field="extra_value")

            # Retrieve value by key
            value = node.extra_field  # Returns 'extra_value'
        """
        if key in self.__dict__:
            return self.__getitem__(key)
        elif key in self.fields:
            return self.fields[key]
        else:
             raise AttributeError(f"Attribute '{key}' not found from the Node attributes or fields")

    def __getitem__(self, key):
        """
        Access an attribute, field, or subnode by key or index.

        Parameters:
            key (Union[str, int, slice]): The name or index of the attribute, field, or subnode to access.

        Returns:
            Any: The value of the attribute, field, or subnode.

        Raises:
            KeyError: If the key is not an attribute, field, or index of a subnode.

        Behavior:
            - If the key is an integer or slice, returns the corresponding subnode(s).
            - Uses `hasattr(self, key)` to check for an attribute with the given key.
            - Returns the attribute value using `getattr(self, key)` if it exists.
            - Checks for the key in the `fields` dictionary if the attribute doesn't exist.
            - Raises a KeyError if the key is not found in attributes, fields, or subnodes.

        Examples:
            # Initialize a Node with fields and subnodes
            node = Node('Node1', extra_field='extra_value')
            node.subnodes = [Node('Child1'), Node('Child2')]

            # Access value by key
            value = node['extra_field']  # Returns 'extra_value'
            value = node[0]  # Returns the first subnode
            value = node['title']  # Raises KeyError
        """
        if isinstance(key, int) or isinstance(key, slice):
            return self.subnodes[key]
        elif hasattr(self, key):
            return getattr(self, key)
        elif key in self.fields:
            return self.fields[key]
        else:
            raise KeyError(f"Key '{key}' not found from the Node attributes or fields")

    def __setitem__(self, key, value):
        """
        Set the value of an attribute or field by key.

        Parameters:
            key (str): The name of the attribute or field to set.
            value (Any): The value to set for the attribute or field.

        Behavior:
            - Checks if the Node has an attribute with the given key using `hasattr(self, key)`.
            - If the attribute exists, sets its value using `setattr(self, key, value)`.
            - Checks if the key exists in the `fields` dictionary.
            - If the key exists in `fields`, updates its value.

        Examples:
            # Initialize a Node with fields
            node = Node('Node1', extra_field='extra_value')

            # Set value by key
            node['extra_field'] = 'new_value'  # Updates 'extra_field' in both attribute and fields dictionary
        """
        if hasattr(self, key):
            setattr(self, key, value)
        if key in self.fields:
            self.fields[key] = value

    def __setattr__(self, key, value):
        """
        Set the value of an attribute or field by key.

        Parameters:
            key (str): The name of the attribute or field to set.
            value (Any): The value to set for the attribute or field.

        Behavior:
            - Calls the superclass' `__setattr__` method to set the attribute.
            - Checks if the key exists in the `fields` dictionary.
            - If the key exists in `fields`, updates its value.

        Examples:
            # Initialize a Node with fields
            node = Node('Node1', extra_field='extra_value')

            # Set value by key
            node.extra_field = 'new_value'  # Updates 'extra_field' in both attribute and fields dictionary
        """
        super().__setattr__(key, value)
        if "fields" in self.__dict__ and key in self.__dict__["fields"]:
            self.fields[key] = value

    def __delattr__(self, key):
        """
        Delete an attribute or field by key.

        Parameters:
            key (str): The name of the attribute or field to delete.

        Behavior:
            - Calls the superclass' `__delattr__` method to delete the attribute.
            - Checks if the key exists in the `fields` dictionary.
            - If the key exists in `fields`, deletes it from the dictionary.

        Examples:
            # Initialize a Node with fields
            node = Node('Node1', extra_field='extra_value')

            # Delete value by key
            del node.extra_field  # Deletes 'extra_field' from both attribute and fields dictionary
        """
        try:
            super().__delattr__(key)
        except:
            pass
        if "fields" in self.__dict__ and key in self.__dict__["fields"]:
            del self.fields[key]

    def __delitem__(self, key):
        """
        Delete an attribute or field by key using dictionary-like syntax.

        Parameters:
            key (str): The name of the attribute or field to delete.

        Behavior:
            - Checks if the object has an attribute with the name specified by `key`.
            - If such an attribute exists, deletes it using `delattr`.
            - Checks if the key exists in the `fields` dictionary.
            - If the key exists in `fields`, deletes it from the dictionary.

        Examples:
            # Initialize a Node with fields
            node = Node('Node1', extra_field='extra_value')

            # Delete value by key using dictionary-like syntax
            del node['extra_field']  # Deletes 'extra_field' from both attribute and fields dictionary
        """
        if hasattr(self, key):
            delattr(self, key)
        if key in self.fields:
            del self.fields[key]
