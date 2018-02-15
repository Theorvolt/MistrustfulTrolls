from pynode.main import *
import queue
import random

def begin():
        seen = [False] * 128
        bfs_queue = queue.Queue()

        # Create the next situation by adding a new node and/or edge
        def next_situation(node, data):
            binary_id = int (''.join(map(str, data)),2)
            new_node = None
	
            # Add a new node, or connect to an existing one
            if seen[binary_id]:
                if not graph.adjacent(node, binary_id):
                    graph.add_edge(node, binary_id, directed=True)
            else:
                new_node = graph.add_node(binary_id, "".join(map(str, data))).set_attribute("data", data)
                graph.add_edge(node, new_node, directed=True)
                seen[binary_id] = True
                return new_node

        start = graph.add_node(0, "0000000").set_attribute("data", [0, 0, 0, 0, 0, 0, 0])
        end = None
        seen[0] = True
        bfs_queue.put(start)

        while not bfs_queue.empty():
                node = bfs_queue.get()
                node.set_color(Color.RED)
                node.highlight()
                data = node.attribute("data")

                if data == [1, 1, 1, 1, 1, 1, 1]:
                        end = node

                    # Try adding all possible new nodes
                boat_side = data[6]
                new_boat_side = (data[6] + 1) % 2

                curr_trolls = (1 if data[0] == data[6] else 0) + (1 if data[1] == data[6] else 0) + (1 if data[2] == data[6] else 0) 
                curr_other = 3 - curr_trolls

                for i in range(0,3):
                        if data[i+3] == boat_side and data[i] != data[i+3]:
                                if curr_other > 0:
                                        valid = False
                for i in range(0,3):
                        if data[i+3] == new_boat_side and data[i] != data[i+3]:
                                if curr_trolls > 0:
                                        valid = False
                for p1 in range(6):
                        for p2 in range(6):
                                if data[p1] != boat_side or data[p2] != boat_side:
                                        continue
                                new_data = list(data)
                                new_data[6] = new_boat_side
                                new_data[p1] = new_boat_side
                                new_data[p2] = new_boat_side
                                valid = True
                                number_trolls = (1 if new_data[0] == new_data[6] else 0) + (1 if new_data[1] == new_data[6] else 0) + (1 if new_data[2] == new_data[6] else 0) 
                                other_trolls = 3 - number_trolls

                                for i in range(0,3):
                                        if new_data[i+3] == new_boat_side and new_data[i] != new_data[i+3]:
                                                if number_trolls > 0:
                                                        valid = False
                                for i in range(0,3):
                                        if new_data[i+3] == boat_side and new_data[i] != new_data[i+3]:
                                                if other_trolls > 0:
                                                        valid = False
                                if valid == False:
                                        continue

                                new_node = next_situation(node,new_data)
                                if new_node != None:
                                        bfs_queue.put(new_node)


        # Reset node color
        for node in graph.nodes():
            node.set_color(Color.DARK_GREY)

        # Color start and end
        start.set_color(Color.GREEN)
        end.set_color(Color.GREEN)
        
        # Randomly choose path
        path = []
        node = end
        while node is not start:
            edge = node.incoming_edges()[random.randint(0, len(node.incoming_edges()) - 1)]
            path.append(edge)
            node = edge.source()

        # Traverse the path
        for edge in reversed(path):
            edge.traverse(color=Color.GREEN)


begin_pynode(begin)
