function redirectToWorkshop(wid) {
    window.location.href = Flask.url_for('workshop_bp.edit', {wid: wid});
} 