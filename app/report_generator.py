from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from .chart_generator import create_gauge_chart, create_bar_chart

def create_report(data, output_file, url):
    doc = SimpleDocTemplate(output_file, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.darkblue,
        spaceAfter=12
    )

    # Add title
    elements.append(Paragraph("Google Lighthouse Report", title_style))
    elements.append(Paragraph(f"URL: {url}", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))

    # Add gauge charts
    categories = data['lighthouseResult']['categories']
    gauges = [
        create_gauge_chart(categories['performance']['score'], "Performance"),
        create_gauge_chart(categories['accessibility']['score'], "Accessibility"),
        create_gauge_chart(categories['best-practices']['score'], "Best Practices"),
        create_gauge_chart(categories['seo']['score'], "SEO")
    ]
    elements.append(Table([gauges[:2], gauges[2:]], colWidths=[3*inch, 3*inch]))

    # Add bar chart for load times
    audits = data['lighthouseResult']['audits']
    load_times = {
        'First Contentful Paint': audits['first-contentful-paint']['numericValue'] / 1000,
        'Time to Interactive': audits['interactive']['numericValue'] / 1000,
        'Speed Index': audits['speed-index']['numericValue'] / 1000,
        'Total Blocking Time': audits['total-blocking-time']['numericValue'] / 1000,
        'Largest Contentful Paint': audits['largest-contentful-paint']['numericValue'] / 1000,
        'Cumulative Layout Shift': audits['cumulative-layout-shift']['numericValue']
    }
    elements.append(create_bar_chart(load_times))

    # Add table of tests
    test_data = [['Test', 'Category', 'Score', 'Status']]
    for audit_id, audit in audits.items():
        if 'score' in audit:
            test_data.append([
                audit['title'],
                audit.get('group', 'N/A'),
                f"{audit['score'] * 100:.0f}%",
                'PASS' if audit['score'] == 1 else 'FAIL'
            ])

    test_table = Table(test_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1*inch])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(test_table)

    doc.build(elements)