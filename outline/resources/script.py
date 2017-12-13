import sys
from os.path import join, dirname, basename
from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
import json


class Node(object):
    def __init__(self, type, label, icon, start, end):
        self.type = type
        self.label = label
        self.icon = icon
        self.start = start
        self.end = end
        self.children = []


class Tree(object):
    def __init__(self):
        self.text = sys.argv[1]
        self.language_model = self.get_language_model()
        self.outline_model = self.get_outline_model()
        self.nodes = []
        self.start_position_in_lines = []
        self.fill_end_position_in_lines()
        self.visit_rule(self.language_model)
        self.make_tree()

    def get_language_model(self):
        language = metamodel_from_file(join(dirname(__file__), 'language.tx'))
        grammar_model = language.model_from_str(self.text)
        return grammar_model

    def get_outline_model(self):
        this_folder = dirname(__file__)
        language = metamodel_from_file(join(dirname(__file__), 'outline.tx'))
        grammar_model = language.model_from_file(join(this_folder, 'outline.ol'))
        return grammar_model

    def fill_end_position_in_lines(self):
        counter = 0
        for line in self.text.splitlines():
            self.start_position_in_lines.append(counter)
            counter += len(line) + 2
        self.start_position_in_lines.append(sys.maxsize)

    def visit_rule(self, rule, mult='1'):
        if (mult == '1'):
            subrules = rule._tx_attrs
            values = {}
            for subrule in subrules:
                child = getattr(rule, subrule)
                attr = subrules[subrule]
                if attr.cont == False:
                    if attr.mult == '1':
                        values[subrule] = child.name
                        continue
                    else:
                        for item in child:
                            self.proccess_rule(values, rule, item.name)
                        continue
                if child == None:
                    continue
                if attr.ref == False:
                    values[subrule] = child
                    continue
                self.visit_rule(child, attr.mult)
            self.proccess_rule(values, rule)
        else:
            for item in rule:
                self.visit_rule(item)

    def proccess_rule(self, values, rule, label=None):
        rule_name = type(rule).__name__
        if len(values) == 0 and label == None:
            return
        for outline_rule in self.outline_model.rules:
            if outline_rule.name == rule_name:
                if label == None:
                    label = self.get_label(values, outline_rule.label.names)
                icon = None
                if outline_rule.icon != None:
                    icon = outline_rule.icon.path
                node = Node(rule_name, label, icon, rule._tx_position, rule._tx_position_end)
                self.nodes.append(node)

    def get_label(self, values, names):
        label = ""
        for name in names:
            for key, value in values.items():
                if name.id == key:
                    label += value
                    break
                if name.string != '':
                    label += name.string
                    break
        return label

    def make_tree(self):
        children = self.determine_parent_child_relation()
        for node in self.nodes:
            if node in self.nodes:
                self.remove_grandchildren(node)
        for child in children:
            if child in self.nodes:
                self.nodes.remove(child)
        self.tree = self.make_nodes()

    def determine_parent_child_relation(self):
        children = []
        for parent in self.nodes:
            for child in self.nodes:
                if self.is_parent_child_relation_valid(parent, child):
                    children.append(child)
                    parent.children.append(child)
        return children

    def is_parent_child_relation_valid(self, parent, child):
        if parent.start < child.start and parent.end > child.end:
            return True
        return False

    def remove_grandchildren(self, node):
        children = []
        for child in node.children:
            for grandchild in child.children:
                if grandchild not in children:
                    children.append(grandchild)
        for child in children:
            if child in self.nodes:
                node.children.remove(child)

    def make_nodes(self, nodes=None):
        objects = []
        if nodes == None:
            nodes = self.nodes
        else:
            nodes = nodes.children
        for node in nodes:
            obj = {}
            obj['type'] = node.type
            obj['label'] = node.label
            obj['icon'] = node.icon
            obj['children'] = self.make_nodes(node)
            point = self.convert_position_in_point(node.start)
            obj['start_line'] = point['row']
            obj['start_point_in_line'] = point['column']
            point = self.convert_position_in_point(node.end)
            obj['end_line'] = point['row']
            obj['end_point_in_line'] = point['column']
            objects.append(obj)
        return objects

    def convert_position_in_point(self, position):
        point = {}
        for line in range(len(self.start_position_in_lines)):
            if position < self.start_position_in_lines[line]:
                point['row'] = line - 1
                point['column'] = position - self.start_position_in_lines[line - 1]
                break
        return point

tree = Tree()
print(json.dumps(tree.tree))
