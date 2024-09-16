#!/usr/bin/env python3
"""Account setting module for the medical personnel"""

from typing import Dict, Any
import bcrypt
from dyno_med import Medical

class AccountSetting:
    def __init__(self):
        """Initialize the AccountSetting class"""
        self.medical = Medical()

    def change_username(self, med_user: object, account_setting: Dict[str, Any]) -> str:
        """
        Change the username of the medical expert

        Args:
            med_user: The user document object
            account_setting: A dictionary containing the new account settings
        Return: The new username
        """
        self.medical._ensure_param(med_user, account_setting)

        new_username = self.medical._ensure_string(account_setting.get('username', ''))
        med_user.username = new_username
        med_user.save()
        return new_username

    def change_password(self, med_user: object, current_password: str, new_password: str) -> str:
        """
        Change the password

        Args:
            med_user: The user document object
            current_password: The current password
            new_password: The password to replace the current password

        Return: A message indicating success or failure
        """
        self.medical._ensure_param(med_user, current_password, new_password)

        # Check the current password against the stored hashed password in the database
        if bcrypt.checkpw(current_password.encode('utf-8'), med_user.password.encode('utf-8')):
            # Hash the new password and store it in the database
            hashed_passwd = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            med_user.password = hashed_passwd
            med_user.save()
            return "Update successful!"
        else:
            return "Current password does not match with old password!"

    def delete_account(self, med_user: object) -> str:
        """
        Delete the medical expert account

        Args:
            med_user: The user document object to be deleted
        Return: A message indicating success on deletion of account
        """
        if med_user:
            med_user.delete()
            return 'Account deleted successfully'
        return 'No account found to delete'