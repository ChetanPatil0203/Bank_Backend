from flask import Blueprint, request
from app.controllers.settings_controller import SettingsController

settings_bp = Blueprint('settings_bp', __name__)

@settings_bp.route('/profile', methods=['GET', 'PUT'])
def profile():
    if request.method == 'GET':
        return SettingsController.get_profile()
    return SettingsController.update_profile()

@settings_bp.route('/preferences', methods=['GET', 'PUT'])
def preferences():
    if request.method == 'GET':
        return SettingsController.get_preferences()
    return SettingsController.update_preferences()

@settings_bp.route('/security/change-password', methods=['POST'])
def change_password():
    return SettingsController.change_password()

@settings_bp.route('/security/activity', methods=['GET'])
def get_activity():
    return SettingsController.get_activity()
