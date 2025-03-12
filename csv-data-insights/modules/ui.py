import gradio as gr

class GradioUI:
    def __init__(self, data_handler, model_handler, visualizer, pdf_generator):
        self.data_handler = data_handler
        self.model_handler = model_handler
        self.visualizer = visualizer
        self.pdf_generator = pdf_generator
        self.current_llm_response = None  # Store the latest LLM response
    
    def load_csv_callback(self, file):
        """Callback for CSV loading"""
        success, message, columns = self.data_handler.load_csv(file.name if file else None)
        
        default_x = columns[0] if columns else None
        default_y = columns[1] if len(columns) > 1 else None
        
        return message, gr.update(choices=columns, value=default_x), gr.update(choices=columns, value=default_y)
    
    def query_callback(self, question):
        """Callback for processing queries"""
        df = self.data_handler.get_dataframe()
        if df is None:
            return "⚠️ Please upload a CSV file first."
        
        data_json = self.data_handler.get_sample_json()
        response = self.model_handler.process_query(question, data_json)
        
        
        self.current_llm_response = response
        
        return response
    
    def plot_callback(self, x_axis, y_axis, graph_type):
        """Callback for generating plots"""
        df = self.data_handler.get_dataframe()
        return self.visualizer.create_plot(df, x_axis, y_axis, graph_type)
    
    def generate_pdf_callback(self, x_axis, y_axis):
        """Callback for generating a PDF report with data insights"""
        df = self.data_handler.get_dataframe()
        if df is None:
            return "⚠️ Please upload a CSV file first."
        
        
        pdf_path = self.pdf_generator.generate_insights_pdf(
            df=df, 
            llm_analysis=self.current_llm_response, 
            include_plots=True,
            x_axis=x_axis,
            y_axis=y_axis
        )
        
        if isinstance(pdf_path, str) and pdf_path.startswith('❌'):
            return pdf_path  
        
        return f"✅ PDF report downloaded successfully: {pdf_path}"
    
    def build_interface(self):
        """Build the Gradio interface"""
        with gr.Blocks() as app:
            gr.Markdown("# AI-powered CSV Analysis")

           
            with gr.Tab("Data Upload"):
                file_input = gr.File(label="Upload CSV", type="filepath")
                upload_button = gr.Button("Load CSV")
                status_output = gr.Textbox(label="Status", interactive=False)
            
            
            with gr.Tab("Query Data"):
                question_input = gr.Textbox(label="Ask a question about the CSV")
                submit_button = gr.Button("Submit")
                response_output = gr.Textbox(label="LLM Response", interactive=False, lines=10)

           
            with gr.Tab("Visualize Data"):
                with gr.Row():
                    x_axis_dropdown = gr.Dropdown(label="X-axis", choices=[], interactive=True)
                    y_axis_dropdown = gr.Dropdown(label="Y-axis", choices=[], interactive=True)
                
                graph_type_dropdown = gr.Radio(
                    choices=["Scatter Plot", "Line Chart", "Bar Chart", "Histogram"],
                    label="Graph Type"
                )
                plot_button = gr.Button("Generate Graph")
                graph_output = gr.Image()
            
          
            with gr.Tab("Generate Report"):
                gr.Markdown("### Generate a PDF report with data insights")
                gr.Markdown("The report will include dataset overview, statistical summary, and visualizations.")
                
                # Use the same dropdowns for consistency, but we'll only access their values
                pdf_button = gr.Button("Generate PDF Report")
                pdf_status = gr.Textbox(label="PDF Status", interactive=False)

            
            upload_button.click(
                self.load_csv_callback, 
                inputs=[file_input], 
                outputs=[status_output, x_axis_dropdown, y_axis_dropdown]
            )
            
            submit_button.click(
                self.query_callback, 
                inputs=[question_input], 
                outputs=[response_output]
            )
            
            plot_button.click(
                self.plot_callback, 
                inputs=[x_axis_dropdown, y_axis_dropdown, graph_type_dropdown], 
                outputs=[graph_output]
            )
            
           
            pdf_button.click(
                self.generate_pdf_callback,
                inputs=[x_axis_dropdown, y_axis_dropdown],
                outputs=[pdf_status]
            )
            
        return app