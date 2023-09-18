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

### Removing Nodes: `remove()` and `remove_subnodes()`
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
            if isinstance(arg, str):
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
        Resets the current node and boundary flags to their initial states.

        Logic Explained:
            - Sets '_current_node' to None.
            - Sets 'reached_tree_end' to False.
            - Sets 'reached_tree_start' to True.
        """
        self._insert_index = None
        self._remove_index = None
        self._current_node = None
        self.reached_tree_end = False
        self.reached_tree_start = True
        return self

    def has_subnodes(self):
        """
        Checks if the current node has any subnodes.

        Returns:
            bool: True if the current node has subnodes, False otherwise.
        """
        return len(self.subnodes) > 0

    def get_subnodes(self):
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
            str: The node's title.
        """
        return self._title

    @title.setter
    def title(self, title=None):
        """
        Set the title of the node.

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
            Node or None: The parent node, or None if the node is the root.

        Behavior:
            - Retrieves the value from the private attribute '_parent'.
            - The '_parent' attribute is set during initialization or when the node is added as a subnode to another node.
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
            next_node = root.next()  # Returns the root node on the first call
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
        Retrieves a node based on a given index path from the current node.

        Parameters:
            index (list): A list of integers representing the index path from the current node to the target node.

        Returns:
            Node: The node at the specified index path.

        Raises:
            IndexError: If the index is out of bounds.

        Logic Explained:
            - Starts at the current node.
            - Iteratively navigates to the subnode at each index in the list.
            - Returns the final node reached.
        """
        node = self
        for i in [index] if isinstance(index, int) else index:
            node = node.subnodes[i]
        return node

    def get_root_node(self):
        """
        Retrieves the root node of the tree to which the current node belongs.

        Returns:
            Node: The ultimate root node of the tree.

        Logic Explained:
            - Calls 'get_root_and_target' method with 'from_root=True' to get the root node.
            - Returns the obtained root node.
        """
        root, _ = self.get_root_and_target(True)
        return root

    def get_last_node(self):
        """
        Retrieves the last subnode of the current node, if any.

        Returns:
            Node or None: The last subnode of the current node, or None if the current node has no subnodes.

        Logic Explained:
            - Checks the 'subnodes' list of the current node.
            - Returns the last element if the list is not empty; otherwise, returns None.
        """
        return self.subnodes[-1] if self.subnodes else None

    def get_end_node(self, from_root=False):
        """
        Retrieves the deepest last node in the subtree rooted at the current node.

        Parameters:
            from_root (bool): If True, considers the ultimate root as the starting point;
                              otherwise, starts from the current node. Default is False.

        Returns:
            Node: The deepest last node in the subtree.

        Logic Explained:
            - Calls 'get_root_and_target' to get the root node based on 'from_root'.
            - Iteratively traverses to the last node at each level to find the end node.
            - Returns the obtained end node.
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
        Retrieves the root and target nodes based on the current node and an optional flag.

        Parameters:
            from_root (bool): Flag to determine the root node. When True, finds the ultimate root
                              of the tree; otherwise, treats the current node as the root. Default is True.

        Returns:
            tuple: (root, target)
                - root: The ultimate root of the tree or the current node, depending on 'from_root'.
                - target: The node currently pointed to by the 'root'.

        Logic Explained:
            - First, if a parent exists, traverse upwards to find the ultimate root of the tree.
            1. When 'from_root' is True and a parent exists:
                - 'root' becomes the ultimate root of the tree.
                - 'target' is set to the current node of this ultimate root.
            2. Otherwise:
                - 'root' is set to the current node.
                - 'target' is determined by the current node of the ultimate root if a parent exists;
                  otherwise, it is set to the current node of the 'root'.
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
        return self._current_node

    def get_parent(self):
        return self._parent

    def get_current_node_index(self, from_root=True):
        """
        Retrieves the index path of the current node based on the 'from_root' parameter.

        Parameters:
            from_root (bool): If True, considers the ultimate root of the tree as the starting point;
                              otherwise, starts from the current node itself. Default is True.

        Returns:
            list: A list of integers representing the index path to the current node,
                  either from the ultimate root or the current node based on 'from_root'.

        Logic Explained:
            1. Fetch the root and target nodes using the 'get_root_and_target' method.
            2. Initialize an empty list called 'path'.
            3. Traverse the tree from the root node to find the target node.
            4. During traversal, update 'path' to capture the index-based route to the target node.
            5. Return the 'path'.

        Note:
            - The 'path' is a list where each element is the index of the node at each level of the tree.
              For example, [0, 1] means the target node is the second child of the first child of the root.
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
        Recursively prints the tree rooted at the current node in a pretty format.

        Parameters:
            indent (int): The current indentation level for the printout. Default is 0.

        Behavior:
            1. Prints the current node's string representation, indented by the specified amount.
            2. Recursively prints all subnodes, increasing the indentation level by 1 for each level.
        """
        print('  ' * indent + str(self))
        for subnode in self.subnodes:
            subnode.pretty_print(indent + 1)

    def __repr__(self):
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
        return self._title if self._title else f"Node-{self._id} (ID: {id(self)})"

    def remove(self, index=None):
        """
        Remove a node based on its index path or clear all subnodes of the current node.

        Parameters:
            index (list|int, optional): An integer or list of integers specifying the index path to the node to remove. If omitted or an empty list is provided, all subnodes are cleared.

        Raises:
            IndexError: If the index path is out of bounds.

        Behavior:
            - If 'index' is provided, navigates to the specified node and removes it, along with its subnodes.
            - If 'index' is omitted or an empty list is given, clears all subnodes of the current node.

        Examples:
            1. To remove a specific subnode:
                node.remove([0, 1])  # Removes the second child of the first child of 'node'.
            2. To clear all subnodes:
                node.remove()
        """
        if index:
            if isinstance(index, int):
                index = [index]
            parent_node = self.get_node_by_index(index[:-1])
            # Remove the node and its subnodes
            del parent_node.subnodes[index[-1]]
        else:
            # Remove all subnodes
            self.subnodes = []

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

    def remove_subnodes(self, index=None):
        """
        Remove multiple subnodes based on their indices and return the modified node.

        Parameters:
            index (list|int, optional): List of indices or an integer specifying the subnodes to remove. Represents the index route to the target node(s).

        Returns:
            Node: The modified node, allowing for method chaining.

        Behavior:
            - Sorts the indices in reverse order to avoid index shifts during removal.
            - Iterates through each index in the sorted list.
            - Calls the 'remove' method for each index to remove the corresponding subnode.

        Examples:
            # Create root node and child nodes
            root = Node("Root")
            child1 = Node("Child1")
            child2 = Node("Child2")
            root.add_subnodes(child1, child2)

            # Remove child nodes by their indices
            root.remove_subnodes([0, 1])

        Note:
            - Indices are removed in reverse order to avoid altering the indices of the nodes yet to be removed.
        """
        index = self._remove_index if index is None else index
        if isinstance(index, int):
            index = [index]
        else:
            # Sorting index based on length and value, in reverse order
            index.sort(key=lambda x: (len(x) if isinstance(x, list) else 0, x), reverse=True)

        for idx in index:
            if isinstance(idx, list):
                parent_node = self.get_node_by_index(idx[:-1])
                del parent_node.subnodes[idx[-1]]
            else:
                del self.subnodes[idx]

        return self

    def __iter__(self):
        """
        Returns the iterator object (self).

        Returns:
            Node: The current instance.

        Behavior:
            1. The Node class itself acts as an iterator.
            2. Returns the instance to support iteration in a for loop.
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
            1. Calls the 'next' method to get the next node.
            2. If the next node is None (end of the tree), raise StopIteration.
            3. Otherwise, returns the next node.
        """
        node = self.next()
        if node is None:
            raise StopIteration
        return node

    def search(self, query, path=None):
        """
        Search for nodes whose titles match the given query.

        Parameters:
            - query (str or re.Pattern): The search query, either a string or a regular expression pattern.
            - path (list, optional): A list of indices representing the path to start the search from.

        Returns:
            list: A list of tuples, each containing a matching node and its path.
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
        Find nodes whose titles match the given list of field values.

        Parameters:
            - titles (list or str): A list of field values to match against node titles.

        Returns:
            list: A list of tuples, each containing a node and its path that matches the field values.
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
        if isinstance(other, int):
            self._remove_index = other
            self.remove_subnodes()
            return self
        else:
            raise TypeError("Unsupported type for substraction")

    def __isub__(self, other):
        if isinstance(other, int):
            self.remove_subnodes(other)
        else:
            raise TypeError("Unsupported type for in-place substraction")
        return self
    
    def __iadd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, int):
            self._insert_index = other
            return self
        if isinstance(other, list) or isinstance(other, tuple):
            self.add_subnodes(*other)
        else:
            if self._insert_index is not None:
                node = self.get_node_by_index(self._insert_index)
                if node:
                    node.add_subnode(other)
                self._insert_index = None
            else:
                self.add_subnode(other)
        return self

    def __igt__(self, other):
        return self.__gt__(other)

    def __gt__(self, other):
        if isinstance(other, list) or isinstance(other, tuple):
            self.add_subnodes(*other)
        else:
            self.add_subnode(other)
        return self.subnodes[-1]

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__getitem__(key)
        elif key in self.fields:
            return self.fields[key]
        else:
             raise AttributeError(f"Attribute '{key}' not found from the Node attributes or fields")

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        elif key in self.fields:
            return self.fields[key]
        else:
            raise KeyError(f"Key '{key}' not found from the Node attributes or fields")

    def __setitem__(self, key, value):
        """
        Sets an attribute by key name and updates the timestamp if the attribute exists.

        Parameters:
            key (str): The name of the attribute to set.
            value: The value to set the attribute to.
        """
        if hasattr(self, key):
            setattr(self, key, value)
        if key in self.fields:
            self.fields[key] = value

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if "fields" in self.__dict__ and key in self.__dict__["fields"]:
            self.fields[key] = value
