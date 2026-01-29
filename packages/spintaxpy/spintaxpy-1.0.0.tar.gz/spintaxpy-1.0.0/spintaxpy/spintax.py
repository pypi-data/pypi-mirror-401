"""
Spintax - Combinatorial String Generator

A library for generating all possible combinations of template strings
with variable elements.
"""

import re
import random
from typing import Iterator, List, Any, Tuple, Union, Callable
from itertools import product

# Store reference to built-in range before we override it
builtins_range = range


class Generator:
    """Base class for all generators"""
    
    def values(self) -> Iterator[Any]:
        """Returns an iterable of all possible values"""
        raise NotImplementedError("Method not implemented")
    
    def __iter__(self):
        return self.values()


class ChoicesGenerator(Generator):
    """Generator for choices between multiple string or number options"""
    
    def __init__(self, options: List[Union[str, int, float]]):
        """
        Args:
            options: The choices to select from
        
        Example:
            ChoicesGenerator(['red', 'green', 'blue'])
        """
        self.options = options
    
    def values(self) -> Iterator[Union[str, int, float]]:
        """Returns all possible values for this choice"""
        for option in self.options:
            yield option


class RangeGenerator(Generator):
    """Generator for numerical ranges"""
    
    def __init__(self, start: float, end: float, step: float = 1, include_end: bool = True):
        """
        Args:
            start: Starting value (inclusive)
            end: Ending value (inclusive)
            step: Increment between values
            include_end: Always include the end value even if not divisible by step
        
        Example:
            RangeGenerator(1, 10, 2)  # 1, 3, 5, 7, 9
            RangeGenerator(1, 10, 3, True)  # 1, 4, 7, 10
        """
        self.start = start
        self.end = end
        self.step = step
        self.include_end = include_end
    
    def values(self) -> Iterator[Union[int, float]]:
        """Returns all values in this range"""
        i = self.start
        last_yielded = None
        while i <= self.end:
            # Yield as int if it's a whole number, otherwise as float
            value = int(i) if i == int(i) else i
            yield value
            last_yielded = i
            i += self.step
        
        # If include_end is True and the last value wasn't included due to step,
        # include the end value explicitly
        if (self.include_end and 
            last_yielded is not None and
            last_yielded < self.end):
            value = int(self.end) if self.end == int(self.end) else self.end
            yield value


class StaticGenerator:
    """Represents a non-generator placeholder for static values"""
    
    def __init__(self, value: Any):
        """
        Args:
            value: The static value
        """
        self.value = value
    
    def values(self) -> Iterator[Any]:
        """Returns the static value"""
        yield self.value


def cartesian_product(generators: List[Any]) -> Iterator[List[Any]]:
    """
    Creates a cartesian product of all provided generators
    
    Args:
        generators: List of generators to combine (can be Generator objects or lists)
    
    Returns:
        Generator of all combinations
    """
    if len(generators) == 0:
        yield []
        return
    
    # Helper to get values from either a generator or a list
    def get_values(gen):
        if isinstance(gen, (list, tuple)):
            return gen
        elif hasattr(gen, 'values'):
            return list(gen.values())
        else:
            return list(gen)
    
    if len(generators) == 1:
        for value in get_values(generators[0]):
            yield [value]
        return
    
    # Collect all values from each generator
    all_values = [get_values(gen) for gen in generators]
    
    # Generate all combinations
    for combination in product(*all_values):
        yield list(combination)


def range(start: float, end: float, step: float = 1, include_end: bool = True) -> RangeGenerator:
    """
    Creates a generator that yields numbers within a specified range
    
    Args:
        start: Starting value (inclusive)
        end: Ending value (inclusive)
        step: Increment between values
        include_end: Always include the end value even if not divisible by step
    
    Returns:
        RangeGenerator instance
    
    Example:
        range(1, 5, 1)  # yields 1, 2, 3, 4, 5
        range(0, 10, 3, True)  # yields 0, 3, 6, 9, 10 (note 10 is included)
    """
    return RangeGenerator(start, end, step, include_end)


def is_range_pattern(pattern: str, separator: str = ",") -> bool:
    """
    Determines if a pattern contains only numeric values and commas (a range pattern)
    
    Args:
        pattern: The pattern to check
        separator: The separator character
    
    Returns:
        True if the pattern is a range pattern, false otherwise
    """
    # Remove all whitespace for checking
    no_whitespace = re.sub(r'\s+', '', pattern)
    
    # Remove trailing commas if present
    separator_pattern = re.escape(separator) + r'+$'
    trimmed_pattern = re.sub(separator_pattern, '', no_whitespace)
    
    # Must have at least one comma to be a range
    if separator not in trimmed_pattern:
        return False
    
    # Split by commas and check each part is a valid number
    parts = trimmed_pattern.split(separator)
    
    # Range patterns must have 2 or 3 parts
    if len(parts) < 2 or len(parts) > 3:
        return False
    
    # Each part must be a valid number
    for part in parts:
        # Empty parts (from multiple commas) are not valid
        if part == "":
            return False
        # Check if it's a valid number
        try:
            float(part)
        except ValueError:
            return False
    
    return True


def parse_range_pattern(pattern: str, separator: str = ",") -> Tuple[float, float, float]:
    """
    Parses a range pattern into start, end, and optional step values
    
    Args:
        pattern: The range pattern to parse
        separator: The separator character
    
    Returns:
        Tuple with (start, end, step)
    """
    # Remove all whitespace
    no_whitespace = re.sub(r'\s+', '', pattern)
    
    # Remove trailing commas
    separator_pattern = re.escape(separator) + r'+$'
    trimmed_pattern = re.sub(separator_pattern, '', no_whitespace)
    
    # Split by comma and convert to numbers
    parts = [float(part) for part in trimmed_pattern.split(separator)]
    
    start = parts[0]
    end = parts[1]
    step = parts[2] if len(parts) > 2 else 1
    
    return start, end, step


def parse_choices_pattern(pattern: str, separator: str = "|") -> List[str]:
    """
    Parses a choices pattern, preserving whitespace in the options
    
    Args:
        pattern: The choices pattern to parse
        separator: The separator character
    
    Returns:
        List of choice options
    """
    # Split by the separator, preserving whitespace
    return pattern.split(separator)


def sub_helper(template: str, pattern_start: str = "{", pattern_end: str = "}") -> dict:
    """
    Shared helper for parse and count functions
    Extracts patterns from the template string
    
    Args:
        template: The template string
        pattern_start: Pattern start delimiter
        pattern_end: Pattern end delimiter
    
    Returns:
        Dictionary containing patterns and string parts
    """
    # Find all {...} patterns
    patterns = []
    pattern_regex = re.compile(
        re.escape(pattern_start) + r'([^' + re.escape(pattern_end) + r']+)' + re.escape(pattern_end)
    )
    string_parts = []
    last_index = 0
    
    for match in pattern_regex.finditer(template):
        # Add the text before the pattern
        string_parts.append(template[last_index:match.start()])
        
        # Add the pattern itself
        patterns.append(match.group(1))
        
        # Update the last index
        last_index = match.end()
    
    # Add the remaining text after the last pattern
    string_parts.append(template[last_index:])
    
    return {'patterns': patterns, 'string_parts': string_parts}


def parse(template: str,
          pattern_start: str = "{",
          pattern_end: str = "}",
          separator_range: str = ",",
          separator_choices: str = "|",
          back_reference_marker: str = "$") -> Iterator[str]:
    """
    Parses a template string with special patterns and returns a generator
    
    Pattern formats:
    - {1,10} - Range from 1 to 10 (whitespace ignored)
    - {1,10,2} - Range from 1 to 10 with step 2 (whitespace ignored)
    - {option1|option2|option3} - Choices between options (whitespace preserved)
    - {singleOption} - Single choice (whitespace preserved)
    - {$n} - Back reference to the nth choice (0-based index)
    
    Args:
        template: Template string with {...} patterns
        pattern_start: Pattern start delimiter (default: '{')
        pattern_end: Pattern end delimiter (default: '}')
        separator_range: Separator for range patterns (default: ',')
        separator_choices: Separator for choices patterns (default: '|')
        back_reference_marker: Marker for back references (default: '$')
    
    Returns:
        Iterator of all pattern combinations
    
    Example:
        parse('Count: {1,5}')  # Generates "Count: 1", "Count: 2", ..., "Count: 5"
        parse('Color: {red|green|blue}')  # Generates "Color: red", "Color: green", "Color: blue"
        parse('You {see|hear} that. Once you {$0}.')  # Back references previous choice
    """
    result = sub_helper(template, pattern_start, pattern_end)
    patterns = result['patterns']
    string_parts = result['string_parts']
    
    # First pass: identify back references
    back_reference_regex = re.compile(re.escape(back_reference_marker) + r'(\d+)')
    back_references = []
    generator_patterns = []
    
    # Separate back references from regular patterns
    for pattern in patterns:
        back_ref_match = back_reference_regex.match(pattern)
        
        if back_ref_match and back_ref_match.group(0) == pattern:
            # This is a back reference pattern
            ref_index = int(back_ref_match.group(1))
            back_references.append(ref_index)
            generator_patterns.append(None)  # Placeholder
        else:
            # Regular pattern
            back_references.append(None)
            generator_patterns.append(pattern)
    
    # Convert patterns to generators
    generators = []
    for pattern in generator_patterns:
        if pattern is None:
            # Back reference placeholder - use a dummy generator with a single value
            generators.append(StaticGenerator(""))
        elif is_range_pattern(pattern, separator_range):
            # It's a range pattern, parse ignoring whitespace
            start, end, step = parse_range_pattern(pattern, separator_range)
            generators.append(range(start, end, step))
        else:
            # It's a choices pattern, preserve whitespace
            generators.append(pattern.split(separator_choices))
    
    # Identify the actual choice patterns (non-back references)
    actual_choice_patterns = []
    actual_choice_indices = []
    
    for i, pattern in enumerate(generator_patterns):
        if back_references[i] is None:
            # This is a regular pattern (not a back reference)
            actual_choice_patterns.append(generators[i])
            actual_choice_indices.append(i)
    
    # Generate all combinations of actual choices
    for actual_combination in cartesian_product(actual_choice_patterns):
        # Create a combination with back references resolved
        resolved_combination = [None] * len(patterns)
        
        # First, place the actual choices in their original positions
        for i, original_index in enumerate(actual_choice_indices):
            resolved_combination[original_index] = actual_combination[i]
        
        # Then, resolve the back references
        for i, ref_index in enumerate(back_references):
            if ref_index is not None:
                # This is a back reference
                # Find the actual value it refers to by finding the ref_index-th actual choice
                actual_choices_seen = 0
                ref_value = None
                
                for j in builtins_range(i):
                    if back_references[j] is None:
                        # This is an actual choice
                        if actual_choices_seen == ref_index:
                            # This is the one we want
                            ref_value = resolved_combination[j]
                            break
                        actual_choices_seen += 1
                
                if ref_value is not None:
                    # Valid back reference
                    resolved_combination[i] = ref_value
                else:
                    # Invalid back reference
                    resolved_combination[i] = f"{pattern_start}{back_reference_marker}{ref_index}{pattern_end}"
        
        # Build the result string
        result_str = string_parts[0]
        for i, value in enumerate(resolved_combination):
            result_str += str(value) + string_parts[i + 1]
        
        yield result_str


def count(template: str,
          pattern_start: str = "{",
          pattern_end: str = "}",
          separator_range: str = ",",
          separator_choices: str = "|",
          back_reference_marker: str = "$") -> int:
    """
    Counts the number of combinations for a given string template
    
    Pattern formats:
    - see "parse" function above
    
    Args:
        template: Template string with {...} patterns
        pattern_start: Pattern start delimiter (default: '{')
        pattern_end: Pattern end delimiter (default: '}')
        separator_range: Separator for range patterns (default: ',')
        separator_choices: Separator for choices patterns (default: '|')
        back_reference_marker: Marker for back references (default: '$')
    
    Returns:
        Total number of combinations
    
    Example:
        count('Count: {1,5}')  # 5
        count('Color: {red|green|blue}')  # 3
    """
    result = sub_helper(template, pattern_start, pattern_end)
    patterns = result['patterns']
    
    # First pass: identify back references
    back_reference_regex = re.compile(re.escape(back_reference_marker) + r'(\d+)')
    actual_choice_patterns = []
    
    # Separate back references from regular patterns
    for pattern in patterns:
        back_ref_match = back_reference_regex.match(pattern)
        
        if not (back_ref_match and back_ref_match.group(0) == pattern):
            # This is a regular pattern (not a back reference)
            actual_choice_patterns.append(pattern)
    
    # Count is the product of the number of choices for each actual pattern
    total_count = 1
    
    for pattern in actual_choice_patterns:
        if is_range_pattern(pattern, separator_range):
            # It's a range pattern, parse ignoring whitespace
            start, end, step = parse_range_pattern(pattern, separator_range)
            # Calculate the number of values in the range
            range_count = len(list(range(start, end, step)))
            total_count *= range_count
        else:
            # It's a choices pattern
            total_count *= len(pattern.split(separator_choices))
    
    return total_count


def choose(template: str,
           pattern_start: str = "{",
           pattern_end: str = "}",
           separator_range: str = ",",
           separator_choices: str = "|",
           back_reference_marker: str = "$") -> Callable:
    """
    Chooses one random or specified combination from the template
    
    Args:
        template: Template string with {...} patterns
        pattern_start: Pattern start delimiter (default: '{')
        pattern_end: Pattern end delimiter (default: '}')
        separator_range: Separator for range patterns (default: ',')
        separator_choices: Separator for choices patterns (default: '|')
        back_reference_marker: Marker for back references (default: '$')
    
    Returns:
        Function that returns a single combination
    
    Example:
        picker = choose("The {red|blue|green} {box|circle}")
        picker()  # Random combination like "The red box"
        picker(0, 1)  # Specific combination "The red circle"
    """
    result = sub_helper(template, pattern_start, pattern_end)
    patterns = result['patterns']
    string_parts = result['string_parts']
    
    # First pass: identify back references
    back_reference_regex = re.compile(re.escape(back_reference_marker) + r'(\d+)')
    back_references = []
    generator_patterns = []
    
    # Separate back references from regular patterns
    for pattern in patterns:
        back_ref_match = back_reference_regex.match(pattern)
        
        if back_ref_match and back_ref_match.group(0) == pattern:
            # This is a back reference pattern
            ref_index = int(back_ref_match.group(1))
            back_references.append(ref_index)
            generator_patterns.append(None)  # Placeholder
        else:
            # Regular pattern
            back_references.append(None)
            generator_patterns.append(pattern)
    
    # Convert patterns to arrays of values
    generators = []
    for pattern in generator_patterns:
        if pattern is None:
            # Back reference placeholder (will be replaced during resolution)
            generators.append([""])  # Dummy placeholder
        elif is_range_pattern(pattern, separator_range):
            # It's a range pattern, parse ignoring whitespace
            start, end, step = parse_range_pattern(pattern, separator_range)
            generators.append(list(range(start, end, step)))
        else:
            # It's a choices pattern, preserve whitespace
            generators.append(pattern.split(separator_choices))
    
    # Create the picker function
    def picker(*input_choices):
        # Create an array for all resolved values
        resolved_values = [None] * len(patterns)
        input_choice_index = 0  # Track position in input_choices
        
        # First, resolve actual pattern choices
        for idx in builtins_range(len(patterns)):
            if back_references[idx] is None:
                # This is a regular pattern (not a back reference)
                values = generators[idx]
                
                # Get the choice index (provided or random)
                if input_choice_index < len(input_choices):
                    choice_index = input_choices[input_choice_index]
                else:
                    choice_index = random.randint(0, len(values) - 1)
                
                # Store the selected value
                resolved_values[idx] = values[choice_index]
                input_choice_index += 1
        
        # Then, resolve all back references
        for idx in builtins_range(len(patterns)):
            if back_references[idx] is not None:
                # This is a back reference
                ref_index = back_references[idx]
                
                # Count up to the nth actual choice
                actual_choice_count = 0
                ref_value = None
                
                for j in builtins_range(len(patterns)):
                    if back_references[j] is None:
                        # This is an actual choice
                        if actual_choice_count == ref_index:
                            # Found the referenced choice
                            ref_value = resolved_values[j]
                            break
                        actual_choice_count += 1
                
                if ref_value is not None:
                    # Valid back reference
                    resolved_values[idx] = ref_value
                else:
                    # Invalid back reference
                    resolved_values[idx] = f"{pattern_start}{back_reference_marker}{ref_index}{pattern_end}"
        
        # Build the result string
        result_str = string_parts[0]
        for idx, value in enumerate(resolved_values):
            result_str += str(value) + string_parts[idx + 1]
        
        return result_str
    
    return picker
