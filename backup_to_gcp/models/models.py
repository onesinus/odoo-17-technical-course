import requests
import tempfile
import base64
import os
import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.service.db import list_dbs

from google.cloud import storage
from datetime import timedelta


class GcpBackupConfig(models.Model):
    _name = 'backup_to_gcp.config'
    _description = 'Backup to GCP Config'

    # is_backup_all = fields.Boolean(string='Backup All Databases?', default=True)
    admin_password = fields.Char(string='Odoo Admin Password', required=True)
    backup_format = fields.Selection(
        [
            ('sql', '.sql (without filestore)'),
            ('zip', '.zip (include filestore)')
        ],
        string='Backup Format',
        default="sql"
    )

    # database_name = fields.Char(string='Database Name', required=True)

    @api.model
    def _get_database_selection(self):
        db_names = list_dbs(self.env.cr)
        return [(db, db) for db in db_names]

    database_name = fields.Selection(selection=_get_database_selection, string='Database Name', required=True)
    credentials_file = fields.Binary(string='Credentials File', attachment=True, required=True)
    gcs_bucket_name = fields.Char(string='GCS Bucket Name', required=True)

    is_scheduler_active = fields.Boolean(string='Backup Active?', default=True)
    scheduler_interval = fields.Integer(string='Every X hours', default=24, required=True)

    is_send_email = fields.Boolean(string='Email Notification?')
    notification_type = fields.Selection(
        [
            ('all', 'All (Success & Error)'),
            ('error', 'Error Only'),
            ('success', 'Success Only'),
        ],
        string='Notification Type',
        default="error"
    )
    email_notification_receiver = fields.Char(string='Receiver Email')

    is_auto_remove = fields.Boolean(string='Auto Remove?')
    keep_data_x_days = fields.Integer(string="Keep data X days", default=7)

    @api.constrains('keep_data_x_days')
    def _check_minimum_value(self):
        for record in self:
            if record.keep_data_x_days < 1:
                raise ValidationError("Minimum value for 'Keep data X days' field is 1.")

    @api.model
    def create(self, vals):
        result = super(GcpBackupConfig, self).create(vals)
        result.create_scheduler()
        return result

    def write(self, vals):
        result = super(GcpBackupConfig, self).write(vals)
        self.create_scheduler()
        return result

    def unlink(self):
        scheduler_name_format = "Backup to GCP Schedule #{}"
        for config in self:
            scheduler = self.env['ir.cron'].with_context(active_test=False).search(
                [
                    ('name', '=', scheduler_name_format.format(config.id))
                ],
                limit=1
            )
            if scheduler:
                # Delete the scheduler
                scheduler.unlink()

        return super().unlink()

    @api.model
    def _scheduler_method(self, config_id):
        config = self.browse(config_id)
        if config:
            self.backup_database_to_gcp(config)

    @api.model
    def create_scheduler(self):
        configs = self.search([])
        model_id = self.env['ir.model'].search([('model', '=', 'backup_to_gcp.config')], limit=1).id
        for config in configs:
            if config:
                config_id = config.id
                name = f"Backup to GCP Schedule #{config_id}"
                scheduler_interval = config.scheduler_interval
                active = config.is_scheduler_active
                cron = self.env['ir.cron'].with_context(active_test=False).search([('name', '=', name)])

                scheduler_data = { # here we can set time execution time
                    'name': name,
                    'interval_number': scheduler_interval,
                    'interval_type': 'hours',
                    'model_id': model_id,
                    'code': f'model._scheduler_method({config_id})',
                    'priority': config_id + 10,
                    'user_id': self.env.user.id,
                    'numbercall': -1,
                    'active': active
                }
                if cron:
                    cron.write(scheduler_data)
                else:
                    self.env['ir.cron'].create(scheduler_data)

    @staticmethod
    def _create_temp_file(content, suffix=""):
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(dir="/tmp", suffix=suffix, delete=False)

        # Write the decoded data to the temporary file
        temp_file.write(content)

        # Close the temporary file
        temp_file.close()

        # Use the temporary file path for further operations
        file_path = temp_file.name
        return file_path

    def _send_email(self, config, email_type, message):
        try:
            if config.is_send_email and config.email_notification_receiver:
                if (config.notification_type == email_type) or config.notification_type == "all":
                    outgoing_mail_server = self.env['ir.mail_server'].search([], order='sequence asc', limit=1)

                    recipient = config.email_notification_receiver
                    subject = f"[Backup Notification]: {email_type} - {message}"
                    body = "Here is information about your odoo database backup:\n\n" \
                           f"Status: {email_type} \n" \
                           f"Message: {message} \n" \
                           "\n" \
                           "\n" \
                           "Note: You can run the backup manually by executing in the Scheduled Actions Odoo " \
                           "or wait for the next execution period. \n" \
                           "Ensure you have set the right Database Name, Odoo Admin Password, " \
                           "GCP Credentials (.json) in Settings > Backup > Backup to GCP Configuration " \
                           "\n" \
                           "\n" \
                           f"Thank You."

                    catch_all_domain = self.env["ir.config_parameter"].sudo().get_param("mail.catchall.domain")
                    response_mail = "auto_backup@%s" % catch_all_domain \
                        if catch_all_domain else self.env.user.partner_id.email
                    email = outgoing_mail_server.build_email(response_mail, [recipient], subject, body)
                    outgoing_mail_server.send_email(email)
        except Exception as e:
            print(f"Failed sending email, Error: {e}")

    def _delete_older_backup_data(self, config):
        credentials_file_binary = config.credentials_file
        decoded_data = base64.b64decode(credentials_file_binary)
        temp_credential_file = self._create_temp_file(decoded_data)

        client = storage.Client.from_service_account_json(temp_credential_file)
        bucket_name = config.gcs_bucket_name
        database_name = config.database_name
        backup_folder = ""  # root (no specific prefix or folder path to consider)
        days_to_keep = config.keep_data_x_days  # Number of days to keep backup data

        threshold_date = datetime.datetime.now() - timedelta(days=days_to_keep)

        bucket = client.get_bucket(bucket_name)
        blob_list = list(bucket.list_blobs(prefix=backup_folder))

        # Iterate through each blob and delete if older than the threshold date
        for blob in blob_list:
            blob_updated_naive = blob.updated.replace(tzinfo=None)
            blob_name = blob.name

            if (blob_updated_naive < threshold_date) and (database_name in blob_name):
                blob.delete()
                print(f"Deleted backup file: {blob.name}")

        os.remove(temp_credential_file)

    def backup_database_to_gcp(self, config):
        try:
            admin_password = config.admin_password
            backup_format = config.backup_format or "sql"

            # Step 1: Create the database backup
            database_name = config.database_name
            backup_name = f"{database_name}-{datetime.datetime.now().strftime('%d-%b-%Y-%H-%M')}.{backup_format}"

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            backup_url = f"{base_url}/web/database/backup"

            payload = {
                "master_pwd": admin_password,
                "name": database_name,
                "backup_format": backup_format
            }

            response = requests.post(backup_url, data=payload)
            if response.status_code == 200:
                # Save the backup file as a temporary file
                backup_file_path = self._create_temp_file(response.content, backup_format)

                # Step 2: Upload the backup file to the GCS bucket
                credentials_file_binary = config.credentials_file
                decoded_data = base64.b64decode(credentials_file_binary) # Decode the binary data
                temp_credential_file = self._create_temp_file(decoded_data)

                gcs_bucket_name = config.gcs_bucket_name
                client = storage.Client.from_service_account_json(temp_credential_file)

                bucket = client.get_bucket(gcs_bucket_name)
                blob = bucket.blob(backup_name)
                blob.upload_from_filename(backup_file_path)

                # Step 3: Clean up the local backup file (optional)
                os.remove(backup_file_path)
                os.remove(temp_credential_file)
                self._send_email(config, "success", f"Backup: {backup_name} is success ")
            else:
                error_message = "Failed to create the database backup"
                self._send_email(config, "error", error_message)
                print(error_message)
        except Exception as e:
            error_message = f"Failed backup database, Error: {e}"
            self._send_email(config, "error", error_message)
            print(error_message)

        if config.is_auto_remove:
            try:
                self._delete_older_backup_data(config)
            except Exception as e:
                delete_older_backup_message = f"Error deleting the older backup data, Error Message: {e}"
                print(delete_older_backup_message)

        # import wdb
        # wdb.set_trace()
