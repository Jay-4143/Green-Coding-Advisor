from typing import Dict, List, Any, Optional
from datetime import datetime
from io import BytesIO
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class ReportGenerator:
    """Generate PDF and CSV reports for code analysis"""
    
    def generate_pdf_report(self, submission_data: Dict[str, Any], user_data: Optional[Dict] = None) -> BytesIO:
        """Generate a PDF report for code analysis"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#10b981'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Green Coding Advisor - Analysis Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        metadata_style = ParagraphStyle(
            'Metadata',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey
        )
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", metadata_style))
        if user_data:
            story.append(Paragraph(f"User: {user_data.get('username', 'N/A')}", metadata_style))
        story.append(Spacer(1, 0.3*inch))
        
        # File information
        story.append(Paragraph("File Information", styles['Heading2']))
        file_info = [
            ['Filename', submission_data.get('filename', 'N/A')],
            ['Language', submission_data.get('language', 'N/A').upper()],
            ['Analysis Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        file_table = Table(file_info, colWidths=[2*inch, 4*inch])
        file_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(file_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Green Score
        story.append(Paragraph("Green Score", styles['Heading2']))
        green_score = submission_data.get('green_score', 0)
        score_color = colors.green if green_score >= 80 else colors.orange if green_score >= 60 else colors.red
        score_data = [
            ['Green Score', f"{green_score}/100"],
            ['Status', 'Excellent' if green_score >= 80 else 'Good' if green_score >= 60 else 'Needs Improvement']
        ]
        score_table = Table(score_data, colWidths=[2*inch, 4*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('TEXTCOLOR', (1, 0), (1, 0), score_color),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(score_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Metrics
        story.append(Paragraph("Performance Metrics", styles['Heading2']))
        metrics_data = [
            ['Metric', 'Value'],
            ['Energy Consumption', f"{submission_data.get('energy_consumption_wh', 0):.4f} Wh"],
            ['CO₂ Emissions', f"{submission_data.get('co2_emissions_g', 0):.4f} g"],
            ['CPU Time', f"{submission_data.get('cpu_time_ms', 0):.2f} ms"],
            ['Memory Usage', f"{submission_data.get('memory_usage_mb', 0):.2f} MB"],
            ['Complexity Score', f"{submission_data.get('complexity_score', 0):.2f}"]
        ]
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 3.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Real-world impact
        if submission_data.get('real_world_impact'):
            story.append(Paragraph("Real-World Impact", styles['Heading2']))
            impact = submission_data['real_world_impact']
            impact_data = [
                ['Equivalent', 'Value'],
                ['Light Bulb Hours', f"{impact.get('light_bulb_hours', 0):.2f} hours"],
                ['Tree Planting Days', f"{impact.get('tree_planting_days', 0):.2f} days"],
                ['Car Miles', f"{impact.get('car_miles', 0):.4f} miles"]
            ]
            impact_table = Table(impact_data, colWidths=[2.5*inch, 3.5*inch])
            impact_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(impact_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Optimization suggestions
        suggestions = submission_data.get('suggestions', [])
        if suggestions:
            story.append(Paragraph("Optimization Suggestions", styles['Heading2']))
            for i, suggestion in enumerate(suggestions, 1):
                if isinstance(suggestion, dict):
                    finding = suggestion.get('finding', 'Suggestion')
                    explanation = suggestion.get('explanation', '')
                    story.append(Paragraph(f"{i}. {finding}", styles['Heading3']))
                    story.append(Paragraph(explanation, styles['Normal']))
                    if suggestion.get('before_code'):
                        story.append(Paragraph("Before:", styles['Normal']))
                        story.append(Paragraph(f"<pre>{suggestion['before_code']}</pre>", styles['Code']))
                    if suggestion.get('after_code'):
                        story.append(Paragraph("After:", styles['Normal']))
                        story.append(Paragraph(f"<pre>{suggestion['after_code']}</pre>", styles['Code']))
                    story.append(Spacer(1, 0.2*inch))
                else:
                    story.append(Paragraph(f"{i}. {suggestion}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Generated by Green Coding Advisor - Promoting Sustainable Software Development", footer_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_csv_report(self, submissions_data: List[Dict[str, Any]]) -> BytesIO:
        """Generate a CSV report for multiple submissions"""
        buffer = BytesIO()
        writer = csv.writer(buffer)
        
        # Write header
        writer.writerow([
            'ID', 'Filename', 'Language', 'Green Score', 'Energy (Wh)', 
            'CO₂ (g)', 'CPU Time (ms)', 'Memory (MB)', 'Complexity', 
            'Analysis Date'
        ])
        
        # Write data
        for submission in submissions_data:
            writer.writerow([
                submission.get('id', ''),
                submission.get('filename', ''),
                submission.get('language', ''),
                submission.get('green_score', 0),
                submission.get('energy_consumption_wh', 0),
                submission.get('co2_emissions_g', 0),
                submission.get('cpu_time_ms', 0),
                submission.get('memory_usage_mb', 0),
                submission.get('complexity_score', 0),
                submission.get('created_at', '')
            ])
        
        buffer.seek(0)
        return buffer
    
    def generate_user_metrics_csv(self, metrics_data: Dict[str, Any]) -> BytesIO:
        """Generate CSV report for user metrics"""
        buffer = BytesIO()
        writer = csv.writer(buffer)
        
        # Write metrics
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Submissions', metrics_data.get('total_submissions', 0)])
        writer.writerow(['Average Green Score', metrics_data.get('average_green_score', 0)])
        writer.writerow(['Total CO₂ Saved', metrics_data.get('total_co2_saved', 0)])
        writer.writerow(['Total Energy Saved', metrics_data.get('total_energy_saved', 0)])
        writer.writerow(['Badges Earned', metrics_data.get('badges_earned', 0)])
        
        buffer.seek(0)
        return buffer


report_generator = ReportGenerator()

