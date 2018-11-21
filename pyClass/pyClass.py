import os
import re


class Class:
    """
    This class assumes that we only have one single class
    in the file(filename) passed to the constructor
    """

    def __init__(self, filename):
        self.filename = filename
        self.exists = os.path.exists(self.filename)
        self.file_as_list = None
        self.file_as_string = None
        self.classes_contained = None
        self.functions_contained = None
        self.__function_set = None
        self.__property_set = None

    def read_as_list(self):
        if self.exists:
            with open(self.filename, 'r') as fp:
                self.file_as_list = fp.readlines()
        else:
            self.file_as_list = []

    def get_as_list(self):
        if self.file_as_list is None:
            self.read_as_list()
        return self.file_as_list

    def get_num_lines_in_file(self):
        if self.file_as_list is None:
            self.read_as_list()
        return len(self.file_as_list)

    def read_as_string(self):
        if self.exists:
            with open(self.filename, 'r') as fp:
                self.file_as_string = fp.read()
        else:
            self.file_as_string = ''

    def get_attributes(self, attrStr):
        return (attrStr.replace(' ', '')
                .replace("\n", '')
                .split(','))

    def get_classes(self, force=False):
        CLASS = 'class ([\w]+)\(?([\w,\s]*)\)?:'
        all_class_names = []
        if self.file_as_string is None:
            self.read_as_string()
        if self.classes_contained is None or force:
            self.classes_contained = []
            for match in re.finditer(CLASS, self.file_as_string):
                class_sig_dict = dict()
                class_sig_dict["name"] = match.group(1)
                class_sig_dict["extends"] = self.get_attributes(match.group(2))
                self.classes_contained.append(class_sig_dict)
            # Assuming there is only one class in the file
            if len(self.classes_contained) != 1:
                print(
                    "Error: There are two classes in a single file. Please update the code. Please contact Pranav Kanade.")
                print("Ommiting collection of functions")
            else:
                self.classes_contained[0]["methods"] = self.get_functions(
                    force)
                self.classes_contained[0]["properties"] = self.get_properties(
                    force)
        return self.classes_contained

    def get_functions(self, force=False):
        """
        NOTE: For now assuming that every file has only one class.
        TODO: Modify this for n number of classes in single file
        """
        self.__function_set = set()
        FUNC = "def ([\w]+)\(?([\w,\s]*)\)?:"
        if self.file_as_string is None:
            self.read_as_string()
        if self.functions_contained is None or force:
            self.functions_contained = []
            for match in re.finditer(FUNC, self.file_as_string):
                func_sig_dict = dict()
                func_sig_dict["name"] = match.group(1)
                self.__function_set.add(match.group(1))
                func_sig_dict["param"] = self.get_attributes(match.group(2))
                self.functions_contained.append(func_sig_dict)
        return self.functions_contained

    def get_properties(self, force=False):
        if self.__property_set is None or force:
            self.__property_set = set()
            if self.functions_contained is None:
                self.get_functions(True)
            PROP = "(self\.[\w]+)"
            for match in re.finditer(PROP, self.file_as_string):
                self.__property_set.add(match.group(1))
        self.__property_set = self.__property_set.difference(
            self.__function_set)
        return list(self.__property_set)

    # TODO: Add function to get the imports
    # TODO: Find a way to represent coupling between two classes
    # TODO: Find the Coupling between current and imported classes
