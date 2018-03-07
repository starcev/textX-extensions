from os.path import join, dirname
from textx.metamodel import metamodel_from_file
from jinja2 import Template

class ColoringVSCode(object):

    def __init__(self, configuration):
        self.configuration = configuration
        self.textxRulesInProgram = {}
        self.keywords = []
        self.operations = []
        self.rule_keyword_relation = []
        self.rule_operation_relation = []
        self.special_characters = ['+','*','?','|','.','(',')','$','[',']','\\','^']
        self.additional_characters = ['<', '>', '=', '+', '-', '*', '/', '|', '&', '(', ')', '~', '!', '@', '#', '$', '[', ']', '{', '}', ',', '.', ';', ':', '?', '%', '\\', '^']
        self.default_keyword_type = None
        self.default_operation_type = None
        self.line_comment = None
        self.block_comment_start = None
        self.block_comment_end = None
        self.rules_keyword_type_relation = {}
        self.rules_operation_type_relation = {}
        self.matches_word_type_relation = {}
        self.regular_expressions = {}

        self.keyword_type_relation = {}
        self.operation_type_relation = {}
        self.regular_expression_type_relation = {}
        self.type_keyword_relation = {}
        self.type_operation_relation = {}
        self.type_regular_expression_relation = {}

        self.coloring = {}

    def do_coloring_for_vscode(self):
        if self.configuration.coloring_path == None:
            return

        this_folder = dirname(__file__)

        textX = metamodel_from_file(join(dirname(__file__), '..', 'textX.tx'))

        grammar_model = textX.model_from_file(join(this_folder, self.configuration.grammar_path))
        grammar = metamodel_from_file(join(this_folder, 'coloring.tx'), debug=False)

        program_model = grammar.model_from_file(join(this_folder, self.configuration.coloring_path))

        self.name = self.configuration.language_name

        self.interpret_grammar(grammar_model)
        self.interpret_program(program_model)
        self.prepare_data()
        self.generate_code()

    def interpret_program(self,model):
        if model.configuration != None:
            self.interpret_configuration(model.configuration)
        for element in model.array:
            if element.rules != None:
                self.intepret_rules(element.rules)
            if element.matches != None:
                self.interpret_matches(element.matches)
            if element.regular_expressions != None:
                self.interpret_regular_expressions(element.regular_expressions)

    def interpret_configuration(self,configuration):
        for command in configuration.configuration_commands:
            if command.default != None:
                self.interpret_default(command.default)
            if command.coment != None:
                self.interpret_comment(command.coment)

    def interpret_default(self,default):
        for option in default.default_options:
            if option.default_keyword_option != None:
                self.default_keyword_type = option.default_keyword_option.type
            if option.default_operation != None:
                self.default_operation_type = option.default_operation.type

    def interpret_comment(self,comment):
        for option in comment.comment_options:
            if option.line != None:
                self.line_comment = self.add_slash_infront_of_special_characters(option.line.id)
            if option.block != None:
                self.block_comment_start = self.add_slash_infront_of_special_characters(option.block.start)
                self.block_comment_end = self.add_slash_infront_of_special_characters(option.block.end)

    def intepret_rules(self,rules):
        for option in rules.rule_options:
            if option.rule_keyword != None:
                for list in option.rule_keyword.rule_lists:
                    for element in list.elements:
                        self.rules_keyword_type_relation[element] = list.type
            if option.rule_operation != None:
                for list in option.rule_operation.rule_lists:
                    for element in list.elements:
                        self.rules_operation_type_relation[element] = list.type

    def interpret_matches(self, matches):
        for list in matches.match_list:
            for word in list.words:
                self.matches_word_type_relation[self.add_slash_infront_of_special_characters(word)] = list.type

    def interpret_regular_expressions(self,regular_expressions):
        for list in regular_expressions.regular_expression_list:
            for expression in list.expression:
                self.regular_expressions[expression] = list.type

    def interpret_grammar(self, model):
        for rule in model.rules:
            self.interpret_sequences(rule.body.sequences,rule.name)

    def interpret_sequences(self,sequences,rule_name):
        for sequence in sequences:
            for expression in sequence.repeatable_expr:
                if expression.expr.simple_match != None and expression.expr.simple_match.str_match != None:
                    self.append_word(rule_name, expression.expr.simple_match.str_match.match)
                if expression.expr.assigment != None and expression.expr.assigment.rhs != None:
                    if expression.expr.assigment.rhs.simple != None and expression.expr.assigment.rhs.simple.str_match != None:
                        self.append_word(rule_name, expression.expr.assigment.rhs.simple.str_match.match)
                    if expression.expr.assigment.rhs.modifiers != None \
                        and expression.expr.assigment.rhs.modifiers.str_match != None:
                        self.append_word(rule_name, expression.expr.assigment.rhs.modifiers.str_match.match)
                if expression.operator != None and expression.operator.modifiers != None \
                        and expression.operator.modifiers.str_match != None:
                    self.append_word(rule_name, expression.operator.modifiers.str_match.match)
                if expression.expr.bracketed_choice != None:
                    self.interpret_sequences(expression.expr.bracketed_choice.choice.sequences, rule_name)

    def append_word(self, rule_name, word):
        if self.is_word_assembled_from_additional_characters(word):
            word = self.add_slash_infront_of_special_characters(word)
            if word not in self.operations:
                self.operations.append(word)
            operation = {'rule': rule_name, 'operation': word}
            self.rule_operation_relation.append(operation)
        else:
            word = self.add_slash_infront_of_special_characters(word)
            if word not in self.keywords:
                self.keywords.append(word)
            keyword = {'rule': rule_name, 'keyword': word}
            self.rule_keyword_relation.append(keyword)

    def is_word_assembled_from_additional_characters(self,word):
        for character in word:
            if character not in self.additional_characters:
                return False
        return True

    def add_slash_infront_of_special_characters(self, word):
        retVal = ""
        for  i, character in enumerate(word):
            if character not in self.special_characters:
                retVal += character
            else:
                retVal += '\\\\'
                retVal += character
        return retVal

    def prepare_data(self):
        self.prepare_relation_keywords()
        self.prepare_relation_operations()
        self.prepare_types()
        self.prepare_coloring_json()

    def prepare_relation_keywords(self):
        for item in self.matches_word_type_relation:
            if item not in self.keywords and self.is_word_assembled_from_additional_characters(item) == False:
                self.keywords.append(item)
        for item in self.keywords:
            self.type = self.get_type_from_keywords(item)
            if item not in self.keyword_type_relation and self.type != None:
                self.keyword_type_relation[item] = self.type
                continue
            self.type = self.get_type_from_rules_keyword(item)
            if self.type != None:
                self.keyword_type_relation[item] = self.type
                continue
            if self.default_keyword_type != None:
                self.keyword_type_relation[item] = self.default_keyword_type

    def prepare_relation_operations(self):
        for item in self.matches_word_type_relation:
            if item not in self.operations and self.is_word_assembled_from_additional_characters(item):
                self.operations.append(item)
        for item in self.operations:
            self.type = self.get_type_from_keywords(item)
            if item not in self.operation_type_relation and self.type != None:
                self.operation_type_relation[item] = self.type
                continue
            self.type = self.get_type_from_rules_operation(item)
            if self.type != None:
                self.operation_type_relation[item] = self.type
                continue
            if self.default_operation_type != None:
                self.operation_type_relation[item] = self.default_operation_type


    def get_type_from_keywords(self, word):
        self.type = None
        for item in self.matches_word_type_relation:
            if item == word:
                self.type = self.matches_word_type_relation.get(item)
        if self.type != None:
            return self.type
        for item in self.keyword_type_relation:
            if item ==  word:
                self.type = self.keyword_type_relation.get(item)
        return self.type

    def get_type_from_rules_keyword(self, word):
        self.type = None
        for item in self.rule_keyword_relation:
            if item['keyword'] == word:
                for relation in self.rules_keyword_type_relation:
                    if relation == item['rule']:
                        self.type = self.rules_keyword_type_relation[relation]
        return self.type

    def get_type_from_rules_operation(self, word):
        self.type = None
        for item in self.rule_operation_relation:
            if item['operation'] == word:
                for relation in self.rules_operation_type_relation:
                    if relation == item['rule']:
                        self.type = self.rules_operation_type_relation[relation]
        return self.type

    def prepare_types(self):
        for item in self.keyword_type_relation:
            if self.keyword_type_relation[item] not in self.type_keyword_relation:
                self.type_keyword_relation[self.keyword_type_relation[item]] = []
            if item != "'" and item != '"' and self.is_word_assembled_from_additional_characters(item) == False:
                self.type_keyword_relation[self.keyword_type_relation[item]].append(item)
            elif item != "'" and item != '"':
                self.type_keyword_relation[self.keyword_type_relation[item]].append(item)
        for item in self.operation_type_relation:
            if self.operation_type_relation[item] not in self.type_operation_relation:
                self.type_operation_relation[self.operation_type_relation[item]] = []
            self.type_operation_relation[self.operation_type_relation[item]].append(item)
        for item in self.regular_expressions:
            if self.regular_expressions[item] not in self.type_regular_expression_relation:
                self.type_regular_expression_relation[self.regular_expressions[item]] = []
            self.type_regular_expression_relation[self.regular_expressions[item]].append(item)
            self.type_regular_expression_relation[self.regular_expressions[item]].append(item)

    def prepare_coloring_json(self):
        self.coloring = {
            'name': self.configuration.language_name,
            'extensions': self.configuration.language_extensions_string,
            'comment': {
                'line': self.line_comment,
                'block_start': self.block_comment_start,
                'block_end': self.block_comment_end
            },
            'keywords': self.get_name_match_relation(self.type_keyword_relation, True),
            'operations': self.get_name_match_relation(self.type_operation_relation),
            'regular_expressions':  self.get_name_match_relation(self.type_regular_expression_relation)
        }

    def get_name_match_relation(self, map, word_boundary=False):
        keywords = []
        deleted = True
        while deleted == True:
            deleted = False
            for item, words in map.items():
                element = ""
                #element += '('
                j = 0
                insert = False
                while j < len(words):
                    if j >= len(words):
                        break
                    indipendent = self.isWordIndipendent(words[j], item, map)
                    if indipendent == False:
                        j = j + 1
                        continue
                    string = ""
                    if word_boundary:
                        string += "\\\\b"
                    string += words[j]
                    if word_boundary:
                        string += "\\\\b"
                    #if appendix != "":
                        #string += "\\b" + appendix + "\\b"
                        #string = string + "$|" + string + " "
                    element += string
                    if j != len(words)-1:
                        element += '|'
                    words.remove(words[j])
                    deleted = True
                    insert = True
                #element += ')'
                keyword = {
                    'name': item,
                    'match': element
                }
                if insert:
                    keywords.append(keyword)
        return keywords

    def isWordIndipendent(self, word, type, map):
        for key, value in map.items():
            for item in value:
                if key != type and word in item:
                    return False
        return True

    def generate_code(self):
        this_folder = dirname(__file__)
        with open(join(this_folder, 'templates', 'language.json.template'), 'r') as file:
            data = file.read()
        template = Template(data)
        result = template.render(self.coloring)
        result_file = open(join(self.configuration.project_path, 'coloring', self.name+'.tmLanguage.json'), 'w')
        result_file.write(result)