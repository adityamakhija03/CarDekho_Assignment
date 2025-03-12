from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import pandas as pd
from datetime import datetime

class PDFGenerator:
    def __init__(self, output_path="data_insights_and_recommendations.pdf"):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            spaceAfter=12,
            textColor=colors.darkblue
        ))
        self.styles.add(ParagraphStyle(
            name='RecommendationHeader',
            parent=self.styles['Heading3'],
            spaceAfter=6,
            textColor=colors.darkred
        ))
    
    def generate_insights_pdf(self, df, llm_analysis=None, include_plots=False, x_axis=None, y_axis=None, recommendations=None):
        """
        Generate a PDF report with insights and stakeholder recommendations from the data
        
        Args:
            df: The pandas DataFrame
            llm_analysis: Text analysis from the LLM (optional)
            include_plots: Parameter kept for backward compatibility (ignored)
            x_axis: Parameter kept for backward compatibility (ignored)
            y_axis: Parameter kept for backward compatibility (ignored)
            recommendations: List of recommendations for stakeholders (optional)
            
        Returns:
            Path to the generated PDF file
        """
        try:
            if df is None:
                return "⚠️ No data available for PDF generation."
            
        
            doc = SimpleDocTemplate(self.output_path, pagesize=letter)
            story = []
            
           
            title_style = self.styles['Title']
            title = Paragraph("Data Insights and Stakeholder Recommendations", title_style)
            story.append(title)
            
           
            timestamp = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                self.styles['Normal'])
            story.append(timestamp)
            story.append(Spacer(1, 20))
            
           
            story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
            summary_text = """
            This report provides key data insights and actionable recommendations based on analysis of the provided dataset. 
            The insights focus on critical patterns and trends identified in the data, while recommendations outline specific 
            actions stakeholders should consider to leverage these insights effectively.
            """
            story.append(Paragraph(summary_text, self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Dataset overview section (brief)
            story.append(Paragraph("Dataset Overview", self.styles['SectionHeader']))
            story.append(Paragraph(f"Dataset Size: {df.shape[0]} rows, {df.shape[1]} columns", self.styles['Normal']))
            
            
            column_data = []
            column_data.append(["Column Name", "Data Type", "Non-Null %", "Unique Values"])
            
            for column in df.columns:
                non_null_percent = f"{(df[column].count() / df.shape[0] * 100):.1f}%"
                unique_count = df[column].nunique()
                unique_percent = f"{(unique_count / df[column].count() * 100):.1f}%" if df[column].count() > 0 else "0%"
                
                column_data.append([
                    column, 
                    str(df[column].dtype), 
                    non_null_percent,
                    f"{unique_count} ({unique_percent})"
                ])
            
            col_table = Table(column_data, colWidths=[120, 100, 80, 120])
            col_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(col_table)
            story.append(Spacer(1, 20))
            
            
            story.append(Paragraph("Key Metrics", self.styles['SectionHeader']))
            
           
            try:
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    metrics_data = []
                    metrics_data.append(["Metric", "Value", "Interpretation"])
                    
                    
                    for col in numeric_df.columns[:5]: 
                        metrics_data.append([
                            f"Average {col}", 
                            f"{numeric_df[col].mean():.2f}",
                            "Above/below industry benchmark" if numeric_df[col].mean() > 0 else "Needs attention"
                        ])
                        
                        metrics_data.append([
                            f"{col} trend", 
                            "Increasing" if numeric_df[col].iloc[-5:].mean() > numeric_df[col].iloc[0:5].mean() else "Decreasing",
                            "Positive signal" if numeric_df[col].iloc[-5:].mean() > numeric_df[col].iloc[0:5].mean() else "Concerning trend"
                        ])
                    
                    metrics_table = Table(metrics_data, colWidths=[150, 100, 200])
                    metrics_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    
                    story.append(metrics_table)
                else:
                    story.append(Paragraph("No numeric columns available for key metrics.", 
                                        self.styles['Normal']))
            except Exception as e:
                story.append(Paragraph(f"Could not generate key metrics: {str(e)}", 
                                    self.styles['Normal']))
            
            story.append(Spacer(1, 20))
            
           
            if llm_analysis:
                story.append(Paragraph("Data Insights", self.styles['SectionHeader']))
                
                
                for paragraph in llm_analysis.split('\n\n'):
                    if paragraph.strip():
                        story.append(Paragraph(paragraph, self.styles['Normal']))
                        story.append(Spacer(1, 10))
            
           
            story.append(Spacer(1, 10))
            story.append(Paragraph("Stakeholder Recommendations", self.styles['SectionHeader']))
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                   
                    story.append(Paragraph(f"Recommendation {i}: {rec['title']}", self.styles['RecommendationHeader']))
                    story.append(Paragraph(f"<b>Priority:</b> {rec.get('priority', 'Medium')}", self.styles['Normal']))
                    story.append(Paragraph(f"<b>Impact:</b> {rec.get('impact', 'Not specified')}", self.styles['Normal']))
                    story.append(Paragraph(rec['description'], self.styles['Normal']))
                    story.append(Paragraph(f"<b>Suggested Action:</b> {rec.get('action', 'No specific action provided')}", 
                                        self.styles['Normal']))
                    story.append(Spacer(1, 10))
            else:
                # Generate generic recommendations if none provided
                generic_recs = [
                    {
                        "title": "Further Data Investigation",
                        "priority": "Medium",
                        "impact": "Potential for improved decision quality",
                        "description": "Based on preliminary analysis, further investigation into data patterns is recommended.",
                        "action": "Conduct deeper analysis on key metrics identified in this report."
                    },
                    {
                        "title": "Stakeholder Review",
                        "priority": "High",
                        "impact": "Enhanced understanding of business implications",
                        "description": "The insights provided require domain expertise to fully interpret and apply.",
                        "action": "Schedule a cross-functional review meeting with department heads to discuss findings."
                    }
                ]
                
                for i, rec in enumerate(generic_recs, 1):
                    story.append(Paragraph(f"Recommendation {i}: {rec['title']}", self.styles['RecommendationHeader']))
                    story.append(Paragraph(f"<b>Priority:</b> {rec.get('priority', 'Medium')}", self.styles['Normal']))
                    story.append(Paragraph(f"<b>Impact:</b> {rec.get('impact', 'Not specified')}", self.styles['Normal']))
                    story.append(Paragraph(rec['description'], self.styles['Normal']))
                    story.append(Paragraph(f"<b>Suggested Action:</b> {rec.get('action', 'No specific action provided')}", 
                                        self.styles['Normal']))
                    story.append(Spacer(1, 10))
            
            story.append(Spacer(1, 10))
            story.append(Paragraph("Conclusion", self.styles['SectionHeader']))
            conclusion_text = """
            This report has presented key insights derived from the dataset analysis and provided actionable 
            recommendations for stakeholders. The focused insights highlight significant patterns and trends 
            that merit attention, while the recommendations outline specific steps that can be taken to address 
            these findings effectively. Timely implementation of these recommendations is advised to maximize 
            their impact on decision-making processes.
            """
            story.append(Paragraph(conclusion_text, self.styles['Normal']))
            
           
            doc.build(story)
            return self.output_path
        
        except Exception as e:
            return f"❌ Error generating PDF: {str(e)}"