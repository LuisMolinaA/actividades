import re

# Definición de tokens
TOKENS = {
    'NUMBER': r'(?<![\d.])-?\d+(\.\d*)?',  # Reconoce números negativos si no están precedidos por otro dígito o punto decimal
    'PLUS': r'\+',
    'MINUS': r'(?<!^)(?<![LPAREN])-',  # Reconoce el signo menos como operador, no como parte de un número, si no es al inicio o después de un paréntesis de apertura
    'MULTIPLY': r'\*',
    'DIVIDE': r'/',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
}

# Definir la precedencia de los operadores
PRECEDENCE = {
    'PLUS': 1,
    'MINUS': 1,
    'MULTIPLY': 2,
    'DIVIDE': 2,
}

# Función para convertir la expresión a RPN (Notación Polaca Inversa)
def infix_to_rpn(tokens):
    output_queue = []
    operator_stack = []

    for token in tokens:
        token_type, token_value = token
        if token_type == 'NUMBER':
            output_queue.append(token_value)
        elif token_type in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'):
            while (operator_stack and operator_stack[-1][0] != 'LPAREN' and
                   PRECEDENCE[operator_stack[-1][0]] >= PRECEDENCE[token_type]):
                output_queue.append(operator_stack.pop()[1])
            operator_stack.append(token)
        elif token_type == 'LPAREN':
            operator_stack.append(token)
        elif token_type == 'RPAREN':
            while operator_stack and operator_stack[-1][0] != 'LPAREN':
                output_queue.append(operator_stack.pop()[1])
            if operator_stack and operator_stack[-1][0] == 'LPAREN':
                operator_stack.pop()  # Pop the 'LPAREN' off the stack, but don't add to output.

    # Pop all the operators left in the stack
    while operator_stack:
        output_queue.append(operator_stack.pop()[1])

    return output_queue

# Función para evaluar la RPN
def evaluate_rpn(rpn_tokens):
    stack = []
    
    for token in rpn_tokens:
        if re.match(TOKENS['NUMBER'], token):
            stack.append(float(token))
        else:
            right_operand = stack.pop()
            left_operand = stack.pop()
            if token == '+':
                stack.append(left_operand + right_operand)
            elif token == '-':
                stack.append(left_operand - right_operand)
            elif token == '*':
                stack.append(left_operand * right_operand)
            elif token == '/':
                stack.append(left_operand / right_operand)
    
    return stack[0]
def check_parentheses(tokens):
    balance = 0
    for token in tokens:
        if token[0] == 'LPAREN':
            balance += 1
        elif token[0] == 'RPAREN':
            balance -= 1
            if balance < 0:
                return False  # Más paréntesis de cierre que de apertura
    return balance == 0  # Debe ser cero para estar balanceado
# Función para procesar la expresión y devolver el resultado
def calculate_expression(expression):
    tokens = list(lex(expression))
    if not check_parentheses(tokens):
        raise ValueError("Unbalanced parentheses")
    rpn_tokens = infix_to_rpn(tokens)
    result = evaluate_rpn(rpn_tokens)
    return {
        'result': result,
        'original_tokens': [(t[0], t[1]) for t in tokens],  # Lista de tokens originales
        'rpn_tokens': rpn_tokens  # Tokens en formato RPN
    }

token_re = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS.items())

def lex(expression):
    for match in re.finditer(token_re, expression):
        token_type = match.lastgroup
        token_value = match.group()
        yield (token_type, token_value)


