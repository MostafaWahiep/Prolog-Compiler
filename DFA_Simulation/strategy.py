from typing import Any
import graphviz as gv
import re


class BaseGraph:
    def __init__(self, name):
        self.g = gv.Digraph(name, filename=name, format='png', comment='DFA')
        self.g.attr(rankdir='LR')
        self.g.attr('node', shape='circle')
        self.g.attr('node', style='filled')
        self.g.attr('node', color='black')
        self.g.attr('node', fillcolor='white')
        self.g.attr('node', fontcolor='black')
        self.g.attr('node', fontname='helvetica')
        self.g.attr('edge', fontname='helvetica')
        self.g.attr('edge', fontsize='10')
        self.g.attr('node', fontsize='10')
        self.g.attr('node', fixedsize='true')
        self.g.attr('node', width='0.5')
        self.g.attr('node', height='0.5')
        self.g.attr('node', margin='0.1')
        self.g.attr('node', penwidth='1')
        self.g.attr('node', ordering='out')
        self.g.attr('node', labelloc='b')
        self.g.attr('node', imagescale='true')
        self.g.attr('node', imagepos='tc')
        self.g.attr('node', labeljust='l')
        self.g.attr('node', labeldistance='1')
        self.g.attr('node', fixedsize='true')
        self.g.attr('node', width='0.5')
        self.g.attr('node', height='0.5')
        self.g.attr('node', margin='0.1')
        self.g.attr('node', penwidth='1')
        self.g.attr('node', ordering='out')
        self.g.attr('node', labelloc='b')
        self.g.attr('node', imagescale='true')
        self.g.attr('node', imagepos='tc')
        self.g.attr('node', labeljust='l')
        self.g.attr('node', labeldistance='1')
        self.g.attr('node', fixedsize='true')
        self.g.attr('node', width='0.5')
        self.g.attr('node', height='0.5')
        self.g.attr('node', margin='0.1')
        self.g.attr('node', penwidth='1')
        self.g.attr('node', ordering='out')
        self.g.attr('node', labelloc='b')
        self.g.attr('node', imagescale='true')
        self.g.attr('node', imagepos='tc')
        self.g.attr('node', labeljust='l')
        self.g.attr('node', labeldistance='1')
        self.g.attr('node', fixedsize='true')
        self.g.attr('node', width='0.5')
        self.g.attr('node', height='0.5')
        self.g.attr('node', margin='0.1')
        self.g.attr('node', penwidth='1')
        self.g.attr('node', ordering='out')
        self.g.attr('node', labelloc='b')
        self.g.attr('node', imagescale='true')
        self.g.attr('node', imagepos='tc')
        self.g.attr('node', labeljust='l')
        self.g.attr('node', labeldistance='1')
        self.g.attr('node', fixedsize='true')
        self.g.attr('graph', dpi='300')

    def add_node(self, name, label, shape='circle', color='black', fillcolor='white', fontcolor='black', fontname='helvetica', fontsize='10', fixedsize='true', width='0.5', height='0.5', margin='0.1', penwidth='1', ordering='out', labelloc='b', imagescale='true', imagepos='tc', labeljust='l', labeldistance='1'):
        self.g.node(name, label, shape=shape, color=color, fillcolor=fillcolor, fontcolor=fontcolor, fontname=fontname, fontsize=fontsize, fixedsize=fixedsize, width=width, height=height,
                    margin=margin, penwidth=penwidth, ordering=ordering, labelloc=labelloc, imagescale=imagescale, imagepos=imagepos, labeljust=labeljust, labeldistance=labeldistance)
        return self.g

    def add_edge(self, start, end, label, color='black', fontcolor='black', fontname='helvetica', fontsize='10', penwidth='1', labeldistance='1', labelangle='0', labeljust='l', labelloc='b', style='solid', arrowhead='normal', arrowsize='1', arrowtail='none', dir='forward', constraint='true'):
        self.g.edge(start, end, label, color=color, fontcolor=fontcolor, fontname=fontname, fontsize=fontsize, penwidth=penwidth, labeldistance=labeldistance, labelangle=labelangle, labeljust=labeljust,
                    labelloc=labelloc, style=style, arrowhead=arrowhead, arrowsize=arrowsize, arrowtail=arrowtail, dir=dir, constraint=constraint)
        return self.g


class DFAGraphCreator:
    def __init__(self, token_type):
        self.token_type = token_type

    def create_graph(self, token):
        return self.token_type.create_graph(token)


class ReservedDataType:

    def create_graph(self, token):
        graph = BaseGraph('Integer')
        graph.add_node('q0', 'q0')
        graph.add_node('q1', 'q1', shape='doublecircle')
        graph.add_node('reject', 'reject')

        graph.add_edge('q0', 'q1', label='[integer]')
        graph.add_edge('q0', 'q1', label='[char]')
        graph.add_edge('q0', 'q1', label='[string]')
        graph.add_edge('q0', 'q1', label='[symbol]')
        graph.add_edge('q0', 'q1', label='[real]')

        graph.add_edge(
            'q0', 'reject', label=f'[^integer|char|string|symbol|real]')
        graph.add_edge('q1', 'reject', label=f'[.*]')
        return graph


class integer:
    def create_graph(self, token):
        graph = BaseGraph('Integer')
        graph.add_node('q0', 'q0')
        graph.add_node('q1', 'q1', shape='doublecircle')
        graph.add_node('reject', 'reject')

        graph.add_edge('q0', 'q1', label='[0-9]')
        graph.add_edge('q1', 'q1', label='[0-9]')
        graph.add_edge('q0', 'reject', label='^[0-9]')
        graph.add_edge('q1', 'reject', label='[^0-9]')
        return graph


class real:
    def create_graph(self, token):
        graph = BaseGraph('Real')
        graph.add_node('q0', 'q0')
        graph.add_node('q1', 'q1')
        graph.add_node('q2', 'q2', shape='doublecircle')
        graph.add_node('reject', 'reject')

        graph.add_edge('q0', 'q0', label='[0-9]')
        graph.add_edge('q0', 'q1', label='[.]')
        graph.add_edge('q1', 'q2', label='[0-9]')
        graph.add_edge('q2', 'q2', label='[0-9]')
        graph.add_edge('q0', 'reject', label='^[0-9]')
        graph.add_edge('q1', 'reject', label='^[.]')
        graph.add_edge('q2', 'reject', label='[^0-9]')
        return graph


class Name:
    def create_graph(self, token):
        graph = BaseGraph('Name')
        graph.add_node('q0', 'q0')
        graph.add_node('q1', 'q1', shape='doublecircle')
        graph.add_node('reject', 'reject')

        graph.add_edge('q0', 'q1', label='[a-z]')
        graph.add_edge('q1', 'q1', label='[a-zA-Z0-9_]')
        graph.add_edge('q0', 'reject', label='^[a-z]')
        graph.add_edge('q1', 'reject', label='[^a-zA-Z0-9_]')
        return graph


class Anonymous:
    def create_graph(self, token):
        graph = BaseGraph('Anonymous')
        graph.add_node('q0', 'q0')
        graph.add_node('q1', 'q1', shape='doublecircle')
        graph.add_node('reject', 'reject')

        graph.add_edge('q0', 'q1', label='[_]')
        graph.add_edge('q0', 'reject', label='^[^_]')
        graph.add_edge('q1', 'reject', label='[^_]')
        return graph


class VariableName:
    def create_graph(self, token):
        graph = BaseGraph('VariableName')
        graph.add_node('q0', 'q0')
        graph.add_node('q1', 'q1')
        graph.add_node('q2', 'q2', shape='doublecircle')
        graph.add_node('reject', 'reject')

        graph.add_edge('q0', 'q1', label='[A-Z_]')
        graph.add_edge('q1', 'q2', label='[a-zA-Z0-9_]')
        graph.add_edge('q2', 'q2', label='[a-zA-Z0-9_]')
        graph.add_edge('q0', 'reject', label='^[A-Z_]')
        graph.add_edge('q1', 'reject', label='^[a-zA-Z0-9_]')
        graph.add_edge('q2', 'reject', label='[^a-zA-Z0-9_]')
        return graph


class String:
    def create_graph(self, token):
        graph = BaseGraph('String')
        graph.add_node('q0', 'q0')
        graph.add_node('q1', 'q1')
        graph.add_node('q2', 'q2')
        graph.add_node('q3', 'q3', shape='doublecircle')
        graph.add_node('reject', 'reject')

        graph.add_edge('q0', 'q1', label='["]')
        graph.add_edge('q1', 'q2', label='[a-zA-Z0-9_]')
        graph.add_edge('q2', 'q2', label='[a-zA-Z0-9_]')
        graph.add_edge('q2', 'q3', label='["]')
        graph.add_edge('q0', 'reject', label='^[^"]')
        graph.add_edge('q1', 'reject', label='^[a-zA-Z0-9_]')
        graph.add_edge('q2', 'reject', label='^[^"]')
        graph.add_edge('q3', 'reject', label='[^"]')
        return graph


class Char:
    def create_graph(self, token):
        graph = BaseGraph('Char')
        graph.add_node('q0', 'q0')
        graph.add_node('q1', 'q1')
        graph.add_node('q2', 'q2')
        graph.add_node('q3', 'q3', shape='doublecircle')

        graph.add_edge('q0', 'q1', label="[']")
        graph.add_edge('q1', 'q2', label='[a-zA-Z0-9_]')
        graph.add_edge('q2', 'q3', label="[']")
        graph.add_edge('q0', 'reject', label='^[^"]')
        graph.add_edge('q1', 'reject', label='^[a-zA-Z0-9_]')
        graph.add_edge('q2', 'reject', label='^[^"]')
        return graph


graph_creator = DFAGraphCreator(ReservedDataType())
graph = graph_creator.create_graph('integer')
graph.g.render('datatype.gv', view=True, cleanup=True)

graph_creator = DFAGraphCreator(integer())
graph = graph_creator.create_graph('integer')
graph.g.render('integer.gv', view=True, cleanup=True)

graph_creator = DFAGraphCreator(real())
graph = graph_creator.create_graph('real')
graph.g.render('real.gv', view=True, cleanup=True)

graph_creator = DFAGraphCreator(Name())
graph = graph_creator.create_graph('Name')
graph.g.render('Name.gv', view=True, cleanup=True)

graph_creator = DFAGraphCreator(Anonymous())
graph = graph_creator.create_graph('Anonymous')
graph.g.render('Anonymous.gv', view=True, cleanup=True)

graph_creator = DFAGraphCreator(VariableName())
graph = graph_creator.create_graph('VariableName')
graph.g.render('VariableName.gv', view=True, cleanup=True)

graph_creator = DFAGraphCreator(String())
graph = graph_creator.create_graph('String')
graph.g.render('String.gv', view=True, cleanup=True)

graph_creator = DFAGraphCreator(Char())
graph = graph_creator.create_graph('Char')
graph.g.render('Char.gv', view=True, cleanup=True)
