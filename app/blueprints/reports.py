from flask import Blueprint, render_template

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/maintenance-summary')
def maintenance_summary():
    return "Maintenance Summary"  # Replace with your actual logic

@reports_bp.route('/cost-analysis')
def cost_analysis():
    return "Cost Analysis"  # Replace with your actual logic

@reports_bp.route('/performance-metrics')
def performance_metrics():
    notification_count = 0  # Set this to your actual notification count logic
    return render_template('your_template.html', notification_count=notification_count)
