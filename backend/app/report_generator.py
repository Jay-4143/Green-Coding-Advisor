from typing import Dict, List, Any, Optional
from datetime import datetime
from io import BytesIO
import csv
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

class ReportGenerator:
    """Generate PDF and CSV reports for code analysis"""
    
    def generate_comprehensive_pdf_report(
        self, 
        submission_data: Dict[str, Any], 
        optimization_data: Optional[Dict[str, Any]] = None,
        user_data: Optional[Dict] = None,
        badge_data: Optional[List[Dict]] = None
    ) -> BytesIO:
        """Generate a comprehensive PDF report with all sections including optimization"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Define custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#10b981'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading2_style = ParagraphStyle(
            'Heading2',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#059669'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Code'],
            fontSize=8,
            fontName='Courier',
            leftIndent=20,
            rightIndent=20,
            backColor=colors.HexColor('#f3f4f6'),
            borderColor=colors.grey,
            borderWidth=1,
            borderPadding=5
        )
        
        metadata_style = ParagraphStyle(
            'Metadata',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey
        )
        
        # ========== SECTION 1: PROJECT OVERVIEW ==========
        story.append(Paragraph("Green Coding Advisor", title_style))
        story.append(Paragraph("Comprehensive Code Analysis & Optimization Report", ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=20
        )))
        story.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        story.append(Paragraph(f"<b>Report Generated:</b> {report_date}", metadata_style))
        if user_data:
            story.append(Paragraph(f"<b>User:</b> {user_data.get('username', 'N/A')} ({user_data.get('email', 'N/A')})", metadata_style))
        story.append(Paragraph(f"<b>Project:</b> Green Coding Advisor - Sustainable Software Development Platform", metadata_style))
        story.append(Paragraph(f"<b>Purpose:</b> Code efficiency analysis and optimization for energy sustainability", metadata_style))
        story.append(Paragraph(f"<b>Detected Language:</b> {submission_data.get('language', 'N/A').upper()}", metadata_style))
        story.append(Spacer(1, 0.3*inch))
        story.append(PageBreak())
        
        # ========== SECTION 2: ORIGINAL CODE ==========
        story.append(Paragraph("1. Original Code", heading2_style))
        original_code = submission_data.get('code_content', '') or optimization_data.get('original_code', '') if optimization_data else ''
        if original_code:
            # Split long code into chunks for better formatting
            code_lines = original_code.split('\n')
            if len(code_lines) > 50:
                story.append(Paragraph(f"<i>Code length: {len(code_lines)} lines</i>", styles['Normal']))
                # Show first 30 and last 20 lines
                preview_code = '\n'.join(code_lines[:30] + ['... (code truncated in preview) ...'] + code_lines[-20:])
                story.append(Preformatted(preview_code, code_style))
            else:
                story.append(Preformatted(original_code, code_style))
        else:
            story.append(Paragraph("<i>Original code not available in submission data</i>", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        story.append(PageBreak())
        
        # ========== SECTION 3: CODE ANALYSIS SUMMARY ==========
        story.append(Paragraph("2. Code Analysis Summary", heading2_style))
        
        analysis_data = [
            ['Metric', 'Value', 'Status'],
            ['Green Score', f"{submission_data.get('green_score', 0):.2f}/100", 
             'Excellent' if submission_data.get('green_score', 0) >= 80 else 
             'Good' if submission_data.get('green_score', 0) >= 60 else 'Needs Improvement'],
            ['Energy Consumption', f"{submission_data.get('energy_consumption_wh', 0):.4f} Wh", 
             'Low' if submission_data.get('energy_consumption_wh', 0) < 0.01 else 
             'Medium' if submission_data.get('energy_consumption_wh', 0) < 0.1 else 'High'],
            ['CO₂ Emissions', f"{submission_data.get('co2_emissions_g', 0):.4f} g", 
             'Low' if submission_data.get('co2_emissions_g', 0) < 5 else 
             'Medium' if submission_data.get('co2_emissions_g', 0) < 20 else 'High'],
            ['CPU Time', f"{submission_data.get('cpu_time_ms', 0):.2f} ms", 
             'Fast' if submission_data.get('cpu_time_ms', 0) < 1 else 
             'Moderate' if submission_data.get('cpu_time_ms', 0) < 5 else 'Slow'],
            ['Memory Usage', f"{submission_data.get('memory_usage_mb', 0):.2f} MB", 
             'Low' if submission_data.get('memory_usage_mb', 0) < 5 else 
             'Medium' if submission_data.get('memory_usage_mb', 0) < 20 else 'High'],
            ['Complexity Score', f"{submission_data.get('complexity_score', 0):.2f}", 
             'Simple' if submission_data.get('complexity_score', 0) < 3 else 
             'Moderate' if submission_data.get('complexity_score', 0) < 7 else 'Complex']
        ]
        
        analysis_table = Table(analysis_data, colWidths=[2*inch, 2*inch, 2*inch])
        analysis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        story.append(analysis_table)
        story.append(Spacer(1, 0.3*inch))
        
        # ========== SECTION 4: MODEL EVALUATION METRICS ==========
        story.append(Paragraph("3. Model Evaluation Metrics", heading2_style))
        story.append(Paragraph(
            "The following metrics indicate the accuracy of our AI models in predicting code efficiency:",
            styles['Normal']
        ))
        
        model_metrics_data = [
            ['Metric', 'Description', 'Typical Range'],
            ['R² Score', 'Coefficient of determination - measures how well the model fits the data', '0.0 - 1.0 (higher is better)'],
            ['MAE', 'Mean Absolute Error - average prediction error', 'Lower is better'],
            ['RMSE', 'Root Mean Squared Error - penalizes larger errors more', 'Lower is better']
        ]
        
        model_table = Table(model_metrics_data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
        model_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(model_table)
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(
            "<i>Note: Model metrics are calculated during training. For this analysis, models with R² > 0.7 are considered reliable.</i>",
            metadata_style
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # ========== SECTION 5: OPTIMIZATION SUGGESTIONS ==========
        story.append(Paragraph("4. Optimization Suggestions", heading2_style))
        suggestions = submission_data.get('suggestions', []) or []
        if not suggestions and optimization_data:
            # Extract suggestions from optimization data
            improvements = optimization_data.get('improvements_explanation', '')
            if improvements:
                suggestions = [{'explanation': line.strip(), 'severity': 'medium'} 
                             for line in improvements.split('\n') if line.strip()]
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                if isinstance(suggestion, dict):
                    finding = suggestion.get('finding', f'Suggestion {i}')
                    explanation = suggestion.get('explanation', '')
                    severity = suggestion.get('severity', 'medium').upper()
                    improvement = suggestion.get('predicted_improvement', {})
                    
                    story.append(Paragraph(f"<b>{i}. {finding}</b>", styles['Heading3']))
                    story.append(Paragraph(f"<b>Severity:</b> {severity}", styles['Normal']))
                    story.append(Paragraph(explanation, styles['Normal']))
                    
                    if improvement:
                        if improvement.get('green_score'):
                            story.append(Paragraph(f"<b>Expected Green Score Improvement:</b> +{improvement['green_score']} points", styles['Normal']))
                        if improvement.get('energy_wh'):
                            story.append(Paragraph(f"<b>Expected Energy Reduction:</b> {abs(improvement['energy_wh']):.4f} Wh", styles['Normal']))
                    
                    if suggestion.get('before_code'):
                        story.append(Paragraph("<b>Before (Inefficient):</b>", styles['Normal']))
                        story.append(Preformatted(suggestion['before_code'], code_style))
                    
                    if suggestion.get('after_code'):
                        story.append(Paragraph("<b>After (Optimized):</b>", styles['Normal']))
                        story.append(Preformatted(suggestion['after_code'], code_style))
                    
                    story.append(Spacer(1, 0.2*inch))
                else:
                    story.append(Paragraph(f"{i}. {suggestion}", styles['Normal']))
        else:
            story.append(Paragraph("<i>No specific optimization suggestions available.</i>", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        story.append(PageBreak())
        
        # ========== SECTION 6: OPTIMIZED CODE ==========
        if optimization_data and optimization_data.get('optimized_code'):
            story.append(Paragraph("5. Optimized Code", heading2_style))
            optimized_code = optimization_data['optimized_code']
            code_lines = optimized_code.split('\n')
            
            if len(code_lines) > 50:
                story.append(Paragraph(f"<i>Optimized code length: {len(code_lines)} lines</i>", styles['Normal']))
                preview_code = '\n'.join(code_lines[:30] + ['... (code truncated in preview) ...'] + code_lines[-20:])
                story.append(Preformatted(preview_code, code_style))
            else:
                story.append(Preformatted(optimized_code, code_style))
            
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(
                "<b>Note:</b> The optimized code produces the same output as the original code but with improved efficiency.",
                styles['Normal']
            ))
            story.append(Spacer(1, 0.3*inch))
            story.append(PageBreak())
        else:
            story.append(Paragraph("5. Optimized Code", heading2_style))
            story.append(Paragraph("<i>Optimized code not available. Run code optimization to generate optimized version.</i>", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
        
        # ========== SECTION 7: PERFORMANCE COMPARISON ==========
        story.append(Paragraph("6. Performance Comparison", heading2_style))
        
        if optimization_data and optimization_data.get('comparison_table'):
            comp_table = optimization_data['comparison_table']
            comparison_data = [
                ['Metric', 'Original Code', 'Optimized Code', 'Improvement']
            ]
            
            # Add each metric comparison
            for metric_key, metric_data in comp_table.items():
                if isinstance(metric_data, dict):
                    original_val = metric_data.get('original', 'N/A')
                    optimized_val = metric_data.get('optimized', 'N/A')
                    improvement = metric_data.get('improvement', 'N/A')
                    comparison_data.append([metric_key.replace('_', ' ').title(), original_val, optimized_val, improvement])
            
            comp_pdf_table = Table(comparison_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            comp_pdf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (1, 1), (1, -1), colors.red),
                ('TEXTCOLOR', (2, 1), (2, -1), colors.green),
                ('TEXTCOLOR', (3, 1), (3, -1), colors.blue),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
            ]))
            story.append(comp_pdf_table)
        else:
            # Fallback comparison using original metrics
            comparison_data = [
                ['Metric', 'Original Code', 'Optimized Code', 'Status'],
                ['Green Score', f"{submission_data.get('green_score', 0):.2f}/100", 'N/A', 'Optimization not run'],
                ['Energy Consumption', f"{submission_data.get('energy_consumption_wh', 0):.4f} Wh", 'N/A', 'Optimization not run'],
                ['CO₂ Emissions', f"{submission_data.get('co2_emissions_g', 0):.4f} g", 'N/A', 'Optimization not run']
            ]
            comp_pdf_table = Table(comparison_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            comp_pdf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(comp_pdf_table)
        
        story.append(Spacer(1, 0.3*inch))
        
        # ========== SECTION 8: SUSTAINABILITY IMPACT ==========
        story.append(Paragraph("7. Sustainability Impact", heading2_style))
        
        impact = submission_data.get('real_world_impact', {}) or {}
        if optimization_data and optimization_data.get('comparison_table'):
            # Calculate improvements
            comp_table = optimization_data['comparison_table']
            energy_improvement = comp_table.get('energy_usage', {}).get('improvement', '0 Wh')
            co2_improvement = comp_table.get('co2_emissions', {}).get('improvement', '0 g')
            
            impact_data = [
                ['Impact Metric', 'Value'],
                ['Energy Saved', energy_improvement],
                ['CO₂ Reduced', co2_improvement]
            ]
            
            if impact:
                impact_data.extend([
                    ['Light Bulb Hours Equivalent', f"{impact.get('light_bulb_hours', 0):.2f} hours"],
                    ['Tree Planting Days Equivalent', f"{impact.get('tree_planting_days', 0):.2f} days"],
                    ['Car Miles Equivalent', f"{impact.get('car_miles', 0):.4f} miles"]
                ])
        else:
            impact_data = [
                ['Impact Metric', 'Value'],
                ['Light Bulb Hours', f"{impact.get('light_bulb_hours', 0):.2f} hours" if impact else 'N/A'],
                ['Tree Planting Days', f"{impact.get('tree_planting_days', 0):.2f} days" if impact else 'N/A'],
                ['Car Miles', f"{impact.get('car_miles', 0):.4f} miles" if impact else 'N/A']
            ]
        
        impact_table = Table(impact_data, colWidths=[3*inch, 3*inch])
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
        
        # ========== SECTION 9: BADGES & ACHIEVEMENTS ==========
        story.append(Paragraph("8. Badges & Achievements", heading2_style))
        
        green_score = submission_data.get('green_score', 0)
        
        # Determine sustainability level
        if green_score >= 90:
            level = "Expert"
            level_color = colors.HexColor('#10b981')
        elif green_score >= 75:
            level = "Advanced"
            level_color = colors.HexColor('#34d399')
        elif green_score >= 60:
            level = "Intermediate"
            level_color = colors.HexColor('#fbbf24')
        else:
            level = "Beginner"
            level_color = colors.orange
        
        badges_data = [
            ['Achievement', 'Status'],
            ['Sustainability Level', level],
            ['Green Score Badge', 'Earned' if green_score >= 60 else 'Not Earned'],
            ['Energy Efficient Badge', 'Earned' if submission_data.get('energy_consumption_wh', 100) < 0.05 else 'Not Earned'],
            ['Low Carbon Badge', 'Earned' if submission_data.get('co2_emissions_g', 100) < 10 else 'Not Earned']
        ]
        
        if badge_data:
            for badge in badge_data:
                badges_data.append([badge.get('name', 'Badge'), 'Earned'])
        
        badges_table = Table(badges_data, colWidths=[3*inch, 3*inch])
        badges_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (1, 1), (1, 1), level_color),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(badges_table)
        story.append(Spacer(1, 0.3*inch))
        
        # ========== SECTION 10: FINAL VERDICT ==========
        story.append(Paragraph("9. Final Verdict", heading2_style))
        
        # Calculate overall rating
        score = green_score
        if score >= 80:
            rating = "Excellent"
            rating_color = colors.green
            recommendation = "Code is production-ready with excellent efficiency. Deploy with confidence."
        elif score >= 60:
            rating = "Good"
            rating_color = colors.HexColor('#fbbf24')
            recommendation = "Code is good but can be improved. Consider applying optimization suggestions."
        else:
            rating = "Needs Improvement"
            rating_color = colors.red
            recommendation = "Code requires optimization before deployment. Apply suggested improvements."
        
        verdict_data = [
            ['Aspect', 'Assessment'],
            ['Overall Performance Rating', rating],
            ['Optimization Success Level', 'High' if optimization_data else 'Not Optimized'],
            ['Deployment Recommendation', recommendation],
            ['Next Steps', 'Monitor performance and continue optimizing' if score >= 60 else 'Apply optimization suggestions and re-analyze']
        ]
        
        verdict_table = Table(verdict_data, colWidths=[2.5*inch, 3.5*inch])
        verdict_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (1, 1), (1, 1), rating_color),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(verdict_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("Generated by Green Coding Advisor - Promoting Sustainable Software Development", footer_style))
        story.append(Paragraph(f"Report ID: {submission_data.get('id', 'N/A')} | Generated: {report_date}", footer_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
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
    
    def generate_json_report(
        self,
        submission_data: Dict[str, Any],
        optimization_data: Optional[Dict[str, Any]] = None,
        user_data: Optional[Dict] = None,
        badge_data: Optional[List[Dict]] = None
    ) -> str:
        """Generate a comprehensive JSON report"""
        report = {
            "project_overview": {
                "project_name": "Green Coding Advisor",
                "purpose": "Code efficiency analysis and optimization for energy sustainability",
                "report_generated": datetime.now().isoformat(),
                "detected_language": submission_data.get('language', 'N/A'),
                "user": user_data.get('username', 'N/A') if user_data else 'N/A'
            },
            "original_code": submission_data.get('code_content', '') or (optimization_data.get('original_code', '') if optimization_data else ''),
            "code_analysis_summary": {
                "green_score": submission_data.get('green_score', 0),
                "energy_consumption_wh": submission_data.get('energy_consumption_wh', 0),
                "co2_emissions_g": submission_data.get('co2_emissions_g', 0),
                "cpu_time_ms": submission_data.get('cpu_time_ms', 0),
                "memory_usage_mb": submission_data.get('memory_usage_mb', 0),
                "complexity_score": submission_data.get('complexity_score', 0)
            },
            "model_evaluation_metrics": {
                "description": "Model metrics indicate prediction accuracy",
                "r2_score_range": "0.0 - 1.0 (higher is better)",
                "mae_description": "Mean Absolute Error - lower is better",
                "rmse_description": "Root Mean Squared Error - lower is better"
            },
            "optimization_suggestions": submission_data.get('suggestions', []),
            "optimized_code": optimization_data.get('optimized_code', '') if optimization_data else None,
            "performance_comparison": optimization_data.get('comparison_table', {}) if optimization_data else {},
            "sustainability_impact": submission_data.get('real_world_impact', {}),
            "badges_achievements": {
                "sustainability_level": self._get_sustainability_level(submission_data.get('green_score', 0)),
                "badges": badge_data or []
            },
            "final_verdict": {
                "overall_rating": self._get_overall_rating(submission_data.get('green_score', 0)),
                "optimization_success": "High" if optimization_data else "Not Optimized",
                "recommendation": self._get_recommendation(submission_data.get('green_score', 0))
            }
        }
        return json.dumps(report, indent=2)
    
    def generate_html_report(
        self,
        submission_data: Dict[str, Any],
        optimization_data: Optional[Dict[str, Any]] = None,
        user_data: Optional[Dict] = None,
        badge_data: Optional[List[Dict]] = None
    ) -> str:
        """Generate a comprehensive HTML report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Green Coding Advisor - Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #10b981; text-align: center; }}
        h2 {{ color: #059669; border-bottom: 2px solid #10b981; padding-bottom: 10px; }}
        h3 {{ color: #047857; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #10b981; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border: 1px solid #ddd; }}
        tr:nth-child(even) {{ background: #f9fafb; }}
        .code-block {{ background: #f3f4f6; border: 1px solid #ddd; padding: 15px; border-radius: 4px; font-family: monospace; white-space: pre-wrap; overflow-x: auto; }}
        .original {{ border-left: 4px solid #ef4444; }}
        .optimized {{ border-left: 4px solid #10b981; }}
        .badge {{ display: inline-block; padding: 5px 10px; border-radius: 4px; margin: 5px; }}
        .badge-earned {{ background: #10b981; color: white; }}
        .badge-not-earned {{ background: #e5e7eb; color: #6b7280; }}
        .footer {{ text-align: center; color: #6b7280; margin-top: 40px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Green Coding Advisor</h1>
        <h2 style="text-align: center; border: none;">Comprehensive Code Analysis & Optimization Report</h2>
        
        <h2>1. Project Overview</h2>
        <table>
            <tr><th>Property</th><th>Value</th></tr>
            <tr><td>Project Name</td><td>Green Coding Advisor</td></tr>
            <tr><td>Purpose</td><td>Code efficiency analysis and optimization for energy sustainability</td></tr>
            <tr><td>Report Generated</td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
            <tr><td>Detected Language</td><td>{submission_data.get('language', 'N/A').upper()}</td></tr>
            <tr><td>User</td><td>{user_data.get('username', 'N/A') if user_data else 'N/A'}</td></tr>
        </table>
        
        <h2>2. Original Code</h2>
        <div class="code-block original">{self._escape_html(submission_data.get('code_content', '') or (optimization_data.get('original_code', '') if optimization_data else 'N/A'))}</div>
        
        <h2>3. Code Analysis Summary</h2>
        <table>
            <tr><th>Metric</th><th>Value</th><th>Status</th></tr>
            <tr><td>Green Score</td><td>{submission_data.get('green_score', 0):.2f}/100</td><td>{'Excellent' if submission_data.get('green_score', 0) >= 80 else 'Good' if submission_data.get('green_score', 0) >= 60 else 'Needs Improvement'}</td></tr>
            <tr><td>Energy Consumption</td><td>{submission_data.get('energy_consumption_wh', 0):.4f} Wh</td><td>{'Low' if submission_data.get('energy_consumption_wh', 0) < 0.01 else 'Medium' if submission_data.get('energy_consumption_wh', 0) < 0.1 else 'High'}</td></tr>
            <tr><td>CO₂ Emissions</td><td>{submission_data.get('co2_emissions_g', 0):.4f} g</td><td>{'Low' if submission_data.get('co2_emissions_g', 0) < 5 else 'Medium' if submission_data.get('co2_emissions_g', 0) < 20 else 'High'}</td></tr>
            <tr><td>CPU Time</td><td>{submission_data.get('cpu_time_ms', 0):.2f} ms</td><td>{'Fast' if submission_data.get('cpu_time_ms', 0) < 1 else 'Moderate' if submission_data.get('cpu_time_ms', 0) < 5 else 'Slow'}</td></tr>
            <tr><td>Memory Usage</td><td>{submission_data.get('memory_usage_mb', 0):.2f} MB</td><td>{'Low' if submission_data.get('memory_usage_mb', 0) < 5 else 'Medium' if submission_data.get('memory_usage_mb', 0) < 20 else 'High'}</td></tr>
            <tr><td>Complexity Score</td><td>{submission_data.get('complexity_score', 0):.2f}</td><td>{'Simple' if submission_data.get('complexity_score', 0) < 3 else 'Moderate' if submission_data.get('complexity_score', 0) < 7 else 'Complex'}</td></tr>
        </table>
        
        <h2>4. Model Evaluation Metrics</h2>
        <p>R² Score: Measures how well the model fits the data (0.0 - 1.0, higher is better)</p>
        <p>MAE: Mean Absolute Error - average prediction error (lower is better)</p>
        <p>RMSE: Root Mean Squared Error - penalizes larger errors more (lower is better)</p>
        
        <h2>5. Optimization Suggestions</h2>
        {self._generate_suggestions_html(submission_data.get('suggestions', []), optimization_data)}
        
        {f'<h2>6. Optimized Code</h2><div class="code-block optimized">{self._escape_html(optimization_data.get("optimized_code", ""))}</div>' if optimization_data and optimization_data.get('optimized_code') else '<h2>6. Optimized Code</h2><p><i>Optimized code not available. Run code optimization to generate optimized version.</i></p>'}
        
        <h2>7. Performance Comparison</h2>
        {self._generate_comparison_html(optimization_data.get('comparison_table', {}) if optimization_data else {}, submission_data)}
        
        <h2>8. Sustainability Impact</h2>
        {self._generate_impact_html(submission_data.get('real_world_impact', {}), optimization_data)}
        
        <h2>9. Badges & Achievements</h2>
        {self._generate_badges_html(submission_data.get('green_score', 0), badge_data)}
        
        <h2>10. Final Verdict</h2>
        {self._generate_verdict_html(submission_data.get('green_score', 0), optimization_data)}
        
        <div class="footer">
            <p>Generated by Green Coding Advisor - Promoting Sustainable Software Development</p>
            <p>Report ID: {submission_data.get('id', 'N/A')} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
        """
        return html
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))
    
    def _generate_suggestions_html(self, suggestions: List, optimization_data: Optional[Dict]) -> str:
        """Generate HTML for optimization suggestions"""
        if not suggestions and optimization_data:
            improvements = optimization_data.get('improvements_explanation', '')
            if improvements:
                suggestions = [{'explanation': line.strip()} for line in improvements.split('\n') if line.strip()]
        
        if not suggestions:
            return "<p><i>No specific optimization suggestions available.</i></p>"
        
        html = "<ul>"
        for i, suggestion in enumerate(suggestions, 1):
            if isinstance(suggestion, dict):
                finding = suggestion.get('finding', f'Suggestion {i}')
                explanation = suggestion.get('explanation', '')
                severity = suggestion.get('severity', 'medium').upper()
                html += f"<li><b>{finding}</b> ({severity})<br>{explanation}"
                if suggestion.get('before_code'):
                    html += f"<br><b>Before:</b><div class='code-block original'>{self._escape_html(suggestion['before_code'])}</div>"
                if suggestion.get('after_code'):
                    html += f"<br><b>After:</b><div class='code-block optimized'>{self._escape_html(suggestion['after_code'])}</div>"
                html += "</li>"
            else:
                html += f"<li>{suggestion}</li>"
        html += "</ul>"
        return html
    
    def _generate_comparison_html(self, comparison_table: Dict, submission_data: Dict) -> str:
        """Generate HTML for performance comparison"""
        if not comparison_table:
            return f"""
            <table>
                <tr><th>Metric</th><th>Original Code</th><th>Optimized Code</th><th>Status</th></tr>
                <tr><td>Green Score</td><td>{submission_data.get('green_score', 0):.2f}/100</td><td>N/A</td><td>Optimization not run</td></tr>
                <tr><td>Energy Consumption</td><td>{submission_data.get('energy_consumption_wh', 0):.4f} Wh</td><td>N/A</td><td>Optimization not run</td></tr>
                <tr><td>CO₂ Emissions</td><td>{submission_data.get('co2_emissions_g', 0):.4f} g</td><td>N/A</td><td>Optimization not run</td></tr>
            </table>
            """
        
        html = "<table><tr><th>Metric</th><th>Original Code</th><th>Optimized Code</th><th>Improvement</th></tr>"
        for metric_key, metric_data in comparison_table.items():
            if isinstance(metric_data, dict):
                original_val = metric_data.get('original', 'N/A')
                optimized_val = metric_data.get('optimized', 'N/A')
                improvement = metric_data.get('improvement', 'N/A')
                html += f"<tr><td>{metric_key.replace('_', ' ').title()}</td><td style='color: red;'>{original_val}</td><td style='color: green;'><b>{optimized_val}</b></td><td style='color: blue;'>{improvement}</td></tr>"
        html += "</table>"
        return html
    
    def _generate_impact_html(self, impact: Dict, optimization_data: Optional[Dict]) -> str:
        """Generate HTML for sustainability impact"""
        html = "<table><tr><th>Impact Metric</th><th>Value</th></tr>"
        if optimization_data and optimization_data.get('comparison_table'):
            comp_table = optimization_data['comparison_table']
            energy_improvement = comp_table.get('energy_usage', {}).get('improvement', '0 Wh')
            co2_improvement = comp_table.get('co2_emissions', {}).get('improvement', '0 g')
            html += f"<tr><td>Energy Saved</td><td>{energy_improvement}</td></tr>"
            html += f"<tr><td>CO₂ Reduced</td><td>{co2_improvement}</td></tr>"
        if impact:
            html += f"<tr><td>Light Bulb Hours</td><td>{impact.get('light_bulb_hours', 0):.2f} hours</td></tr>"
            html += f"<tr><td>Tree Planting Days</td><td>{impact.get('tree_planting_days', 0):.2f} days</td></tr>"
            html += f"<tr><td>Car Miles</td><td>{impact.get('car_miles', 0):.4f} miles</td></tr>"
        html += "</table>"
        return html
    
    def _generate_badges_html(self, green_score: float, badge_data: Optional[List[Dict]]) -> str:
        """Generate HTML for badges"""
        level = self._get_sustainability_level(green_score)
        html = f"<table><tr><th>Achievement</th><th>Status</th></tr>"
        html += f"<tr><td>Sustainability Level</td><td><b>{level}</b></td></tr>"
        html += f"<tr><td>Green Score Badge</td><td><span class='badge {'badge-earned' if green_score >= 60 else 'badge-not-earned'}'>{'Earned' if green_score >= 60 else 'Not Earned'}</span></td></tr>"
        if badge_data:
            for badge in badge_data:
                html += f"<tr><td>{badge.get('name', 'Badge')}</td><td><span class='badge badge-earned'>Earned</span></td></tr>"
        html += "</table>"
        return html
    
    def _generate_verdict_html(self, green_score: float, optimization_data: Optional[Dict]) -> str:
        """Generate HTML for final verdict"""
        rating = self._get_overall_rating(green_score)
        recommendation = self._get_recommendation(green_score)
        html = f"<table><tr><th>Aspect</th><th>Assessment</th></tr>"
        html += f"<tr><td>Overall Performance Rating</td><td><b>{rating}</b></td></tr>"
        html += f"<tr><td>Optimization Success Level</td><td>{'High' if optimization_data else 'Not Optimized'}</td></tr>"
        html += f"<tr><td>Deployment Recommendation</td><td>{recommendation}</td></tr>"
        html += "</table>"
        return html
    
    def _get_sustainability_level(self, score: float) -> str:
        """Get sustainability level from score"""
        if score >= 90:
            return "Expert"
        elif score >= 75:
            return "Advanced"
        elif score >= 60:
            return "Intermediate"
        else:
            return "Beginner"
    
    def _get_overall_rating(self, score: float) -> str:
        """Get overall rating from score"""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        else:
            return "Needs Improvement"
    
    def _get_recommendation(self, score: float) -> str:
        """Get deployment recommendation from score"""
        if score >= 80:
            return "Code is production-ready with excellent efficiency. Deploy with confidence."
        elif score >= 60:
            return "Code is good but can be improved. Consider applying optimization suggestions."
        else:
            return "Code requires optimization before deployment. Apply suggested improvements."
    
    def generate_weekly_email_body(
        self,
        start_date: str,
        end_date: str,
        user_data: Dict[str, Any],
        stats: Dict[str, Any],
        recent_submissions: List[Dict[str, Any]]
    ) -> str:
        """Generate HTML body for weekly email report"""
        
        # Calculate sustainability level and motivational message
        avg_score = stats.get('average_green_score', 0)
        if avg_score >= 80:
            level = "Sustainability Champion"
            message = "Outstanding work! You are leading the way in sustainable coding."
            color = "#10b981" # Green
        elif avg_score >= 60:
            level = "Eco-Conscious Coder"
            message = "Great progress! You're making a real difference."
            color = "#3b82f6" # Blue
        else:
            level = "Green Coder in Training"
            message = "Keep going! Every optimization counts towards a greener future."
            color = "#f59e0b" # Amber
            
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #f3f4f6; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: white; padding: 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 24px; font-weight: bold; }}
                .header p {{ margin: 10px 0 0; opacity: 0.9; }}
                .content {{ padding: 30px; }}
                .greeting {{ font-size: 18px; color: #1f2937; margin-bottom: 20px; }}
                .summary-card {{ background-color: {color}10; border-left: 4px solid {color}; padding: 20px; border-radius: 4px; margin-bottom: 30px; }}
                .summary-title {{ color: {color}; font-weight: bold; font-size: 16px; margin-bottom: 5px; }}
                .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px; }}
                .stat-item {{ background-color: #f9fafb; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #e5e7eb; }}
                .stat-value {{ font-size: 24px; font-weight: bold; color: #111827; margin-bottom: 5px; }}
                .stat-label {{ font-size: 13px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }}
                .submissions-list {{ margin-bottom: 30px; }}
                .submission-item {{ display: flex; justify-content: space-between; align-items: center; padding: 12px; border-bottom: 1px solid #f3f4f6; }}
                .submission-item:last-child {{ border-bottom: none; }}
                .file-info {{ display: flex; flex-direction: column; }}
                .filename {{ font-weight: 500; color: #374151; }}
                .language {{ font-size: 12px; color: #9ca3af; }}
                .score {{ font-weight: bold; padding: 4px 8px; border-radius: 4px; font-size: 14px; }}
                .score-high {{ background-color: #d1fae5; color: #065f46; }}
                .score-med {{ background-color: #dbeafe; color: #1e40af; }}
                .score-low {{ background-color: #fee2e2; color: #991b1b; }}
                .footer {{ background-color: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; border-top: 1px solid #e5e7eb; }}
                .btn {{ display: inline-block; background-color: #059669; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 20px; }}
                .btn:hover {{ background-color: #047857; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Weekly Green Coding Report</h1>
                    <p>{start_date} - {end_date}</p>
                </div>
                
                <div class="content">
                    <p class="greeting">Hello {user_data.get('username', 'Green Coder')},</p>
                    <p>Here's a summary of your sustainable coding impact this week.</p>
                    
                    <div class="summary-card">
                        <div class="summary-title">{level}</div>
                        <p>{message}</p>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-value">{stats.get('total_submissions', 0)}</div>
                            <div class="stat-label">Submissions</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">{stats.get('average_green_score', 0):.1f}</div>
                            <div class="stat-label">Avg Green Score</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">{stats.get('total_co2_saved', 0):.2f}g</div>
                            <div class="stat-label">CO₂ Saved</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">{stats.get('total_energy_saved', 0):.2f}Wh</div>
                            <div class="stat-label">Energy Saved</div>
                        </div>
                    </div>
                    
                    <h3>Top Submissions This Week</h3>
                    <div class="submissions-list">
        """
        
        if recent_submissions:
            for sub in recent_submissions[:5]:
                score = sub.get('green_score', 0)
                score_class = "score-high" if score >= 80 else "score-med" if score >= 60 else "score-low"
                
                html += f"""
                        <div class="submission-item">
                            <div class="file-info">
                                <span class="filename">{sub.get('filename', 'code.py')}</span>
                                <span class="language">{sub.get('language', 'unknown')}</span>
                            </div>
                            <span class="score {{score_class}}">{{score:.1f}}</span>
                        </div>
                """.format(score_class=score_class, score=score)
        else:
            html += "<p><i>No submissions this week. Time to start coding!</i></p>"
            
        html += f"""
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="{user_data.get('dashboard_url', '#')}" class="btn">View Full Dashboard</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Generated by Green Coding Advisor AI</p>
                    <p>Keep coding green!</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html

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

