import matplotlib.pyplot as plt
from typing import Union, Dict, List, Optional, Any

class Visualizer:
    """
    A class for handling visualizations within the per_datasets package.
    Designed to be decoupled from specific workflow logic.
    """
    
    def __init__(self):
        # We can initialize default styles here if needed
        pass

    def line_plot(self, 
                  data: Union[Dict[str, Any], List[float]], 
                  y: Optional[str] = None, 
                  x: Optional[str] = None, 
                  title: str = "Line Plot", 
                  xlabel: str = "Index", 
                  ylabel: str = "Value",
                  grid: bool = True):
        """
        Plots a line graph dynamically based on the input data and parameters.

        Args:
            data: The source data. Can be a dictionary (containing the data keys) or a direct list of values.
            y: The key string to look up in 'data' for the Y-axis values (required if data is a dict).
            x: The key string to look up in 'data' for the X-axis values (optional).
            title: The title of the plot.
            xlabel: The label for the X-axis.
            ylabel: The label for the Y-axis.
            grid: Whether to display grid lines (default True).
        """
        y_values = []
        x_values = None
        
        # 1. Handle Dictionary Input
        if isinstance(data, dict):
            if y is None:
                print("Error: Parameter 'y' (key) is required when data is a dictionary.")
                return
            
            if y not in data:
                print(f"Error: Key '{y}' not found in the provided data. keys available: {list(data.keys())}")
                return
            
            y_values = data[y]
            
            # Optional X-axis key
            if x:
                if x in data:
                    x_values = data[x]
                else:
                    print(f"Warning: X-axis key '{x}' not found. Plotting against index.")

        # 2. Handle List/Tuple Input
        elif isinstance(data, (list, tuple)):
            y_values = data
            
        else:
            print(f"Error: Data format '{type(data).__name__}' not supported. Please provide a dict or list.")
            return

        # 3. Create the Plot
        plt.figure(figsize=(10, 6))
        
        if x_values is not None:
            plt.plot(x_values, y_values, label=y if y else 'Series')
        else:
            plt.plot(y_values, label=y if y else 'Series')
            
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(grid)
        plt.legend()
        
        # Render
        plt.show()
