import tokenize

from io import BytesIO

def strip_comments_from_source(source):
    io_obj = BytesIO(source.encode('utf-8'))

    
    try:
        tokens = tokenize.tokenize(io_obj.readline)
        # We need to filter tokens.
        # untokenize expects an iterable of (type, string) or (type, string, start, end, line)
        
        filtered_tokens = []
        for t in tokens:
            if t.type == tokenize.COMMENT:
                continue
            # If we just skip comment, untokenize might leave whitespace?
            # untokenize effectively reconstructs based on spacing if we provide just type/string?
            # Actually untokenize is smart enough to handle spacing if we rely on it, 
            # BUT if we remove tokens, we might mess up line numbers if we keep the original start/end?
            # The simple way: use (type, string) tuples only.
            
            # However, untokenize( (type,string) ) loses format.
            # We want to keep format.
            
            # Better approach:
            # Reconstruct string manually using start/end indices?
            # Scan tokens, if comment, don't add to output.
            
            filtered_tokens.append(t)
            
        return tokenize.untokenize(filtered_tokens)
    except Exception as e:
        print(f"Error parsing: {e}")
        return source

test_code = """
# Header comment
def foo():
    x = 1 # Inline comment
    s = "Has # hash"
    '''
    Docstring
    '''
    return x
"""

if __name__ == "__main__":
    print("Testing strip...")
    print(strip_comments_from_source(test_code))
