from dataclasses import dataclass
from typing import Tuple

from pyobscenity.util import is_high_surrogate, is_low_surrogate

@dataclass
class LiteralNode:
    chars: list[int]
    """The literal string value of this node."""

@dataclass
class WildcardNode:
    """A node that matches any pattern."""
    pass

@dataclass
class OptionalNode:
    """The node contained within the optional expression."""
    child_node: LiteralNode | WildcardNode

class BoundaryAssertionNode:
    """A node that asserts a word boundary."""
    pass

type Node = LiteralNode | OptionalNode | WildcardNode | BoundaryAssertionNode

@dataclass
class ParsedPattern:
    nodes: list[Node]
    """The list of nodes that make up the parsed pattern."""
    require_word_boundary_at_start: bool
    """Whether a word boundary is required at the start of the pattern."""
    require_word_boundary_at_end: bool
    """Whether a word boundary is required at the end of the pattern."""

    def potentially_matches_empty_string(self) -> bool:
        '''
        Determines if the pattern can match an empty string (i.e., all nodes are optional).
        :return: True if the pattern can match an empty string, False otherwise.
        '''
        return all(isinstance(node, OptionalNode) for node in self.nodes)
    
    def as_regex(self) -> str:
        '''
        Converts the parsed pattern into a regular expression string.
        :return: The regular expression string representing the pattern.
        '''
        regex_parts = []

        if self.require_word_boundary_at_start and len(self.nodes) > 0 and not isinstance(self.nodes[0], BoundaryAssertionNode):
            regex_parts.append(r'\b')

        for node in self.nodes:
            if isinstance(node, LiteralNode):
                escaped_chars = ''.join(f'\\x{char:02x}' for char in node.chars)
                regex_parts.append(escaped_chars)
            elif isinstance(node, WildcardNode):
                regex_parts.append(r'.')
            elif isinstance(node, OptionalNode):
                if isinstance(node.child_node, LiteralNode):
                    escaped_chars = ''.join(f'\\x{char:02x}' for char in node.child_node.chars)
                    regex_parts.append(f'(?:{escaped_chars})?')
                elif isinstance(node.child_node, WildcardNode):
                    regex_parts.append(r'(?:.)?')
            elif isinstance(node, BoundaryAssertionNode):
                regex_parts.append(r'\b')

        if self.require_word_boundary_at_end and len(self.nodes) > 0 and not isinstance(self.nodes[-1], BoundaryAssertionNode):
            regex_parts.append(r'\b')

        return ''.join(regex_parts)

supports_escaping = "\\[]?|"

class PatternParser:
    '''
    Parser for obscenity patterns.
    '''

    def __init__(self):
        self.input = ''
        self.line = 1
        self.column = 1
        self.position = 0
        self.lastColumn = 1
        self.lastWidth = 0

    def parse_pattern(self, pattern: str) -> ParsedPattern:
        '''
        Parses the given pattern string into a ParsedPattern object.
        :param pattern: The pattern string to be parsed.
        :return: A ParsedPattern object representing the parsed pattern.
        '''
        self.done = False
        self._set_input(pattern)
        nodes = []
        first_node = self._next_node()
        require_word_boundary_at_start = isinstance(first_node, BoundaryAssertionNode)
        if first_node is not None:
            nodes.append(first_node)

        require_word_boundary_at_end = False

        while True:
            node = self._next_node()

            if node is None:
                # End of input reached; stop parsing
                break

            # Update self.done to reflect whether we've consumed the final char.
            self.done = self._peek() is None

            nodes.append(node)

            # Handle boundary assertion: it is only valid at the very end. If it's
            # found with more input after it, that's an error.
            if isinstance(node, BoundaryAssertionNode):
                if not self.done:
                    raise ValueError(f"Unexpected word boundary assertion at line {self.line}, column {self.column}")
                require_word_boundary_at_end = True

        return ParsedPattern(
            nodes=nodes,
            require_word_boundary_at_start=require_word_boundary_at_start,
            require_word_boundary_at_end=require_word_boundary_at_end
        )

    def _set_input(self, input: str):
        '''
        Sets the input pattern string for parsing.
        :param input: The input pattern string.
        '''
        self.input = input
        self.line = 1
        self.column = 1
        self.position = 0
        self.lastColumn = 1
        self.lastWidth = 0
        self.done = len(input) == 0

    def _next_node(self) -> Node | None:
        '''
        Parses the next node from the input pattern string.
        :return: The next Node object, or None if the end of input is reached.
        '''
        next = self._peek()

        if next is None:
            self.done = True
            return None
        elif next == '[':
            return self._parse_optional()
        elif next == ']':
            raise ValueError(f"Unmatched closing bracket at line {self.line}, column {self.column}")
        elif next == '?':
            return self._parse_wildcard()
        elif next == '|':
            return self._parse_boundary_assertion()
        else:
            return self._parse_literal()
        
    def _parse_optional(self) -> OptionalNode:
        pre_open_pos = self._mark()
        self._next()  # consume '['
        post_open_pos = self._mark()

        if self.done:
            raise ValueError(f"Unterminated optional at line {self.line}, column {self.column}")
        if self._accept('['):
            raise ValueError(f"Nested optionals are not allowed at line {self.line}, column {self.column}")
        
        child_node = self._next_node()

        if isinstance(child_node, BoundaryAssertionNode):
            raise ValueError(f"Boundary assertions are not allowed inside optionals at line {self.line}, column {self.column}")
        
        if not self._accept(']'):
            raise ValueError(f"Unterminated optional at line {self.line}, column {self.column}")
        
        return OptionalNode(child_node=child_node)
    
    def _parse_wildcard(self) -> WildcardNode:
        self._next()  # consume '?'
        return WildcardNode()
    
    def _parse_boundary_assertion(self) -> BoundaryAssertionNode:
        self._next()  # consume '|'
        return BoundaryAssertionNode()
    
    def _parse_literal(self) -> LiteralNode:
        chars = []
        while not self.done:
            if self._accept('[]?|'):
                self._backup()
                break

            next_char = self._next()
            if next_char is None:
                break

            if next_char == '\\':
                if self.done:
                    self._backup()
                    raise ValueError(f"Trailing backslash at line {self.line}, column {self.column}")
                escaped_char = self._next()
                if escaped_char and escaped_char not in supports_escaping:
                    self._backup()
                    raise ValueError(f"Invalid escape sequence '\\{escaped_char}' at line {self.line}, column {self.column}")
                
                if escaped_char is not None:
                    chars.append(ord(escaped_char))
            else:
                chars.append(ord(next_char))
        return LiteralNode(chars=chars)
    
    def _peek(self) -> str | None:
        '''
        Peeks at the next character in the input without consuming it.
        :return: The next character, or None if at the end of input.
        '''
        if self.position >= len(self.input):
            return None
        return self.input[self.position]
    
    def _mark(self) -> Tuple[int, int]:
        '''
        Marks the current position in the input.
        :return: The current position index.
        '''
        return self.line, self.column
    
    def _accept(self, chars: str) -> bool:
        '''
        Accepts the next character if it is in the given set of characters.
        :param chars: A string of characters to accept.
        :return: True if a character was accepted, False otherwise.
        '''
        next_char = self._peek()
        if next_char is not None and next_char in chars:
            self._next()
            return True
        return False
    
    def _next(self) -> str | None:
        if self.position >= len(self.input):
            self.done = True
            return None
        
        char = self.input[self.position]
        self.position += 1
        # Reset the last width, which is used to track extra width for surrogate pairs.
        self.lastWidth = 0
        
        if char == '\n':
            self.line += 1
            self.lastColumn = self.column
            self.column = 1
            return char

        self.lastColumn = self.column
        self.column += 1

        # If current char is a high surrogate and there's another code unit available,
        # see if it's a low surrogate and combine them.
        if is_high_surrogate(char) and not self.done and self.position < len(self.input):
            next_ch = self.input[self.position]
            next_cp = ord(next_ch)
            if is_low_surrogate(next_ch):
                # consume the low surrogate
                self.position += 1
                # record extra width consumed by the surrogate pair (beyond the 1 we
                # already advanced the column by)
                self.lastWidth += 1
                # Convert the surrogate pair into a single Unicode code point.
                high_val = ord(char)
                low_val = next_cp
                code_point = 0x10000 + ((high_val - 0xD800) << 10) + (low_val - 0xDC00)
                return chr(code_point)

        return char
    
    def _backup(self):
        '''
        Backs up one character in the input.
        '''
        if self.position == 0:
            return

        # Step back one code unit plus any extra width that was consumed for
        # combined surrogate pairs. `lastWidth` stores the extra width beyond
        # the 1 normally consumed by `next()`.
        step_back = 1 + self.lastWidth
        self.position -= step_back
        self.column = self.lastColumn

        # If we've backed up over a newline, adjust the line counter.
        if self.input[self.position] == '\n':
            self.line -= 1
