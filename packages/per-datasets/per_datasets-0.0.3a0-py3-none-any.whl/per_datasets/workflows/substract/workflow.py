"""
Subtract workflow function for per_datasets
"""

def subtract(a: float, b: float) -> float:
    """
    ## subtract
    
    Subtracts the second number from the first number as a workflow example.
    
    ### **parameters**
    
    a : float
        Number to subtract from
        
    b : float
        Number to subtract
        
    ### **returns**
    
    float
        Difference of a and b (a - b)
        
    ### **examples**
    
    >>> from per_datasets.workflows.subtract import subtract
    >>> result = subtract(10.5, 3.2)
    >>> print(result)
    7.3
    """
    return a - b