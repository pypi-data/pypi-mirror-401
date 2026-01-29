ERROR_RULES = {

    
    "TypeError": {
        "explanation": "You used incompatible data types together.",
        "fix": "Check variable types or convert them using int(), str(), float(), etc.",
        "example": "int('5') + 10"
    },

    "ValueError": {
        "explanation": "The value is of correct type but has an invalid value.",
        "fix": "Check user input or function arguments.",
        "example": "int('123')"
    },

    
    "IndexError": {
        "explanation": "You tried to access a list or tuple index that does not exist.",
        "fix": "Check the length of the list before accessing.",
        "example": "if i < len(my_list): print(my_list[i])"
    },

    "KeyError": {
        "explanation": "You tried to access a dictionary key that does not exist.",
        "fix": "Use dict.get() or check if key exists.",
        "example": "my_dict.get('key')"
    },

    
    "NameError": {
        "explanation": "You used a variable or function name that is not defined.",
        "fix": "Check spelling or define the variable before use.",
        "example": "x = 10"
    },

    "AttributeError": {
        "explanation": "The object does not have the attribute or method you tried to use.",
        "fix": "Check object type or available attributes.",
        "example": "'hello'.upper()"
    },

   
    "ImportError": {
        "explanation": "Python could not import the module or object.",
        "fix": "Check module name or install missing package.",
        "example": "pip install package_name"
    },

    "ModuleNotFoundError": {
        "explanation": "The module you are trying to import does not exist.",
        "fix": "Install the module or check spelling.",
        "example": "pip install requests"
    },

   
    "FileNotFoundError": {
        "explanation": "The file you are trying to access does not exist.",
        "fix": "Check file path or working directory.",
        "example": "open('data.txt')"
    },

    "PermissionError": {
        "explanation": "You do not have permission to access this file or resource.",
        "fix": "Change file permissions or run with correct access.",
        "example": "chmod +r file.txt"
    },

    "IsADirectoryError": {
        "explanation": "You tried to open a directory as a file.",
        "fix": "Use correct file path instead of directory.",
        "example": "open('file.txt')"
    },

   
    "ZeroDivisionError": {
        "explanation": "You tried to divide a number by zero.",
        "fix": "Ensure denominator is not zero.",
        "example": "if b != 0: a / b"
    },

    "OverflowError": {
        "explanation": "The calculation result is too large to be represented.",
        "fix": "Use smaller numbers or optimized logic.",
        "example": "math.exp(10)"
    },

   
    "AssertionError": {
        "explanation": "An assert condition failed.",
        "fix": "Check the logic of your assert statement.",
        "example": "assert x > 0"
    },

   
    "SyntaxError": {
        "explanation": "Your Python code syntax is invalid.",
        "fix": "Check missing colons, brackets, or quotes.",
        "example": "if x > 5:"
    },

    "IndentationError": {
        "explanation": "Your code indentation is incorrect.",
        "fix": "Ensure consistent indentation (spaces or tabs).",
        "example": "use 4 spaces per block"
    },

    "TabError": {
        "explanation": "You mixed tabs and spaces in indentation.",
        "fix": "Use only spaces or only tabs consistently.",
        "example": "convert tabs to spaces"
    },

   
    "UnicodeDecodeError": {
        "explanation": "Python failed to decode a byte sequence into text.",
        "fix": "Specify correct encoding like utf-8.",
        "example": "open('file.txt', encoding='utf-8')"
    },

    "UnicodeEncodeError": {
        "explanation": "Python failed to encode text into bytes.",
        "fix": "Ensure characters are supported by encoding.",
        "example": "text.encode('utf-8')"
    },

   
    "MemoryError": {
        "explanation": "The program ran out of memory.",
        "fix": "Optimize data usage or process in chunks.",
        "example": "use generators instead of lists"
    },

    "RecursionError": {
        "explanation": "Function exceeded maximum recursion depth.",
        "fix": "Add a base condition or reduce recursion.",
        "example": "if n == 0: return"
    },

    
    "TimeoutError": {
        "explanation": "The operation took too long to complete.",
        "fix": "Optimize code or increase timeout.",
        "example": "set timeout parameter"
    },

    "RuntimeError": {
        "explanation": "A generic runtime error occurred.",
        "fix": "Check logic or unexpected conditions.",
        "example": "review stack trace"
    }
}