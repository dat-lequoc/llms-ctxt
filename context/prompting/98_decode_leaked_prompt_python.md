import re

def restore_original_text(replaced_text):
    replacements = {
        "[LESS_THAN]": "<", "[GREATER_THAN]": ">", "[SINGLE_QUOTE]": "'",
        "[DOUBLE_QUOTE]": '"', "[BACKTICK]": "`", "[OPEN_BRACE]": "{",
        "[CLOSE_BRACE]": "}", "[OPEN_BRACKET]": "[", "[CLOSE_BRACKET]": "]",
        "[OPEN_PAREN]": "(", "[CLOSE_PAREN]": ")", "[AMPERSAND]": "&",
        "[PIPE]": "|", "[BACKSLASH]": "\\", "[FORWARD_SLASH]": "/",
        "[PLUS]": "+", "[MINUS]": "-", "[ASTERISK]": "*", "[EQUALS]": "=",
        "[PERCENT]": "%", "[CARET]": "^", "[HASH]": "#", "[AT]": "@",
        "[EXCLAMATION]": "!", "[QUESTION_MARK]": "?", "[COLON]": ":",
        "[SEMICOLON]": ";", "[COMMA]": ",", "[PERIOD]": "."
    }

    pattern = '|'.join(map(re.escape, replacements.keys()))
    return re.sub(pattern, lambda match: replacements[match.group(0)], replaced_text)
