import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def __init__(self, output_path="plot.png"):
        self.output_path = output_path
    
    def create_plot(self, df, x_axis, y_axis, graph_type):
        """Generate visualization based on selected columns and graph type"""
        if df is None:
            return "⚠️ Please upload a CSV file first."
        
        if x_axis not in df.columns or y_axis not in df.columns:
            return "⚠️ Invalid column selection."
        
        plt.figure(figsize=(10, 5))
        
        try:
            if graph_type == "Scatter Plot":
                sns.scatterplot(data=df, x=x_axis, y=y_axis)
            elif graph_type == "Line Chart":
                sns.lineplot(data=df, x=x_axis, y=y_axis)
            elif graph_type == "Bar Chart":
                sns.barplot(data=df, x=x_axis, y=y_axis)
            elif graph_type == "Histogram":
                sns.histplot(df[x_axis], bins=20, kde=True)
            
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            plt.title(f"{graph_type}: {x_axis} vs {y_axis}")
            
            
            plt.savefig(self.output_path)
            plt.close()
            return self.output_path
        except Exception as e:
            return f"❌ Error generating graph: {str(e)}"