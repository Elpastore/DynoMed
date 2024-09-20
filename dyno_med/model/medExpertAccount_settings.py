from typing import Dict, Any
import bcrypt
from dyno_med import Medical
from flask import flash, jsonify, session

class AccountSetting:
    def __init__(self):
        """Initialize the AccountSetting class"""
        self.medical = Medical()

    def change_username(self, med_user: object, account_setting: Dict[str, Any]):
        """
        Change the username of the medical expert.
        """
        self.medical._check_input_params(med_user, account_setting)
        try:
            new_username = self.medical._ensure_string(account_setting.get('username', ''))
            med_user.username = new_username
            med_user.save()
            flash('Username changed successfully.', 'success')
            return jsonify({'success': True, 'message': 'Username changed successfully'})
        except Exception as e:
            flash(f'Failed to save username: {e}', 'danger')
            return jsonify({'success': False, 'message': f'Failed to change username: {e}'})

    def change_password(self, med_user: object, data: Dict[str, Any]):
        """
        Change the password of the user (passwords are integers).
        """
        self.medical._check_input_params(med_user, data)

        # Ensure integer passwords are converted to strings for processing
        new_password = str(data.get('new_password', '')).strip()
        old_password = str(data.get('old_password', '')).strip()
        confirm_password = str(data.get('confirm_password', '')).strip()

        # Ensure all password fields are provided
        if not new_password:
            flash("New password field is empty", 'danger')
            return jsonify({'success': False, 'message': 'New password is required'})

        if not old_password:
            flash("Old password field is empty", 'danger')
            return jsonify({'success': False, 'message': 'Old password is required'})

        if not confirm_password:
            flash("Confirm password field is empty", 'danger')
            return jsonify({'success': False, 'message': 'Confirm password is required'})

        # Check if old password matches the user's current password
        if not bcrypt.checkpw(old_password.encode('utf-8'), med_user.password.encode('utf-8')):
            flash('Current password does not match.', 'danger')
            return jsonify({'success': False, 'message': 'Old password is incorrect'})

        # Check if the new password matches the confirmation
        if new_password != confirm_password:
            flash('New password does not match the confirmed password.', 'danger')
            return jsonify({'success': False, 'message': 'New password and confirm password do not match'})

        # Hash the new password and save it
        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        med_user.password = new_hash
        med_user.save()

        flash('Password changed successfully.', 'success')
        return jsonify({'success': True, 'message': 'Password changed successfully'})


    def delete_account(self, med_user: object):
        """
        Delete the user's account.
        """
        if med_user:
            med_user.delete()
            flash('Account deactivated successfully.', 'success')
            session.clear()
            return jsonify({'success': True, 'message': 'Account deactivated. You have been logged out.'})
        else:
            flash('No account found to delete.', 'danger')
            return jsonify({'success': False, 'message': 'Failed to deactivate account'})

    def change_email(self, med_user: object, data: Dict[str, Any]):
        """
        Change the email address of the user.
        """
        self.medical._check_input_params(med_user, data)
        try:
            new_email = self.medical._ensure_string(data.get('email', ''))
            med_user.email = new_email
            med_user.save()
            flash('Email changed successfully.', 'success')
            return jsonify({'success': True, 'message': 'Email changed successfully'})
        except Exception as e:
            flash(f'Failed to change email: {e}', 'danger')
            return jsonify({'success': False, 'message': f'Failed to change email: {e}'})

    @staticmethod
    def unauthorized_access():
        flash('Unauthorized access.', 'danger')
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 401

    @staticmethod
    def user_not_found():
        flash('User not found.', 'danger')
        return jsonify({'success': False, 'message': 'User not found'}), 404
